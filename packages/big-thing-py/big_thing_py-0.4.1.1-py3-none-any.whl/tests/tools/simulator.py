from tests.tools.test_tools_utils import *
from tests.tools.sop_elements import *
from tabulate import tabulate


class Simulator():

    def __init__(self, simulation_file_path: str = None, clean_start: bool = True, debug: bool = False) -> None:
        self._name = None
        self._middleware_list: List[SoPMiddlewareElement] = []

        self._simulation_file_path = simulation_file_path
        self._simulation_code: List[SimulationData] = []
        self._simulation_start_time = None
        self._middleware_tree_config = None

        self._clean_start = clean_start

        self._simulation_statistics = {
            'middleware_list': []
        }

        self._user_data = {'function': self._on_message, 'user_data': None}
        self._debug = debug

        self._event_log: List[EventHolder] = []
        self._new_event_log: List[EventHolder] = []
        self._event_queue: Queue = Queue()

    @exception_wrapper
    def init(self):
        simulation_file = json_file_read(
            self._simulation_file_path)
        self._name = simulation_file['name']
        for chunk in simulation_file['simulation']:
            self._simulation_code.append(SimulationData(chunk=chunk))

    @exception_wrapper
    def wrapup(self):
        for middleware in self._middleware_list:
            for thing in middleware._thing_list:
                thing.kill()
            middleware.kill()

    def make_middleware_tree(self):
        middleware_tree = {}
        middleware_events: List[SimulationData] = []

        for event in self._simulation_code:
            if event.event_type == EventType.MIDDLEWARE_RUN:
                middleware_events.append(event)
        middleware_events = sorted(
            middleware_events, key=lambda x: x.level, reverse=True)

        for event in middleware_events:
            if event.level not in middleware_tree:
                middleware_tree[event.level] = [event]
            else:
                middleware_tree[event.level].append(event)
        return middleware_tree

    def make_thing_tree(self):
        thing_tree = dict(super=[], basic=[])
        thing_events: List[SimulationData] = []

        for event in self._simulation_code:
            if event.event_type == EventType.THING_RUN:
                thing_events.append(event)
        thing_events = sorted(
            thing_events, key=lambda x: x.is_super, reverse=True)

        for event in thing_events:
            if event.is_super:
                thing_tree['super'].append(event)
            else:
                thing_tree['basic'].append(event)
        return thing_tree

    def build_middleware_env(self):
        middleware_tree = self.make_middleware_tree()
        for level, layer in middleware_tree.items():
            layer: List[SimulationData]
            thread_list: List[Thread] = []

            SOPTEST_LOG_DEBUG(
                f'start to build Middleware layer level{level}...', 0)
            for middleware_data in layer:
                self._simulation_code.remove(middleware_data)
                mqtt_monitor_client = SoPMQTTMonitor(
                    name=middleware_data.name, host=middleware_data.host, port=middleware_data.port, debug=self._debug, level=middleware_data.level)

                if middleware_data.parent_host:
                    middleware = SoPMiddlewareElement(parent_mqtt_monitor_client=self.select_middleware(middleware_data.parent_host, middleware_data.parent_port)._mqtt_monitor_client,
                                                      data=middleware_data, clean_start=self._clean_start, with_parent=True, debug=self._debug)
                else:
                    middleware = SoPMiddlewareElement(
                        mqtt_monitor_client=mqtt_monitor_client, data=middleware_data, clean_start=self._clean_start, with_parent=False, debug=self._debug)

                thread = Thread(target=middleware.run, kwargs={'simulator': self, 'user_data': self._user_data},
                                name=f'{middleware._name}_thread')
                mqtt_monitor_client._client.user_data_set(self._user_data)
                self._middleware_list.append(middleware)
                thread_list.append(thread)
                thread.start()
                self._event_log.append(EventHolder(
                    middleware_name=middleware._name, event_type=EventType.MIDDLEWARE_RUN, level=middleware._level, timestamp=time.time(),
                    host=middleware._host, port=middleware._port))

            for thread in thread_list:
                thread_name = thread.getName()
                thread.join()
                for event in self._event_log:
                    if event.middleware_name == thread_name.split('_')[-1]:
                        event.duration = time.time() - event.timestamp

            SOPTEST_LOG_DEBUG(
                f'Middleware layer level {level} online...', 0)

    def build_thing_env(self):
        thing_tree = self.make_thing_tree()
        for thing_type, layer in thing_tree.items():
            layer: List[SimulationData]
            thread_list: List[Thread] = []

            SOPTEST_LOG_DEBUG(
                f'start to build register {thing_type} things...', 0)
            for thing_data in layer:
                self._simulation_code.remove(thing_data)

                sel_middleware = self.select_middleware(
                    host=thing_data.host, port=thing_data.port)
                thing = SoPThingElement(mqtt_monitor_client=sel_middleware.get_mqtt_monitor_client(),
                                        data=thing_data, debug=self._debug)
                sel_middleware._thing_list.append(thing)
                thread = Thread(target=thing.run, args=())
                thread_list.append(thread)
                thread.start()
                self._event_log.append(EventHolder(
                    thing_name=thing._name, event_type=EventType.THING_RUN, level=thing._level, timestamp=time.time(),
                    host=thing._host, port=thing._port))

            for thread in thread_list:
                thread_name = thread.getName()
                thread.join()
                for event in self._event_log:
                    if event.thing_name == thread_name.split('_')[-1]:
                        event.duration = time.time() - event.timestamp

            SOPTEST_LOG_DEBUG(
                f'thing register {thing_type} type finish...', 0)

    def kill_env(self):
        for event in self._simulation_code:
            if event.event_type == EventType.MIDDLEWARE_RUN:
                if event.parent_host:
                    middleware = SoPMiddlewareElement(parent_mqtt_monitor_client=self.select_middleware(event.parent_host, event.parent_port)._mqtt_monitor_client,
                                                      data=event, clean_start=self._clean_start, with_parent=True, debug=self._debug)
                else:
                    middleware = SoPMiddlewareElement(
                        data=event, clean_start=self._clean_start, with_parent=False, debug=self._debug)

                middleware.make_middleware_config_file()
                self._middleware_list.append(middleware)

        for middleware in self._middleware_list:
            middleware.kill()

        SOPTEST_LOG_DEBUG('All Middleware was killed!', 0)

    @exception_wrapper
    def start(self):
        self._simulation_start_time = time.time()

        self.build_middleware_env()
        self.build_thing_env()

        for event in self._simulation_code:
            cur_time = time.time()
            sel_middleware = self.select_middleware(
                host=event.host, port=event.port)

            if event.event_type == EventType.DELAY:
                delay = SoPDelayElement(data=event)
                delay.run()
                # self._event_log.append(EventHolder(
                #     event_type=event.event_type, timestamp=cur_time))
            else:
                # wait until timestamp is reached
                if event.timestamp:
                    while time.time() - self._simulation_start_time < event.timestamp:
                        time.sleep(0.0001)

                if event.event_type == EventType.SCENARIO_ADD:
                    sel_mqtt_monitor_client = sel_middleware.get_mqtt_monitor_client()
                    scenario = SoPScenarioElement(
                        mqtt_monitor_client=sel_mqtt_monitor_client, data=event, debug=self._debug)
                    self.user_data_set(sel_mqtt_monitor_client, scenario)

                    # if super thing is include in scenario, then run check_pc_service_list first
                    for thing in sel_middleware._thing_list:
                        if thing._is_super == True:
                            retry = 10
                            while not self.check_thing_exist(host=event.host, port=event.port, thing_name=thing._name, is_super=True) and retry:
                                SOPTEST_LOG_DEBUG(
                                    f'wait for super thing {thing._name} detect...', 1)
                                time.sleep(1)
                                retry -= 1
                            break

                    time.sleep(1)
                    scenario.add()
                    sel_middleware._scenario_list.append(scenario)

                    # FIXME: change it to 10 after debug super thing!!!
                    retry = 100

                    # wait for scenario add to middleware's DB
                    time.sleep(1)
                    while not self.check_scenario_ready(host=event.host, port=event.port, scenario_name=scenario._name, stuck_handling=True, timeout=20) and retry:
                        time.sleep(1)
                        retry -= 1
                elif event.event_type == EventType.SCENARIO_VERIFY:
                    for scenario in sel_middleware._scenario_list:
                        if scenario._name == event.name:
                            scenario.verify()
                            break
                elif event.event_type == EventType.SCENARIO_RUN:
                    for scenario in sel_middleware._scenario_list:
                        if scenario._name == event.name:
                            if self.check_scenario_state(
                                host=event.host, port=event.port, scenario_name=scenario._name,
                                target_scenario_state=[ScenarioStateType.COMPLETED,
                                                       ScenarioStateType.INITIALIZED]):
                                scenario.run()
                                break
                elif event.event_type == EventType.SCENARIO_STOP:
                    for scenario in sel_middleware._scenario_list:
                        if scenario._name == event.name:
                            while True:
                                scenario_state = self.check_scenario_state(
                                    host=event.host, port=event.port, scenario_name=scenario._name)
                                if scenario_state == ScenarioStateType.RUNNING:
                                    scenario.stop()
                                elif scenario_state in [ScenarioStateType.COMPLETED, ScenarioStateType.INITIALIZED, ScenarioStateType.STUCKED]:
                                    SOPTEST_LOG_DEBUG(
                                        f'Scenario {scenario._name} is already in {scenario_state}', 1)
                                time.sleep(1)
                            break
                elif event.event_type == EventType.SCENARIO_UPDATE:
                    for scenario in sel_middleware._scenario_list:
                        if scenario._name == event.name:
                            while not self.check_scenario_state(
                                    host=event.host, port=event.port, scenario_name=scenario._name,
                                    target_scenario_state=[ScenarioStateType.RUNNING,
                                                           ScenarioStateType.EXECUTING,
                                                           ScenarioStateType.COMPLETED,
                                                           ScenarioStateType.INITIALIZED,
                                                           ScenarioStateType.STUCKED]):
                                time.sleep(1)
                            scenario.update()
                            break
                elif event.event_type == EventType.SCENARIO_DELETE:
                    for scenario in sel_middleware._scenario_list:
                        if scenario._name == event.name:
                            while not self.check_scenario_state(
                                    host=event.host, port=event.port, scenario_name=scenario._name,
                                    target_scenario_state=[ScenarioStateType.COMPLETED,
                                                           ScenarioStateType.INITIALIZED,
                                                           ScenarioStateType.STUCKED]):
                                time.sleep(1)
                            scenario.delete()
                            break

            if not event.name:
                event_name = ''
            else:
                event_name = event.name
            if not event.host:
                event_host = ''
            else:
                event_host = event.host
            if not event.port:
                event_port = ''
            else:
                event_port = event.port

            # if event.event_type in [EventType.MIDDLEWARE_RUN, EventType.MIDDLEWARE_KILL, EventType.THING_KILL]:
            #     SOPTEST_LOG_DEBUG(
            #         f"""[EVENT][{event.event_type.value:<{max([len(e.value) for e in EventType])}}]: {event_name:<40}|{f'{event_host}:{event_port}':<21}|{f'{"SUPER" if event.is_super else "BASIC"}':<6}|{f'{"LOCAL" if event.is_local else "REMOTE"}':<6}""", 0)
            SOPTEST_LOG_DEBUG(
                f"""[EVENT][{event.event_type.value:<{max([len(e.value) for e in EventType])}}]: {event_name:<40}|{f'{event_host}:{event_port}':<21}|{f'{"SUPER" if event.is_super else "BASIC"}':<6}|{f'{"LOCAL" if event.is_local else "REMOTE"}':<6}""", 0)

        self.wrapup()
        self.post_processing_event_log()

    def _on_message(self, client: SoPMQTTMonitor, user_data: Any, message: mqtt.MQTTMessage):
        topic, payload, timestamp = decode_MQTT_message(message)
        timestamp = time.time()
        host = client._host
        port = client._port
        level = client._level
        scenario_name = payload.get('scenario', None)
        return_type = SoPType.to_soptype(payload.get('return_type', None))
        return_value = payload.get('return_value', None)
        error_type = SoPErrorType.to_soperrortype(payload.get('error', None))

        user_data = user_data['user_data']

        sel_middleware = self.select_middleware(host=host, port=port)
        # print(f'{client._host}:{client._port}')

        if SoPProtocolType.Default.TM_REGISTER.get_prefix() in topic:
            thing_name = topic.split('/')[-1]
            self._event_log.append(EventHolder(thing_name=thing_name, middleware_name=sel_middleware._name,
                                               event_type=EventType.THING_REGISTER, level=level, timestamp=timestamp,
                                               host=host, port=port))
        elif SoPProtocolType.Default.MT_RESULT_REGISTER.get_prefix() in topic:
            thing_name = topic.split('/')[-1]

            for event in list(reversed(self._event_log)):
                if thing_name == event.thing_name and event.event_type == EventType.THING_REGISTER:
                    event.duration = timestamp - event.timestamp
                    event.result = error_type
                    SOPTEST_LOG_DEBUG(
                        f'[REGISTER] thing: {thing_name} duration: {event.duration}', 0)
                    break
        elif SoPProtocolType.Default.TM_UNREGISTER.get_prefix() in topic:
            thing_name = topic.split('/')[-1]
            self._event_log.append(EventHolder(thing_name=thing_name, middleware_name=sel_middleware._name,
                                               event_type=EventType.THING_UNREGISTER, level=level, timestamp=timestamp,
                                               host=host, port=port))
        elif SoPProtocolType.Default.MT_RESULT_UNREGISTER.get_prefix() in topic:
            thing_name = topic.split('/')[-1]

            for event in list(reversed(self._event_log)):
                if thing_name == event.thing_name and event.event_type == EventType.THING_UNREGISTER:
                    event.duration = timestamp - event.timestamp
                    event.result = error_type
                    SOPTEST_LOG_DEBUG(
                        f'[UNREGISTER] thing: {thing_name} duration: {event.duration}', 0)
                    break
        elif SoPProtocolType.Default.MT_EXECUTE.get_prefix() in topic:
            thing_name = topic.split('/')[-1]
            function_name = topic.split('/')[-2]
            energy = None

            for thing in sel_middleware._thing_list:
                for function in thing._function_list:
                    if function_name == function['name']:
                        energy = function['energy']

            self._event_log.append(EventHolder(thing_name=thing_name, function_name=function_name, middleware_name=sel_middleware._name, scenario_name=scenario_name,
                                               event_type=EventType.FUNCTION_EXECUTE, level=level, timestamp=timestamp, energy=energy,
                                               host=host, port=port))
        elif SoPProtocolType.Default.TM_RESULT_EXECUTE.get_prefix() in topic:
            thing_name = topic.split('/')[-1]
            function_name = topic.split('/')[-2]

            scenario = self.select_scenario(name=scenario_name)
            sel_thing = self.select_thing(name=thing_name)
            if not sel_thing in scenario._thing_list:
                scenario._thing_list.append(sel_thing)

            for event in list(reversed(self._event_log)):
                if thing_name == event.thing_name and function_name == event.function_name and scenario_name == event.scenario_name and event.event_type == EventType.FUNCTION_EXECUTE:
                    event.duration = timestamp - event.timestamp
                    event.result = error_type
                    event.return_type = return_type
                    event.return_value = return_value
                    SOPTEST_LOG_DEBUG(
                        f'[EXECUTE] thing: {thing_name} function: {function_name} scenario: {scenario_name} duration: {event.duration} return value:{return_value} - {return_type.value}', 0)
                    break
        elif SoPProtocolType.WebClient.EM_VERIFY_SCENARIO.get_prefix() in topic:
            self._event_log.append(EventHolder(middleware_name=sel_middleware._name, scenario_name=scenario_name,
                                               event_type=EventType.SCENARIO_VERIFY, level=level, timestamp=timestamp,
                                               result=error_type,
                                               host=host, port=port))
        elif SoPProtocolType.WebClient.ME_RESULT_VERIFY_SCENARIO.get_prefix() in topic:
            for event in list(reversed(self._event_log)):
                if scenario_name == event.scenario_name and event.event_type == EventType.SCENARIO_VERIFY:
                    event.duration = timestamp - event.timestamp
                    event.result = error_type
                    SOPTEST_LOG_DEBUG(
                        f'[SCENE_VERIFY] scenario: {scenario_name} duration: {event.duration}', 1)
                    break
        elif SoPProtocolType.WebClient.EM_ADD_SCENARIO.get_prefix() in topic:
            self._event_log.append(EventHolder(middleware_name=sel_middleware._name, scenario_name=scenario_name,
                                               event_type=EventType.SCENARIO_ADD, level=level, timestamp=timestamp,
                                               result=error_type,
                                               host=host, port=port))
        elif SoPProtocolType.WebClient.ME_RESULT_ADD_SCENARIO.get_prefix() in topic:
            for event in list(reversed(self._event_log)):
                if scenario_name == event.scenario_name and event.event_type == EventType.SCENARIO_ADD:
                    event.duration = timestamp - event.timestamp
                    event.result = error_type
                    SOPTEST_LOG_DEBUG(
                        f'[SCENE_ADD] scenario: {scenario_name} duration: {event.duration}', 1)
                    break
        elif SoPProtocolType.WebClient.EM_RUN_SCENARIO.get_prefix() in topic:
            self._event_log.append(EventHolder(middleware_name=sel_middleware._name, scenario_name=scenario_name,
                                               event_type=EventType.SCENARIO_RUN, level=level, timestamp=timestamp,
                                               result=error_type,
                                               host=host, port=port))
        elif SoPProtocolType.WebClient.ME_RESULT_RUN_SCENARIO.get_prefix() in topic:
            for event in list(reversed(self._event_log)):
                if scenario_name == event.scenario_name and event.event_type == EventType.SCENARIO_RUN:
                    event.duration = timestamp - event.timestamp
                    event.result = error_type
                    SOPTEST_LOG_DEBUG(
                        f'[SCENE_RUN] scenario: {scenario_name} duration: {event.duration}', 1)
                    break
        elif SoPProtocolType.WebClient.EM_STOP_SCENARIO.get_prefix() in topic:
            self._event_log.append(EventHolder(middleware_name=sel_middleware._name, scenario_name=scenario_name,
                                               event_type=EventType.SCENARIO_STOP, level=level, timestamp=timestamp,
                                               result=error_type,
                                               host=host, port=port))
        elif SoPProtocolType.WebClient.ME_RESULT_STOP_SCENARIO.get_prefix() in topic:
            for event in list(reversed(self._event_log)):
                if scenario_name == event.scenario_name and event.event_type == EventType.SCENARIO_STOP:
                    event.duration = timestamp - event.timestamp
                    event.result = error_type
                    SOPTEST_LOG_DEBUG(
                        f'[SCENE_STOP] scenario: {scenario_name} duration: {event.duration}', 1)
                    break
        elif SoPProtocolType.WebClient.EM_UPDATE_SCENARIO.get_prefix() in topic:
            self._event_log.append(EventHolder(middleware_name=sel_middleware._name, scenario_name=scenario_name,
                                               event_type=EventType.SCENARIO_UPDATE, level=level, timestamp=timestamp,
                                               result=error_type,
                                               host=host, port=port))
        elif SoPProtocolType.WebClient.ME_RESULT_UPDATE_SCENARIO.get_prefix() in topic:
            for event in list(reversed(self._event_log)):
                if scenario_name == event.scenario_name and event.event_type == EventType.SCENARIO_UPDATE:
                    event.duration = timestamp - event.timestamp
                    event.result = error_type
                    SOPTEST_LOG_DEBUG(
                        f'[SCENE_UPDATE] scenario: {scenario_name} duration: {event.duration}', 1)
                    break
        elif SoPProtocolType.WebClient.EM_DELETE_SCENARIO.get_prefix() in topic:
            self._event_log.append(EventHolder(middleware_name=sel_middleware._name, scenario_name=scenario_name,
                                               event_type=EventType.SCENARIO_DELETE, level=level, timestamp=timestamp,
                                               result=error_type,
                                               host=host, port=port))
        elif SoPProtocolType.WebClient.ME_RESULT_DELETE_SCENARIO.get_prefix() in topic:
            for event in list(reversed(self._event_log)):
                if scenario_name == event.scenario_name and event.event_type == EventType.SCENARIO_DELETE:
                    event.duration = timestamp - event.timestamp
                    event.result = error_type
                    SOPTEST_LOG_DEBUG(
                        f'[SCENE_DELETE] scenario: {scenario_name} duration: {event.duration}', 1)
                    break
        elif SoPProtocolType.Super.MS_SCHEDULE.get_prefix() in topic:
            requester_middleware_name = topic.split('/')[-1]
            super_middleware_name = topic.split('/')[-2]
            super_thing_name = topic.split('/')[-3]
            super_function_name = topic.split('/')[-4]

            self._event_log.append(EventHolder(thing_name=super_thing_name, function_name=super_function_name, middleware_name=super_middleware_name, requester_middleware_name=requester_middleware_name, scenario_name=scenario_name,
                                               event_type=EventType.SUPER_SCHEDULE, level=level, timestamp=timestamp,
                                               host=host, port=port))
            SOPTEST_LOG_DEBUG(
                f'[SUPER_SCHEDULE_START] super_middleware: {super_middleware_name} requester_middleware: {requester_middleware_name} super_thing: {super_thing_name} super_function: {super_function_name} scenario: {scenario_name}', 0)
        elif SoPProtocolType.Super.SM_SCHEDULE.get_prefix() in topic:
            super_thing_name = topic.split('/')[-1]
            target_middleware_name = topic.split('/')[-2]
            target_thing_name = topic.split('/')[-3]
            target_function_name = topic.split('/')[-4]

            self._event_log.append(EventHolder(thing_name=super_thing_name, target_thing_name=target_thing_name, target_function_name=target_function_name, target_middleware_name=target_middleware_name, scenario_name=scenario_name,
                                               event_type=EventType.SUB_SCHEDULE, level=level, timestamp=timestamp,
                                               host=host, port=port))
            SOPTEST_LOG_DEBUG(
                f'  [SUB_SCHEDULE_START] target_middleware: {target_middleware_name} target_thing: {target_thing_name} target_function: {target_function_name} scenario: {scenario_name}', 0)
        elif SoPProtocolType.Super.MS_RESULT_SCHEDULE.get_prefix() in topic:
            super_thing_name = topic.split('/')[-1]
            target_middleware_name = topic.split('/')[-2]
            target_thing_name = topic.split('/')[-3]
            target_function_name = topic.split('/')[-4]

            scenario = self.select_scenario(name=scenario_name)
            sel_thing = self.select_thing(name=super_thing_name)
            if not sel_thing in scenario._thing_list:
                scenario._thing_list.append(sel_thing)

            for event in list(reversed(self._event_log)):
                if super_thing_name == event.thing_name and \
                        target_function_name == event.target_function_name and \
                        target_middleware_name == event.target_middleware_name and \
                        scenario_name == event.scenario_name and \
                        event.event_type == EventType.SUB_SCHEDULE:
                    event.duration = timestamp - event.timestamp
                    event.result = error_type
                    event.return_type = return_type
                    event.return_value = return_value
                    SOPTEST_LOG_DEBUG(
                        f'  [SUB_SCHEDULE_END] target_middleware: {target_middleware_name} target_thing: {target_thing_name} target_function: {target_function_name} scenario: {scenario_name} duration: {event.duration} result: {event.result}', 0)
                    break
        elif SoPProtocolType.Super.SM_RESULT_SCHEDULE.get_prefix() in topic:
            requester_middleware_name = topic.split('/')[-1]
            super_middleware_name = topic.split('/')[-2]
            super_thing_name = topic.split('/')[-3]
            super_function_name = topic.split('/')[-4]

            scenario = self.select_scenario(name=scenario_name)
            sel_thing = self.select_thing(name=super_thing_name)
            if not sel_thing in scenario._thing_list:
                scenario._thing_list.append(sel_thing)

            for event in list(reversed(self._event_log)):
                if super_thing_name == event.thing_name and \
                        super_function_name == event.function_name and \
                        super_middleware_name == event.middleware_name and \
                        requester_middleware_name == event.requester_middleware_name and \
                        scenario_name == event.scenario_name and \
                        event.event_type == EventType.SUPER_SCHEDULE:
                    event.duration = timestamp - event.timestamp
                    event.result = error_type
                    event.return_type = return_type
                    event.return_value = return_value
                    SOPTEST_LOG_DEBUG(
                        f'[SUPER_EXECUTE_END] super_middleware: {super_middleware_name} requester_middleware: {requester_middleware_name} super_thing: {super_thing_name} super_function: {super_function_name} scenario: {scenario_name} duration: {event.duration} result: {event.result}', 0)
                    break

        ################################################################################################################################################################################################################################################

        elif SoPProtocolType.Super.MS_EXECUTE.get_prefix() in topic:
            super_function_name = topic.split('/')[-4]
            super_thing_name = topic.split('/')[-3]
            super_middleware_name = topic.split('/')[-2]
            requester_middleware_name = topic.split('/')[-1]

            self._event_log.append(EventHolder(thing_name=super_thing_name, function_name=super_function_name, middleware_name=super_middleware_name, requester_middleware_name=requester_middleware_name, scenario_name=scenario_name,
                                               event_type=EventType.SUPER_FUNCTION_EXECUTE, level=level, timestamp=timestamp,
                                               host=host, port=port))
            SOPTEST_LOG_DEBUG(
                f'[SUPER_EXECUTE_START] super_middleware: {super_middleware_name} requester_middleware: {requester_middleware_name} super_thing: {super_thing_name} super_function: {super_function_name} scenario: {scenario_name}', 0)
        elif SoPProtocolType.Super.SM_EXECUTE.get_prefix() in topic:
            super_thing_name = topic.split('/')[-1]
            target_middleware_name = topic.split('/')[-2]
            target_thing_name = topic.split('/')[-3]
            target_function_name = topic.split('/')[-4]

            self._event_log.append(EventHolder(thing_name=super_thing_name, target_middleware_name=target_middleware_name, target_thing_name=target_thing_name, target_function_name=target_function_name, scenario_name=scenario_name,
                                               event_type=EventType.SUB_FUNCTION_EXECUTE, level=level, timestamp=timestamp,
                                               host=host, port=port))
            SOPTEST_LOG_DEBUG(
                f'  [SUB_EXECUTE_START] target_middleware: {target_middleware_name} target_thing: {target_thing_name} target_function: {target_function_name} scenario: {scenario_name}', 0)
        elif SoPProtocolType.Super.MS_RESULT_EXECUTE.get_prefix() in topic:
            super_thing_name = topic.split('/')[-1]
            target_middleware_name = topic.split('/')[-2]
            target_thing_name = topic.split('/')[-3]
            target_function_name = topic.split('/')[-4]

            scenario = self.select_scenario(name=scenario_name)
            sel_thing = self.select_thing(name=super_thing_name)
            if not sel_thing in scenario._thing_list:
                scenario._thing_list.append(sel_thing)

            for event in list(reversed(self._event_log)):
                if super_thing_name == event.thing_name and \
                        target_thing_name == event.target_thing_name and \
                        target_function_name == event.target_function_name and \
                        target_middleware_name == event.target_middleware_name and \
                        scenario_name == event.scenario_name and \
                        event.event_type == EventType.SUB_FUNCTION_EXECUTE:
                    event.duration = timestamp - event.timestamp
                    event.result = error_type
                    event.return_type = return_type
                    event.return_value = return_value
                    SOPTEST_LOG_DEBUG(
                        f'  [SUB_EXECUTE_END] target_middleware: {target_middleware_name} target_thing: {target_thing_name} target_function: {target_function_name} scenario: {scenario_name} duration: {event.duration} result: {event.result} return value:{return_value} - {return_type.value}', 0)
                    break
        elif SoPProtocolType.Super.SM_RESULT_EXECUTE.get_prefix() in topic:
            requester_middleware_name = topic.split('/')[-1]
            super_middleware_name = topic.split('/')[-2]
            super_thing_name = topic.split('/')[-3]
            super_function_name = topic.split('/')[-4]

            scenario = self.select_scenario(name=scenario_name)
            sel_thing = self.select_thing(name=super_thing_name)
            if not sel_thing in scenario._thing_list:
                scenario._thing_list.append(sel_thing)

            for event in list(reversed(self._event_log)):
                if super_thing_name == event.thing_name and \
                        super_function_name == event.function_name and \
                        super_middleware_name == event.middleware_name and \
                        requester_middleware_name == event.requester_middleware_name and \
                        scenario_name == event.scenario_name and \
                        event.event_type == EventType.SUPER_FUNCTION_EXECUTE:
                    event.duration = timestamp - event.timestamp
                    event.result = error_type
                    event.return_type = return_type
                    event.return_value = return_value
                    SOPTEST_LOG_DEBUG(
                        f'[SUPER_EXECUTE_END] super_middleware: {super_middleware_name} requester_middleware: {requester_middleware_name} super_thing: {super_thing_name} super_function: {super_function_name} scenario: {scenario_name} duration: {event.duration} result: {event.result} return value:{return_value} - {return_type.value}', 0)
                    break
        # elif SoPProtocolType.Default.TM_VALUE_PUBLISH.get_prefix() in topic:
        #     pass
        # elif SoPProtocolType.Default.TM_VALUE_PUBLISH_OLD.get_prefix() in topic:
        #     pass

    # ====================================
    #    _____  _                  _
    #   / ____|| |                | |
    #  | |     | |__    ___   ___ | | __
    #  | |     | '_ \  / _ \ / __|| |/ /
    #  | |____ | | | ||  __/| (__ |   <
    #   \_____||_| |_| \___| \___||_|\_\
    # ====================================

    @exception_wrapper
    def check_pc_service_list(self, host: str = None, port: int = None, timeout: int = 10):
        sel_mqtt_monitor_client = self.select_middleware(
            host=host, port=port).get_mqtt_monitor_client()
        topic, payload, timestamp = sel_mqtt_monitor_client.expect(
            SoPProtocolType.Super.PC_SERVICE_LIST.value % ('#'), timeout=timeout)
        if payload is not None:
            SOPTEST_LOG_DEBUG(
                f'Service list packet detected!', 0)
            return True
        else:
            SOPTEST_LOG_DEBUG('get service list failed...', -1)
            return False

    @exception_wrapper
    def check_thing_exist(self, host: str = None, port: int = None, thing_name: str = None, is_super: bool = False, timeout: int = 10):
        sel_mqtt_monitor_client = self.select_middleware(
            host=host, port=port).get_mqtt_monitor_client()
        topic, payload, timestamp = sel_mqtt_monitor_client.publish_and_expect(
            encode_MQTT_message(
                SoPProtocolType.WebClient.EM_REFRESH.value % sel_mqtt_monitor_client._client_id, f'{{}}'),
            SoPProtocolType.WebClient.ME_RESULT_SERVICE_LIST.value % (sel_mqtt_monitor_client._client_id), timeout=timeout)
        if payload is not None:
            service_list = payload['services']
            for service in service_list:
                thing_list = service['things']
                for thing in thing_list:
                    if thing_name == thing['id'] and is_super == bool(thing['is_super']):
                        thing_name_prefix = 'Super ' if is_super else ''
                        SOPTEST_LOG_DEBUG(
                            f'{thing_name_prefix}Thing {thing_name} detected at {sel_mqtt_monitor_client._client_id}!', 0)
                        return True
            else:
                SOPTEST_LOG_DEBUG(
                    f'Thing {thing_name} not exist!', -1)
                return False
        else:
            raise SOPTEST_LOG_DEBUG('get thing list failed...', -1)

    @exception_wrapper
    def check_scenario_state(self, host: str = None, port: int = None, scenario_name: str = None, target_scenario_state: List[ScenarioStateType] = None, timeout: int = 10):
        scenario_state = self.get_scenario_state(
            host=host, port=port, scenario=scenario_name, timeout=timeout)

        if scenario_state in target_scenario_state:
            SOPTEST_LOG_DEBUG(
                f'scenario state matched! -- scenario: {scenario_name}, state: {scenario_state.value}', 0)
            return scenario_state
        elif not target_scenario_state:
            SOPTEST_LOG_DEBUG(
                f'scenario {scenario_name} state is {scenario_state.value}', 0)
            return scenario_state
        else:
            SOPTEST_LOG_DEBUG(
                f'scenario state not matched! -- scenario: {scenario_name}, state: {scenario_state.value}', 0)
            return False

    @exception_wrapper
    def check_scenario_ready(self, host: str = None, port: int = None, scenario_name: str = None, stuck_handling: bool = True, timeout: int = 10):
        sel_middleware = self.select_middleware(host=host, port=port)
        scenario_state = self.get_scenario_state(
            host=host, port=port, scenario=scenario_name, timeout=timeout)

        if scenario_state in [ScenarioStateType.INITIALIZED, ScenarioStateType.COMPLETED]:
            SOPTEST_LOG_DEBUG(
                f'scenario {scenario_name} is {scenario_state.value}...', 1)
            return True
        elif scenario_state in [ScenarioStateType.STUCKED]:
            if stuck_handling:
                SOPTEST_LOG_DEBUG(
                    f'scenario {scenario_name} is STUCKED... try to update scenario', 1)
                for scenario in sel_middleware._scenario_list:
                    if scenario._name == scenario_name and scenario_state == ScenarioStateType.STUCKED:
                        if scenario.update():
                            return True
                        else:
                            return False
            else:
                SOPTEST_LOG_DEBUG(
                    f'scenario {scenario_name} is STUCKED... but skip to update scenario', 1)
        else:
            SOPTEST_LOG_DEBUG(
                f'scenario {scenario_name} is not ready -- state: {scenario_state.value}', 1)
            return False

    # ========================
    #         _    _  _
    #        | |  (_)| |
    #  _   _ | |_  _ | | ___
    # | | | || __|| || |/ __|
    # | |_| || |_ | || |\__ \
    #  \__,_| \__||_||_||___/
    # ========================

    @exception_wrapper
    def get_scenario_state(self, host: str = None, port: int = None, scenario: str = None, timeout: int = 10) -> ScenarioStateType:
        target_scenario_info = self.find_scenario(
            host=host, port=port, scenario=scenario, timeout=timeout)
        return target_scenario_info['state']

    @exception_wrapper
    def find_scenario(self, host: str = None, port: int = None, scenario: str = None, timeout: int = 10):
        sel_mqtt_monitor_client = self.select_middleware(
            host=host, port=port).get_mqtt_monitor_client()
        topic, payload, timestamp = sel_mqtt_monitor_client.publish_and_expect(encode_MQTT_message(SoPProtocolType.WebClient.EM_REFRESH.value % sel_mqtt_monitor_client._client_id, f'{{}}'),
                                                                               SoPProtocolType.WebClient.ME_RESULT_SCENARIO_LIST.value % sel_mqtt_monitor_client._client_id, timeout=timeout)
        for scenario_info in payload['scenarios']:
            if scenario_info['name'] == scenario:
                return dict(id=scenario_info['id'], name=scenario_info['name'], code=scenario_info['contents'],
                            state=ScenarioStateType.get(scenario_info['state']), schedule_info=scenario_info['scheduleInfo'])
        else:
            SOPTEST_LOG_DEBUG(
                f'Scenario {scenario} not found...', -1)
            return False

    def select_middleware(self, host: str = None, port: int = None, name: str = None) -> SoPMiddlewareElement:
        for middleware in self._middleware_list:
            if (host == middleware._host and port == middleware._port) or name == middleware._name:
                return middleware

    def select_scenario(self, middleware: SoPMiddlewareElement = None, name: str = None) -> SoPScenarioElement:
        if middleware:
            for scenario in middleware._scenario_list:
                if name == scenario._name:
                    return scenario
        else:
            for middleware in self._middleware_list:
                for scenario in middleware._scenario_list:
                    if name == scenario._name:
                        return scenario

    def select_thing(self, middleware: SoPMiddlewareElement = None, name: str = None) -> SoPThingElement:
        if middleware:
            for thing in middleware._thing_list:
                if name == thing._name:
                    return thing
        else:
            for middleware in self._middleware_list:
                for thing in middleware._thing_list:
                    if name == thing._name:
                        return thing

    def user_data_set(self, sel_mqtt_monitor_client: SoPMQTTMonitor, user_data):
        self._user_data['user_data'] = user_data
        sel_mqtt_monitor_client._client.user_data_set(self._user_data)

    def get_function_energy_list(self, function_name: str):
        function_energy_list = []
        for middleware in self._middleware_list:
            for thing in middleware._thing_list:
                for function in thing._function_list:
                    if function['name'] == function_name:
                        function_energy_list.append(
                            function['energy'])
        function_energy_list = sorted(
            function_energy_list, reverse=True)
        return function_energy_list

    def calculate_utilization(self):
        total_simulation_time = self._event_log[-1].timestamp - \
            self._event_log[0].timestamp

        for middleware in self._middleware_list:
            for event in middleware._event_log:
                if event.event_type in [EventType.FUNCTION_EXECUTE, EventType.SUPER_FUNCTION_EXECUTE]:
                    if event.function_name not in middleware._service_utilization_info:
                        middleware._service_utilization_info[event.function_name] = 0
                    if event.duration:
                        middleware._service_utilization_info[event.function_name] += event.duration

                    if event.thing_name not in middleware._thing_utilization_info:
                        middleware._thing_utilization_info[event.thing_name] = 0
                    if event.duration:
                        middleware._thing_utilization_info[event.thing_name] += event.duration
        for middleware in self._middleware_list:
            for k, i in middleware._service_utilization_info.items():
                middleware._service_utilization_info[k] /= total_simulation_time
            for k, i in middleware._thing_utilization_info.items():
                middleware._thing_utilization_info[k] /= total_simulation_time

    def calculate_energy_score(self):
        function_energy_info = {}
        for middleware in self._middleware_list:
            for thing in middleware._thing_list:
                for function in thing._function_list:
                    if function['name'] not in function_energy_info:
                        function_energy_info[function['name']] = [
                            function['energy'], ]
                    else:
                        function_energy_info[function['name']].append(
                            function['energy'])

            score = 0
            cnt = 0
            for event in middleware._event_log:
                if event.function_name in function_energy_info:
                    energy_list = sorted(
                        function_energy_info[event.function_name])
                    for i, energy in enumerate(energy_list):
                        if energy == event.energy:
                            energy_score = 100 / (i + 1)
                            score += energy_score
                            cnt += 1
            middleware._energy_score = score / cnt

    def calculate_qos_score(self):
        for middleware in self._middleware_list:
            cnt = 0
            execute_event_list = [
                event for event in middleware._event_log if event.event_type == EventType.FUNCTION_EXECUTE]
            for event in execute_event_list:
                if event.result == SoPErrorType.NO_ERROR:
                    cnt += 1
            middleware._qos_score = (cnt / len(execute_event_list)) * 100.0

    def calculate_scenario_cycle_avg(self):
        for middleware in self._middleware_list:
            loop_period_list: List[float] = []
            for scenario in middleware._scenario_list:
                # capture execute pattern
                start_index = 0
                for i, event in enumerate(scenario._event_log):
                    if event.event_type == EventType.SCENARIO_RUN:
                        start_index = i
                tmp_event_list: List[EventHolder] = []
                for event in scenario._event_log[start_index+1:]:
                    if event.event_type in [EventType.FUNCTION_EXECUTE, EventType.SUPER_FUNCTION_EXECUTE]:
                        tmp_event_list.append(event)
                prev_event = tmp_event_list[0]
                for event in tmp_event_list:
                    if event.function_name == tmp_event_list[0].function_name:
                        loop_period_list.append(
                            event.timestamp - prev_event.timestamp)
                        prev_event = event
                loop_period_list = loop_period_list[1:]

                scenario._avg_loop_period = sum(
                    loop_period_list)/len(loop_period_list)
                for loop_period in loop_period_list:
                    if abs(loop_period - scenario._period) < scenario._period * 0.1:
                        scenario._loop_check = True
                    else:
                        scenario._loop_check = False
                        break

    def post_processing_event_log(self):
        for event in self._event_log:
            event.timestamp -= self._simulation_start_time
            if event.event_type in [EventType.MIDDLEWARE_RUN,
                                    EventType.MIDDLEWARE_KILL,
                                    EventType.THING_REGISTER,
                                    EventType.THING_UNREGISTER,
                                    EventType.THING_KILL,
                                    EventType.FUNCTION_EXECUTE,
                                    EventType.SCENARIO_VERIFY,
                                    EventType.SCENARIO_ADD,
                                    EventType.SCENARIO_RUN,
                                    EventType.SCENARIO_STOP,
                                    EventType.SCENARIO_UPDATE,
                                    EventType.SCENARIO_DELETE]:
                middleware = self.select_middleware(
                    event.host, event.port, event.middleware_name)
                middleware._event_log.append(event)

                for thing in middleware._thing_list:
                    if event.event_type in [EventType.THING_REGISTER,
                                            EventType.THING_UNREGISTER,
                                            EventType.THING_KILL,
                                            EventType.FUNCTION_EXECUTE]:
                        thing._event_log.append(event)

                for scenario in middleware._scenario_list:
                    if event.event_type in [EventType.THING_REGISTER,
                                            EventType.THING_UNREGISTER,
                                            EventType.THING_KILL,
                                            EventType.FUNCTION_EXECUTE,
                                            EventType.SCENARIO_VERIFY,
                                            EventType.SCENARIO_ADD,
                                            EventType.SCENARIO_RUN,
                                            EventType.SCENARIO_STOP,
                                            EventType.SCENARIO_UPDATE,
                                            EventType.SCENARIO_DELETE]:
                        scenario._event_log.append(event)

        # service, thing utilization
        self.calculate_utilization()
        self.calculate_scenario_cycle_avg()
        self.calculate_energy_score()
        self.calculate_qos_score()

    def convert_return_type(self, return_type):
        if return_type.value == -1:
            return_type = 'UNDEFINED'
        else:
            return_type = return_type
        return return_type

    def convert_execute_result(self, execute_result):
        if execute_result.value == 0:
            return 'NO_ERROR'
        elif execute_result.value == -1:
            return 'FAILED'
        elif execute_result.value == -2:
            return 'TIMEOUT'
        elif execute_result.value == -3:
            return 'NO_PARALLEL'
        elif execute_result.value == -4:
            return 'DUPLICATE'
        elif execute_result.value == -5:
            return 'UNDEFINED'

    def print_table(self, table, header, scenario_name: str = None):
        title_filler = '-'
        table = tabulate(table, headers=header, tablefmt='fancy_grid')

        if scenario_name:
            print(
                f"{f' scenario {scenario_name} ':{title_filler}^{len(table.split()[0])}}")
        print(table)

    @ exception_wrapper
    def print_simulation_result(self, target_middleware: SoPMiddlewareElement):
        while True:
            print()
            print('0: Middleware score\n'
                  '1: Thing Utilization\n'
                  '2: Service Utilization\n'
                  '3: Scenario Score\n'
                  '4: Whole Timeline\n')
            user_input = input('Select Menu (\'q\' for exit menu): ')

            if user_input == 'q' or not user_input.isdigit():
                break

            user_input = int(user_input)

            if user_input == 0:
                # print middleware score
                print(f'== Middleware {target_middleware._name} Score == ')
                header = ['energy_score', 'qos_score']
                table = []
                for scenario in target_middleware._scenario_list:
                    table.append([target_middleware._energy_score,
                                  target_middleware._qos_score])
                    self.print_table(table, header)
            elif user_input == 1:
                # print thing utilization
                print(f'== Thing Utilization ==')
                header = ['thing', 'utilization']
                table = []
                for k, i in target_middleware._thing_utilization_info.items():
                    table.append([k, f'{i * 100:.2f}%'])
                self.print_table(table, header)
            elif user_input == 2:
                # print service utilization
                print(f'== Service Utilization ==')
                header = ['service', 'utilization']
                table = []
                for k, i in target_middleware._service_utilization_info.items():
                    table.append([k, f'{i * 100:.2f}%'])
                self.print_table(table, header)
            elif user_input == 3:
                # print scenario score
                print(f'== Scenario Score ==')
                header = ['scenario', 'avg latency', 'cycle check']
                table = []
                for scenario in target_middleware._scenario_list:
                    table.append(
                        [scenario._name, f'{scenario._avg_loop_period:.4f}s', scenario._loop_check])
                    self.print_table(table, header)
            elif user_input == 4:
                # print scenario timeline
                print(f'== Whole Timeline ==')
                header = ['time', 'duration', 'event_type', 'level', 'middleware',
                          'thing', 'service', 'scenario', 'result', 'return_value', 'return_type']
                table = []
                for event in target_middleware._event_log:
                    if event.event_type == EventType.FUNCTION_EXECUTE and not event.duration:
                        continue
                    table.append([event.timestamp, event.duration, event.event_type.value, event.level, event.middleware_name,
                                  event.thing_name, event.function_name, event.scenario_name, self.convert_execute_result(event.result), event.return_value, self.convert_return_type(event.return_type)])
                self.print_table(table, header)


if __name__ == '__main__':
    pass
