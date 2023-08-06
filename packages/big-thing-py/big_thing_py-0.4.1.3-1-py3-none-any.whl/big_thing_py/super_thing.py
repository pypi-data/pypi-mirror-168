
from big_thing import *
from super import *

import random


class SoPSuperThing(SoPBigThing):

    class ServiceTable:
        value_list: List[SoPServiceInfo] = []
        function_list: List[SoPServiceInfo] = []

    def __init__(self, name: str = None, service_list: List[SoPService] = [], alive_cycle: float = 60, is_super: bool = False, is_parallel: bool = True,
                 ip: str = None, port: int = None, ssl_ca_path: str = None, ssl_enable: bool = None, log_enable: bool = True, append_mac_address: bool = True,
                 refresh_cycle: float = 10):
        super().__init__(name=name, service_list=service_list, alive_cycle=alive_cycle, is_super=is_super,
                         is_parallel=is_parallel, ip=ip, port=port, ssl_ca_path=ssl_ca_path, ssl_enable=ssl_enable, append_mac_address=append_mac_address, log_enable=log_enable)

        self._hierarchical_service_table = SoPSuperThing.ServiceTable()

        self._last_refresh_time: float = 0
        self._last_available_send_time: float = 0
        self._refresh_cycle: float = refresh_cycle
        self._available_cycle: float = refresh_cycle / 2

        self._function_list: List[SoPSuperFunction] = self._function_list

        self._schedule_waiting_list: List[str] = []
        # key = f'{super_function_name}_{thing_name}_{middleware_name}_{super_thing_name}_{scenario_name}'
        # value = {
        #     'tag_list': [subfunction_tag_list],
        #     'subscribe_topic': subscribe_topic
        # }
        self._schedule_waiting_device_hash: Dict[str, Dict[str, Union[list, str]]] = {
        }

        # key = f'{super_function_name}_{thing_name}_{middleware_name}_{super_thing_name}_{scenario_name}'
        # value = {
        #     'tag_list': [subfunction_tag_list],
        #     'subscribe_topic': subscribe_topic
        # }
        self._super_execute_waiting_hash: Dict[str, Dict[str, Union[list, str]]] = {
        }

        # key = f'{subfunction_name}_{super_function_name}_{requester_middleware_name}_{scenario_name}'
        # value = [
        #     {
        #         'thing_name': thing_name,
        #         'middleware_name': middleware_name
        #     }, ...
        # ]
        self._service_mapping_table: Dict[str, List[Dict[str, str]]] = {}

        # Queue
        self._super_execute_queue: Queue = Queue()
        self._schedule_queue: Queue = Queue()

        self._thread_func_list += [
            self.refresh_thread_func,
            self.available_thread_func
        ]

        self.extract_subfunction_info()

    # override
    def setup(self, avahi_enable=True):
        self.extract_subfunction_info()
        return super().setup(avahi_enable)

    # ===========================================================================================
    #  _    _                             _    __                      _    _
    # | |  | |                           | |  / _|                    | |  (_)
    # | |_ | |__   _ __   ___   __ _   __| | | |_  _   _  _ __    ___ | |_  _   ___   _ __   ___
    # | __|| '_ \ | '__| / _ \ / _` | / _` | |  _|| | | || '_ \  / __|| __|| | / _ \ | '_ \ / __|
    # | |_ | | | || |   |  __/| (_| || (_| | | |  | |_| || | | || (__ | |_ | || (_) || | | |\__ \
    #  \__||_| |_||_|    \___| \__,_| \__,_| |_|   \__,_||_| |_| \___| \__||_| \___/ |_| |_||___/
    # ===========================================================================================

    def refresh_thread_func(self, stop_event: Event):
        while not self._registered:
            time.sleep(THREAD_TIME_OUT)

        try:
            while not stop_event.wait(THREAD_TIME_OUT):
                if (get_current_time() - self._last_refresh_time) > self._refresh_cycle:
                    self.send_SM_REFRESH()
                    time.sleep(self._refresh_cycle / 2)

        except Exception as e:
            stop_event.set()
            print_error(e)
            return False

    def available_thread_func(self, stop_event: Event):
        while not self._registered:
            time.sleep(THREAD_TIME_OUT)

        try:
            while not stop_event.wait(THREAD_TIME_OUT):
                if (get_current_time() - self._last_available_send_time) > self._available_cycle:
                    self.send_SM_AVAILABILITY()
                    time.sleep(self._available_cycle / 2)

        except Exception as e:
            stop_event.set()
            print_error(e)
            return False

    # Whole super function structure
    # super_thing -- super_function1 -- subfunction1 ---- subfunction1(target Thing3, target Middleware1)
    #            |                  |                \
    #            |                  |                 \-- subfunction1(target Thing2, target Middleware3)
    #            |                  |                  \
    #            |                  |                   \ subfunction1(target Thing4, target Middleware7)
    #            |                  |                    \
    #            |                  |-- subfunction2      \ ....
    #            |                  |
    #            |                  |-- ...
    #            |
    #            |
    #            |-- super_function2 -- subfunction1(target Thing1, target Middleware2)
    def schedule_thread_func(self, schedule_request: ScheduleRequest):

        def schedule_wait_target_device_list_by_policy(exist_hierarchy_subfunction_list: List[SoPServiceInfo],
                                                       subfunction_policy: SoPPolicy) -> List[SoPServiceInfo]:
            if subfunction_policy == SoPPolicy.ALL:
                scheduled_subfunction_list = exist_hierarchy_subfunction_list
            elif subfunction_policy == SoPPolicy.SINGLE:
                random_selected_function_service = random.choice(
                    exist_hierarchy_subfunction_list)
                scheduled_subfunction_list = [
                    random_selected_function_service]
            else:
                raise Exception(
                    f'not supported policy... skip schedule: {subfunction_policy}')

            return scheduled_subfunction_list

        try:
            super_function_name, \
                super_thing_name, \
                super_middleware_name, \
                requester_middleware_name, \
                scenario_name, \
                period = schedule_request.unpack()

            schedule_request_key = self.make_schedule_request_key(super_function_name,
                                                                  super_thing_name,
                                                                  super_middleware_name,
                                                                  requester_middleware_name,
                                                                  scenario_name)

            # target super function -- subfunction 1 -- target Thing device 1
            #                       \                \_ target Thing device 2
            #                        \ subfunction 2 -- target Thing device 3
            #                        |               \_ target Thing device 4
            #                        \- subfunction 3 - target Thing device 5

            # find target super function from self function list
            target_super_function = self.search_service(
                src_service_list=self._function_list,
                target_service_name=super_function_name)
            target_super_function = target_super_function[0] if len(
                target_super_function) == 1 else target_super_function

            # request schedule for each target super function's subfunction
            SOPLOG_DEBUG(
                f'[SCHEDULE RUN] super function {super_function_name} scheduling start', 'green')
            for subfunction in target_super_function.get_subfunction_list():
                subfunction_name = subfunction.get_name()
                subfunction_tag_list = subfunction.get_tag_list()
                subfunction_policy = subfunction.get_policy()

                # find target Thing device from hierarchy service tree(middleware tree)
                target_device_list = self.search_service(
                    self._hierarchical_service_table.function_list,
                    target_service_name=subfunction_name,
                    target_tags_list=subfunction_tag_list)
                target_device_list = schedule_wait_target_device_list_by_policy(
                    target_device_list, subfunction_policy)

                # target_device was not exist, skip schedule
                if not target_device_list:
                    schedule_result = ScheduleResult(super_function_name,
                                                     super_thing_name,
                                                     super_middleware_name,
                                                     requester_middleware_name,
                                                     super_thing_name,
                                                     SoPErrorType.EXECUTE_FAIL,
                                                     scenario_name)
                    self.send_SM_RESULT_SCHEDULE(schedule_result)
                    raise Exception(
                        f'no target device found for subfunction {subfunction_name}... skip schedule')

                # request schedule for each subfunction's target Thing device
                SOPLOG_DEBUG(
                    f'....[SUBSCHEDULE RUN] subfunction {subfunction_name} scheduling start', 'green')

                schedule_success = False
                retry = 2
                while not schedule_success and retry:
                    subfunction_target_device_mapping_list = []
                    for target_subfunction in target_device_list:
                        target_subfunction_name = target_subfunction.get_name()
                        target_middleware_name = target_subfunction.get_middleware_name()
                        target_thing_name = target_subfunction.get_thing_name()

                        subfunction_schedule_result_topic = SoPProtocolType.Super.MS_RESULT_SCHEDULE.value % (
                            target_subfunction_name, target_thing_name, target_middleware_name, super_thing_name
                        )
                        schedule_request_device_key = self.make_schedule_request_device_key(
                            target_subfunction_name,
                            target_thing_name,
                            target_middleware_name,
                            self._name,
                            scenario_name)
                        schedule_result_queue = Queue()
                        schedule_request_device_value = self.make_schedule_request_device_value(
                            subfunction_tag_list,
                            subfunction_schedule_result_topic,
                            requester_middleware_name,
                            super_function_name,
                            schedule_result_queue
                        )

                        if schedule_request_device_key not in self._schedule_waiting_device_hash:
                            self._schedule_waiting_device_hash[schedule_request_device_key] = schedule_request_device_value
                        else:
                            raise Exception(
                                f'duplicated key... schedule request already exist, key: {schedule_request_device_key}')

                        # send schedule request to tatget Thing device via middleware tree
                        self._subscribe(subfunction_schedule_result_topic)
                        self.send_SM_SCHEDULE(target_subfunction_name,
                                              target_thing_name,
                                              target_middleware_name,
                                              super_thing_name,
                                              scenario_name,
                                              period)
                        SOPLOG_DEBUG(
                            f'........[SCHEDULE TARGET RUN] subfunction {subfunction_name} target Thing:{target_thing_name}, Middleware:{target_middleware_name} scheduling request sent', 'green')
                        try:
                            schedule_result = schedule_result_queue.get(
                                timeout=60)
                        except Exception:
                            raise Exception(
                                'schedule request timeout... skip schedule')
                        finally:
                            self._unsubscribe(
                                subfunction_schedule_result_topic)

                        result_scenario_name = schedule_result['scenario_name']
                        try:
                            error = SoPErrorType(schedule_result['error'])
                        except ValueError as e:
                            error = SoPErrorType(int(schedule_result['error']))

                        # send schedule result was come with error=0 mean schedule success
                        if error == SoPErrorType.NO_ERROR:
                            super_service_mapping_value = self.make_super_service_mapping_value(
                                target_thing_name,
                                target_middleware_name,
                                super_thing_name,
                                super_function_name,
                                scenario_name)
                            subfunction_target_device_mapping_list.append(
                                super_service_mapping_value)
                            SOPLOG_DEBUG(
                                f'........[SCHEDULE TARGET END] subfunction {subfunction_name} target Thing:{target_thing_name}, Middleware:{target_middleware_name} scheduling result received!!!', 'green')
                        # if sceanrio name was not match, skip schedule
                        elif not result_scenario_name == scenario_name:
                            schedule_result = ScheduleResult(super_function_name,
                                                             super_thing_name,
                                                             target_middleware_name,
                                                             requester_middleware_name,
                                                             super_thing_name,
                                                             SoPErrorType.NO_ERROR,
                                                             scenario_name)
                            self.send_SM_RESULT_SCHEDULE(schedule_result)
                            raise Exception(f'''[schedule_thread_func] scenario name mismatch... skip schedule'
                                            recv scenario={result_scenario_name}
                                            target scenario={scenario_name}''')
                        # error was not NO_ERROR, go to next target device
                        else:
                            SOPLOG_DEBUG(f'''[schedule_thread_func] schedule failed for 
                                middleware | {target_middleware_name} 
                                thing      | {target_thing_name} 
                                go to next target...''', 'yellow')
                    else:
                        super_service_mapping_key = self.make_super_service_mapping_key(
                            subfunction_name,
                            super_function_name,
                            requester_middleware_name,
                            scenario_name)

                        if super_service_mapping_key in self._service_mapping_table:
                            SOPLOG_DEBUG(
                                f'Update service mapping table... key: {super_service_mapping_key}', 'cyan')

                        self._service_mapping_table[super_service_mapping_key] = subfunction_target_device_mapping_list
                        schedule_success = True
                else:
                    SOPLOG_DEBUG(
                        f'''....[SUBSCHEDULE END] subfunction {subfunction_name} scheduling success!!!
                                super_function_name    | {super_function_name}
                                subfunction_name       | {subfunction_name}
                                subfunction_tag_list   | {
                                    [tag.get_name() for tag in subfunction_tag_list]}
                                subfunction_policy     | {subfunction_policy}''', 'green')
                    pass

            SOPLOG_DEBUG(
                f'[SCHEDULE END] super function {super_function_name} scheduling success!!!', 'green')
            schedule_result = ScheduleResult(super_function_name,
                                             super_thing_name,
                                             super_middleware_name,
                                             requester_middleware_name,
                                             super_thing_name,
                                             SoPErrorType.NO_ERROR,
                                             scenario_name)
            self.send_SM_RESULT_SCHEDULE(schedule_result)
            self._schedule_waiting_list.remove(schedule_request_key)
            return True
        except Exception as e:
            print_error(e)
            SOPLOG_DEBUG(
                '[schedule_thread_func] schedule failed because of some error... find it!!!', 'red')
            self._schedule_waiting_list.remove(schedule_request_key)
            return False

    def super_execute_thread_func(self, stop_event: Event):
        try:
            while not stop_event.wait(THREAD_TIME_OUT):
                if self._super_execute_queue.empty():
                    continue
                function_execute_info = self._super_execute_queue.get()

                target_thing = function_execute_info['target_thing']
                target_function = function_execute_info['target_function']

                if self._name != target_thing:
                    continue
                for function in self._function_list:
                    function_name = function.get_name()
                    if function_name == target_function:
                        if self._is_parallel or not function.get_running():
                            function.execute(function_execute_info)
                        else:
                            SOPLOG_DEBUG(colored(
                                f'super function {function_name} is busy', 'yellow'))
                            self._super_execute_queue.put(
                                function_execute_info)
                        break
                else:
                    SOPLOG_DEBUG(colored('function not exist', 'red'))
        except Exception as e:
            stop_event.set()
            print_error(e)
            return False

    def super_function_execute_result_thread_func(self, stop_event: Event):
        try:
            while not stop_event.wait(THREAD_TIME_OUT):
                if self._super_function_execute_result_queue.empty():
                    continue
                execute_result = self._super_function_execute_result_queue.get()

                function_name = execute_result['function_name']
                thing_name = execute_result['thing_name']
                super_middleware_name = execute_result['middleware_name']
                requester_middleware_name = execute_result['requester_middleware_name']
                error = execute_result['error']
                scenario_name = execute_result['scenario']
                return_type = execute_result['return_type']
                return_value = execute_result['return_value']

                self.send_SM_RESULT_EXECUTE(
                    function_name, thing_name, super_middleware_name, requester_middleware_name, error, scenario_name, return_type, return_value)
        except Exception as e:
            stop_event.set()
            print_error(e)
            return False

    # ====================================================================================================================
    #  _                        _  _        ___  ___ _____  _____  _____
    # | |                      | || |       |  \/  ||  _  ||_   _||_   _|
    # | |__    __ _  _ __    __| || |  ___  | .  . || | | |  | |    | |    _ __ ___    ___  ___  ___   __ _   __ _   ___
    # | '_ \  / _` || '_ \  / _` || | / _ \ | |\/| || | | |  | |    | |   | '_ ` _ \  / _ \/ __|/ __| / _` | / _` | / _ \
    # | | | || (_| || | | || (_| || ||  __/ | |  | |\ \/' /  | |    | |   | | | | | ||  __/\__ \\__ \| (_| || (_| ||  __/
    # |_| |_| \__,_||_| |_| \__,_||_| \___| \_|  |_/ \_/\_\  \_/    \_/   |_| |_| |_| \___||___/|___/ \__,_| \__, | \___|
    #                                                                                                         __/ |
    #                                                                                                        |___/
    # ====================================================================================================================

    def handle_mqtt_message(self, msg: mqtt.MQTTMessage) -> None:
        topic, payload, timestamp = unpack_mqtt_message(msg)

        if super().handle_mqtt_message(msg):
            return True
        else:
            if topic[0] == 'MS':
                if topic[1] == 'RESULT':
                    if topic[2] == 'SCHEDULE':
                        self.handle_MS_RESULT_SCHEDULE(msg)
                    elif topic[2] == 'EXECUTE':
                        self.handle_MS_RESULT_EXECUTE(msg)
                    elif topic[2] == 'SERVICE_LIST':
                        self.handle_MS_RESULT_SERVICE_LIST(msg)
                    else:
                        SOPLOG_DEBUG(
                            '[handle_mqtt_message] Unexpected MS_RESULT topic!')
                elif topic[1] == 'SCHEDULE':
                    self.handle_MS_SCHEDULE(msg)
                elif topic[1] == 'EXECUTE':
                    self.handle_MS_EXECUTE(msg)
                else:
                    SOPLOG_DEBUG('[handle_mqtt_message] Unexpected MS topic!')
            elif topic[0] == 'ME':
                if topic[1] == 'NOTIFY_CHANGE':
                    self.handle_ME_NOTIFY(msg)
                else:
                    SOPLOG_DEBUG('[handle_mqtt_message] Unexpected ME topic!')
            else:
                SOPLOG_DEBUG('[handle_mqtt_message] Unexpected topic!')

    def send_mqtt_message(self, msg: Union[mqtt.MQTTMessage, ExecuteResult, SuperExecuteResult, ScheduleResult]) -> None:
        if type(msg) == SuperExecuteResult:
            self.send_SM_RESULT_EXECUTE(msg)
        elif type(msg) == ScheduleResult:
            self.send_SM_RESULT_SCHEDULE(msg)
        elif super().send_mqtt_message(msg):
            return True
        else:
            raise Exception('[send_mqtt_message] Unexpected message type!')

    # ================
    # ___  ___ _____
    # |  \/  |/  ___|
    # | .  . |\ `--.
    # | |\/| | `--. \
    # | |  | |/\__/ /
    # \_|  |_/\____/
    # ================

    # MS/SCHEDULE/[SuperFunctionName]/[SuperThingName]/[MiddlewareName]/[RequesterMWName]
    def handle_MS_SCHEDULE(self, msg: mqtt.MQTTMessage):
        topic, payload, timestamp = unpack_mqtt_message(msg)

        super_function_name = topic[2]
        super_thing_name = topic[3]
        super_middleware_name = topic[4]
        requester_middleware_name = topic[5]

        scenario_name = payload['scenario']
        period = int(payload['period'])

        schedule_request = ScheduleRequest(
            super_function_name, super_thing_name, super_middleware_name, requester_middleware_name, scenario_name, period)

        for function in self._function_list:
            function_name = function.get_name()
            if function_name == super_function_name:
                self.schedule(schedule_request)
                return True
        else:
            SOPLOG_DEBUG('function not exist', 'red')
            return False

    def handle_MS_EXECUTE(self, msg: mqtt.MQTTMessage):
        topic, payload, timestamp = unpack_mqtt_message(msg)

        target_super_function_name = topic[2]
        target_super_thing_name = topic[3]
        target_super_middleware_name = topic[4]
        requester_middleware_name = topic[5]

        scenario_name = payload['scenario']
        arg_list = payload['arguments']

        if scenario_name not in self._running_scenario_hash:
            self._running_scenario_hash[scenario_name] = []
        self._running_scenario_hash[scenario_name].append(
            {
                'target_super_function_name': target_super_function_name,
                'requester_middleware_name': requester_middleware_name
            })

        # TODO: complete this
        execute_request = SuperExecuteRequest(target_super_function_name, target_super_thing_name, target_super_middleware_name, requester_middleware_name,
                                              None, self._name, arg_list,
                                              scenario_name=scenario_name, is_parallel=True)
        execute_request.set_user_data(self._running_scenario_hash)

        target_super_function = self.search_service(
            self._function_list, target_super_function_name)
        target_super_function = target_super_function[0] if len(
            target_super_function) == 1 else target_super_function
        try:
            target_super_function.execute(execute_request)
        except Exception:
            SOPLOG_DEBUG('function not exist', 'red')
            return False

    def handle_MS_RESULT_SCHEDULE(self, msg: mqtt.MQTTMessage):
        topic, payload, timestamp = unpack_mqtt_message(msg)

        # MS/RESULT/SCHEDULE/[FunctionName]/[ThingName]/[MiddlewareName]/[SuperThingName]
        target_subfunction_name = topic[3]
        target_thing_name = topic[4]
        target_middleware_name = topic[5]
        super_thing_name = topic[6]
        try:
            error = SoPErrorType(payload['error'])
        except ValueError as e:
            error = SoPErrorType(int(payload['error']))
        scenario_name = payload['scenario']

        waiting_schedule_key = self.make_schedule_request_device_key(
            target_subfunction_name,
            target_thing_name,
            target_middleware_name,
            super_thing_name,
            scenario_name)
        schedule_result_value = self.make_schedule_result_value(
            error, scenario_name)

        if waiting_schedule_key in self._schedule_waiting_device_hash:
            waiting_schedule_value = self._schedule_waiting_device_hash[waiting_schedule_key]
            subfunction_schedule_result_queue: Queue = waiting_schedule_value['queue']
            subfunction_schedule_result_queue.put(schedule_result_value)
            self._schedule_waiting_device_hash.pop(waiting_schedule_key)

    def handle_MS_RESULT_EXECUTE(self, msg: mqtt.MQTTMessage):
        topic, payload, timestamp = unpack_mqtt_message(msg)

        # MT/RESULT/EXECUTE/[FunctionName]/[ThingName]/[MiddlewareName]/[SuperThingName]
        subfunction_name = topic[3]
        target_thing_name = topic[4]
        target_middleware_name = topic[5]
        super_thing_name = topic[6]
        try:
            error = SoPErrorType(payload['error'])
        except ValueError as e:
            error = SoPErrorType(int(payload['error']))
        scenario_name = payload['scenario']
        return_type = payload['return_type']
        return_value = payload['return_value']

        super_execute_result_value = self.make_super_execute_result_value(
            error, scenario_name, return_type, return_value)
        waiting_super_execute_key = self.make_super_execute_key(
            subfunction_name,
            target_thing_name,
            target_middleware_name,
            super_thing_name,
            scenario_name)
        if waiting_super_execute_key in self._super_execute_waiting_hash:
            waiting_super_execute_value = self._super_execute_waiting_hash[
                waiting_super_execute_key]
            subfunction_super_execute_result_queue: Queue = waiting_super_execute_value[
                'queue']
            subfunction_super_execute_result_queue.put(
                super_execute_result_value)

            # if error == 0:
            #     SOPLOG_DEBUG(
            #         f'[handle_MS_RESULT_EXECUTE] {subfunction_name} execute success!', 'green')
            # else:
            #     SOPLOG_DEBUG(
            #         f'[handle_MS_RESULT_EXECUTE] {subfunction_name} execute failed...', 'red')
            #     result['return_value'] = False

            # mapping_key = self.make_super_service_mapping_key(
            #     subfunction_name, super_function_name, requester_middleware_name, scenario_name)
            # for target_device in self._service_mapping_table[mapping_key]:
            #     if target_device['thing_name'] == target_thing_name and target_device['middleware_name'] == target_middleware_name:
            #         target_device['result'] = result

            # self._unsubscribe(subscribe_topic)
            self._super_execute_waiting_hash.pop(waiting_super_execute_key)

    def handle_MS_RESULT_SERVICE_LIST(self, msg: mqtt.MQTTMessage):
        topic, payload, timestamp = unpack_mqtt_message(msg)

        # for dump example service list...
        # json_file_write('service_list.json', payload)

        try:
            for middleware in payload['services']:
                middleware_name = middleware['middleware']
                hierarchy_type = middleware['hierarchy']
                thing_list = middleware['things']
                for thing in thing_list:
                    is_alive = thing['is_alive']
                    if is_alive != 1:
                        continue
                    is_super = thing['is_super']
                    alive_cycle = thing['alive_cycle']

                    thing_name = thing['id']
                    value_list = thing['values']
                    function_list = thing['functions']

                    for value_info in value_list:
                        function_tag_list = [SoPTag(tag['name'])
                                             for tag in value_info['tags']]
                        value = SoPValue(
                            name=value_info['name'],
                            tag_list=function_tag_list,
                            desc=value_info['description'],
                            type=type_converter(value_info['type']),
                            bound=(float(value_info['bound']['min_value']),
                                   float(value_info['bound']['max_value'])),
                            format=value_info['format'],
                            # cycle=value_info['cycle']
                        )

                        service_info = SoPServiceInfo(
                            thing_name=thing_name,
                            middleware_name=middleware_name,
                            hierarchy=hierarchy_type,
                            service_type=SoPServiceType.VALUE,
                            policy=None,
                            is_alive=is_alive,
                            is_super=is_super,
                            value=value,
                            function=None,
                        )
                        if service_info not in self._hierarchical_service_table.value_list:
                            self._hierarchical_service_table.value_list.append(
                                service_info)
                    for function_info in function_list:
                        function_tag_list = [SoPTag(tag['name'])
                                             for tag in function_info['tags']]

                        arg_list = [
                            SoPArgument(
                                name=arg['name'],
                                type=type_converter(arg['type']),
                                bound=(float(arg['bound']['min_value']),
                                       float(arg['bound']['max_value'])),
                            ) for arg in function_info['arguments']] if bool(function_info['use_arg']) else []

                        function = SoPFunction(
                            name=function_info['name'],
                            tag_list=function_tag_list,
                            desc=function_info['description'],
                            arg_list=arg_list,
                            return_type=type_converter(
                                function_info['return_type']),
                            exec_time=function_info['exec_time'],
                            timeout=None)

                        service_info = SoPServiceInfo(
                            thing_name=thing_name,
                            middleware_name=middleware_name,
                            hierarchy=hierarchy_type,
                            service_type=SoPServiceType.VALUE,
                            policy=None,
                            is_alive=is_alive,
                            is_super=is_super,
                            value=None,
                            function=function,
                        )
                        if service_info not in self._hierarchical_service_table.function_list:
                            self._hierarchical_service_table.function_list.append(
                                service_info)

            # if self._is_super:
            #     for function in self._function_list:
            #         _subfunction_list = function._target_subfunction_list
            #         for subfunction in _subfunction_list:
            #             subfunction_info = self.find_super_function_service(
            #                 function.get_name())
            #             subfunction.target_thing = subfunction_info.get_thing_name()

            self._last_refresh_time = get_current_time()
        except KeyError as e:
            print_error(e)
            SOPLOG_DEBUG('[handle_MS_RESULT_SERVICE_LIST] KeyError', 'red')
        except ValueError as e:
            print_error(e)
            SOPLOG_DEBUG('[handle_MS_RESULT_SERVICE_LIST] ValueError', 'red')
        except Exception as e:
            print_error(e)
            SOPLOG_DEBUG(
                '[handle_MS_RESULT_SERVICE_LIST] Unknown Exception', 'red')

        # MS/EXECUTE/off_all/SuperThingTest_D45D64A628DB/Middleware222222_DCA632DD3CB5/#
        # MS/EXECUTE/off_all/SuperThingTest_D45D64A628DB

    # ===================
    #   __  __   ______
    #  |  \/  | |  ____|
    #  | \  / | | |__
    #  | |\/| | |  __|
    #  | |  | | | |____
    #  |_|  |_| |______|
    # ===================

    def handle_ME_NOTIFY(self, msg: mqtt.MQTTMessage):
        topic, payload, timestamp = unpack_mqtt_message(msg)

        self.send_SM_REFRESH()

        try:
            pass
        except KeyError as e:
            print_error(e)
            SOPLOG_DEBUG('[handle_ME_NOTIFY] KeyError', 'red')
        except ValueError as e:
            print_error(e)
            SOPLOG_DEBUG('[handle_ME_NOTIFY] ValueError', 'red')
        except Exception as e:
            print_error(e)
            SOPLOG_DEBUG(
                '[handle_ME_NOTIFY] Unknown Exception', 'red')

    # ================
    #  _____ ___  ___
    # /  ___||  \/  |
    # \ `--. | .  . |
    #  `--. \| |\/| |
    # /\__/ /| |  | |
    # \____/ \_|  |_/
    # ================

    def send_SM_SCHEDULE(self, target_subfunction_name: str, target_thing_name: str,
                         target_middleware_name: str, super_thing_name: str, scenario_name: str, period: float):
        '''TM/SCHEDULE/[FunctionName]/[ThingName]/[MiddlewareName]/[SuperThingName]'''
        topic = SoPProtocolType.Super.SM_SCHEDULE.value % (
            target_subfunction_name, target_thing_name, target_middleware_name, super_thing_name)
        payload = {
            "scenario": scenario_name,
            "period": period
        }
        msg = encode_MQTT_message(topic, payload)

        self._publish_queue.put(msg)

    # TODO: complete this function
    def send_SM_EXECUTE(self, subfunction_name: str, target_thing_name: str, target_middleware_name: str,
                        super_thing_name: str, scenario_name: str, arg_list: Tuple):
        topic = SoPProtocolType.Super.SM_EXECUTE.value % (
            subfunction_name, target_thing_name, target_middleware_name, super_thing_name)

        payload = {
            "scenario": scenario_name,
            "arguments": [{'order': i, 'value': str(arg)} for i, arg in enumerate(arg_list)] if arg_list else []
        }
        msg = encode_MQTT_message(topic, payload)

        self._publish_queue.put(msg)

    def send_SM_RESULT_SCHEDULE(self, schedule_result: ScheduleResult):
        # super_function_name, super_thing_name, super_middleware_name, requester_middleware_name, scenario_name = schedule_result.unpack()

        topic = SoPProtocolType.Super.SM_RESULT_SCHEDULE.value % (
            schedule_result.function_name,
            schedule_result.thing_name,
            schedule_result.middleware_name,
            schedule_result.requester_middleware_name)
        payload = {
            "scenario": schedule_result.scenario_name,
            "error": schedule_result.error.value,
        }
        msg = encode_MQTT_message(topic, payload)

        self._publish_queue.put(msg)

    def send_SM_RESULT_EXECUTE(self, super_execute_result: SuperExecuteResult):

        topic = SoPProtocolType.Super.SM_RESULT_EXECUTE.value % (
            super_execute_result.super_function_name,
            super_execute_result.super_thing_name,
            super_execute_result.super_middleware_name,
            super_execute_result.requester_middleware_name)
        payload = {
            "error": super_execute_result.error.value,
            "scenario": super_execute_result.scenario_name,
            "return_type": super_execute_result.return_type.value,
            "return_value": super_execute_result.return_value
        }
        msg = encode_MQTT_message(topic, payload)

        self._publish_queue.put(msg)

    def send_SM_AVAILABILITY(self):
        availablity = self.dump_availablity()

        topic = SoPProtocolType.Super.SM_AVAILABILITY.value % self._name
        payload = dict_to_json_string(availablity)
        msg = encode_MQTT_message(topic, payload)

        self._publish_queue.put(msg)
        self._last_available_send_time = get_current_time()

    def send_SM_REFRESH(self):
        topic = SoPProtocolType.Super.SM_REFRESH.value % self._name
        payload = EMPTY_JSON
        msg = encode_MQTT_message(topic, payload)

        self._publish_queue.put(msg)

    # ========================
    #         _    _  _
    #        | |  (_)| |
    #  _   _ | |_  _ | | ___
    # | | | || __|| || |/ __|
    # | |_| || |_ | || |\__ \
    #  \__,_| \__||_||_||___/
    # ========================

    def schedule(self, schedule_request: ScheduleRequest):
        super_function_name, \
            super_thing_name, \
            super_middleware_name, \
            requester_middleware_name, \
            scenario_name, \
            period = schedule_request.unpack()

        schedule_request_key = self.make_schedule_request_key(super_function_name,
                                                              super_thing_name,
                                                              super_middleware_name,
                                                              requester_middleware_name,
                                                              scenario_name)

        if schedule_request_key in self._schedule_waiting_list:
            print_error(
                '[schedule] schedule_request_key already exists in _schedule_waiting_hash')
            return False
        else:
            self._schedule_waiting_list.append(schedule_request_key)

        self._thread = SoPThread(
            func=self.schedule_thread_func,
            daemon=True,
            arg_list=(schedule_request, ))
        self._thread.start()

    def find_super_function_service(self, super_function_service_name):
        for function in self._function_list:
            if function.get_name() == super_function_service_name:
                return function

    def make_subfunction_list(self, super_function_name: str, subfunction_name: str,
                              arg_list: List[SoPArgument], tag_list: List[SoPTag], policy: SoPPolicy):
        for function in self._function_list:
            if not function.get_name() == super_function_name:
                continue
            if function.get_first_execute():
                function.add_subfunction(SoPFunction(name=subfunction_name,
                                                     arg_list=arg_list,
                                                     tag_list=tag_list,
                                                     policy=policy))
                return True
            else:
                return False

    def request_function_service(self, tags: List[SoPTag] = [], subfunction_name: str = '', arg_list: Tuple = None,
                                 super_function_name: str = '',  policy: SoPPolicy = 'all', timeout=40) -> Union[List[dict], bool]:
        if self.make_subfunction_list(
                super_function_name, subfunction_name, arg_list, tags, policy):
            return

        result_list = []
        for k, service_map in self._service_mapping_table.items():
            if not (subfunction_name in k and super_function_name in k):
                continue

            for service in service_map:
                target_middleware_name = service['middleware_name']
                target_thing_name = service['thing_name']
                super_thing_name = service['super_thing_name']
                super_function_name = service['super_function_name']
                scenario_name = service['scenario_name']

                subfunction_super_execute_result_topic = SoPProtocolType.Super.MS_RESULT_EXECUTE.value % (
                    subfunction_name, target_thing_name, target_middleware_name, super_thing_name)
                super_execute_key = self.make_super_execute_key(
                    subfunction_name,
                    target_thing_name,
                    target_middleware_name,
                    super_thing_name,
                    scenario_name)
                execute_result_queue = Queue()
                waiting_execute_value = self.make_super_execute_value(
                    tags,
                    subfunction_super_execute_result_topic,
                    self._middleware_name,
                    super_function_name,
                    execute_result_queue
                )

                if super_execute_key not in self._super_execute_waiting_hash:
                    self._super_execute_waiting_hash[super_execute_key] = waiting_execute_value
                else:
                    raise Exception(
                        'duplicated key... super execute request already exist')

                self._subscribe(subfunction_super_execute_result_topic)
                self.send_SM_EXECUTE(subfunction_name,
                                     target_thing_name,
                                     target_middleware_name,
                                     super_thing_name,
                                     scenario_name,
                                     arg_list)
                SOPLOG_DEBUG(
                    f'....[Subfunction EXECUTE]', 'green')
                try:
                    super_execute_result = execute_result_queue.get(timeout=60)
                except Exception:
                    raise Exception(
                        'subfunction execute timeout... skip subfunction run')
                finally:
                    self._unsubscribe(subfunction_super_execute_result_topic)

                error = SoPErrorType(super_execute_result['error'])
                try:
                    error = SoPErrorType(super_execute_result['error'])
                except ValueError as e:
                    error = SoPErrorType(int(super_execute_result['error']))
                result_scenario_name = super_execute_result['scenario_name']
                running_scenario_hash_value = self._running_scenario_hash[scenario_name]
                requester_middleware_name = running_scenario_hash_value[0]['requester_middleware_name']

                if error == SoPErrorType.NO_ERROR:
                    SOPLOG_DEBUG(
                        f'........[Subfunction EXECUTE END] subfunction {subfunction_name} target Thing:{target_thing_name}, Middleware:{target_middleware_name} subfunction result received!!!', 'green')

                    mapping_key = self.make_super_service_mapping_key(
                        subfunction_name, super_function_name, requester_middleware_name, scenario_name)
                    for target_device in self._service_mapping_table[mapping_key]:
                        if target_thing_name == target_device['thing_name'] and target_middleware_name == target_device['middleware_name']:
                            target_device['result'] = super_execute_result
                            result_list.append(super_execute_result)
                elif not result_scenario_name == scenario_name:
                    schedule_result = ScheduleResult(super_function_name,
                                                     super_thing_name,
                                                     target_middleware_name,
                                                     requester_middleware_name,
                                                     super_thing_name,
                                                     SoPErrorType.NO_ERROR,
                                                     scenario_name)
                    self.send_SM_RESULT_SCHEDULE(schedule_result)
                    raise Exception(f'''[schedule_thread_func] scenario name mismatch... skip schedule'
                                    recv scenario={result_scenario_name}
                                    target scenario={scenario_name}''')
                else:
                    SOPLOG_DEBUG(f'schedule failed for \
                        thing      | {target_thing_name} \
                        middleware | {target_middleware_name}. \
                        go to next target...', 'yellow')
        # else:
        #     SOPLOG_DEBUG(
        #         f'Super service mapping info not found : mapping_key={mapping_key}', 'red')

        return result_list

    # execute service via super service
    def req(self, tag_list: List[str] = [], service_name: str = '', arg_list: Tuple = None,
            service_type: SoPServiceType = SoPServiceType.FUNCTION, policy: SoPPolicy = SoPPolicy.SINGLE,
            timeout=40) -> Union[List[dict], bool]:

        # TODO: implemnet more pancy way to get super service name(previous function name)
        super_service_name = inspect.currentframe().f_back.f_code.co_name
        if isinstance(tag_list, list):
            pass
        elif isinstance(tag_list, str):
            tag_list = [tag_list]
        else:
            tag_list = []
        tag_list = [SoPTag(str_tag) for str_tag in tag_list]

        try:
            if service_type == SoPServiceType.FUNCTION:
                return self.request_function_service(tags=tag_list, subfunction_name=service_name, arg_list=arg_list,
                                                     super_function_name=super_service_name, policy=policy, timeout=timeout)
            elif service_type == SoPServiceType.VALUE:
                return self.request_function_service(tags=tag_list, subfunction_name=f'__{service_name}', arg_list=arg_list,
                                                     super_function_name=super_service_name, policy=policy, timeout=timeout)
            else:
                raise Exception(
                    'service type error!!! service type only can be [SoPServiceType.FUNCTION | SoPServiceType.VALUE]')
        except Exception as e:
            print_error(e)
            return False

    # execute scenario line
    def r(self, line: str = None, *arg_list) -> Union[List[dict], bool]:
        super_service_name = inspect.currentframe().f_back.f_code.co_name

        scope_policy = 'all' if 'all' in line else 'single'
        function_name = line.split('.')[1][0:line.split('.')[1].find('(')]
        braket_parse: List[str] = re.findall(r'\(.*?\)', line)
        tags = [tag[1:] for tag in braket_parse[0][1:-1].split(' ')]

        argments = []
        for braket_inner_element in braket_parse[1][1:-1].split(','):
            braket_inner_element = braket_inner_element.strip(' ')
            if braket_inner_element == '':
                continue
            else:
                argments.append(braket_inner_element)

        for i, arg in enumerate(argments):
            if '$' in arg:
                index = int(arg[1:])
                argments[i] = arg_list[index-1]

        argments = tuple(argments)

        result_list = self.request_function_service(tags=tags, subfunction_name=function_name, arg_list=argments,
                                                    super_function_name=super_service_name, policy=scope_policy)

        return result_list

    def search_service(self, src_service_list: List[Union[SoPServiceInfo, SoPSuperFunction, SoPValue]],
                       target_service_name: str = None, target_tags_list: List[SoPTag] = None) -> Union[List[Union[SoPServiceInfo, SoPSuperFunction, SoPValue]], bool]:
        exist_target_device_list = []

        # function name and value name(prefix '__') check
        for function_info in src_service_list:
            if not (target_service_name == function_info.get_name() or
                    target_service_name == '__' + function_info.get_name()):
                continue

            # service tag check
            if not target_tags_list:
                exist_target_device_list.append(function_info)
            else:
                for tag in target_tags_list:
                    if not tag in [tag for tag in function_info.get_tag_list()]:
                        break
                else:
                    exist_target_device_list.append(function_info)

        return exist_target_device_list if len(exist_target_device_list) > 0 else False

    # override
    def _subscribe_init_topics(self, thing_name: str):
        super()._subscribe_init_topics(thing_name)

        topic_list = [SoPProtocolType.Super.MS_RESULT_SERVICE_LIST.value % thing_name,
                      SoPProtocolType.WebClient.ME_NOTIFY_CHANGE.value % thing_name]

        for topic in topic_list:
            self._subscribe(topic)

    # override
    def _subscribe_service_topics(self, thing_name: str, function_list: List[SoPFunction]):
        for function in function_list:
            function_name = function.get_name()
            middleware_name = self._middleware_name
            function.set_execute_result_queue(
                self._publish_queue)

            topic_list = [SoPProtocolType.Super.MS_EXECUTE.value % (function_name, thing_name, middleware_name, '#'),
                          SoPProtocolType.Super.MS_SCHEDULE.value % (
                function_name, thing_name, middleware_name, '#')]

            for topic in topic_list:
                self._subscribe(topic)

    # make functions
    def make_schedule_request_key(self, super_function_name, super_thing_name, super_middleware_name, requester_middleware_name, scenario_name):
        return f'{super_function_name}_{super_thing_name}_{super_middleware_name}_{requester_middleware_name}_{scenario_name}'

    def make_super_execute_key(self, function_name, thing_name, middleware_name, super_thing_name, scenario_name):
        return f'{function_name}_{thing_name}_{middleware_name}_{super_thing_name}_{scenario_name}'

    def make_super_execute_value(self, subfunction_tags, subscribe_topic, requester_middleware_name, super_function_name, queue):
        return {
            'tags': subfunction_tags,
            'subscribe_topic': subscribe_topic,
            'requester_middleware_name': requester_middleware_name,
            'super_function_name': super_function_name,
            'queue': queue
        }

    def make_super_execute_result_value(self, error: SoPErrorType, scenario_name: str, return_type: SoPType, return_value: Union[bool, float, str, int]) -> Dict:
        return {
            'error': error.value,
            'scenario_name': scenario_name,
            'return_type': return_type,
            'return_value': return_value
        }

    # target_subfunction_name, target_thing_name, target_middleware_name, super_thing_name, scenario_name
    def make_schedule_request_device_key(self, target_subfunction_name, target_thing_name, target_middleware_name, super_thing_name, scenario_name):
        return f'{target_subfunction_name}_{target_thing_name}_{target_middleware_name}_{super_thing_name}_{scenario_name}'

    def make_schedule_request_device_value(self, subfunction_tags, subscribe_topic, requester_middleware_name, super_function_name, queue):
        return {
            'tags': subfunction_tags,
            'subscribe_topic': subscribe_topic,
            'requester_middleware_name': requester_middleware_name,
            'super_function_name': super_function_name,
            'queue': queue
        }

    def make_schedule_result_value(self, error: SoPErrorType, scenario_name: str) -> Dict:
        return {
            'error': error.value,
            'scenario_name': scenario_name
        }

    def make_super_service_mapping_key(self, subfunction_name: str, super_function_name: str, requester_middleware_name: str, scenario_name: str) -> str:
        return f'{subfunction_name}_{super_function_name}_{requester_middleware_name}_{scenario_name}'

    def make_super_service_mapping_value(self, target_thing_name: str, target_middleware_name: str, super_thing_name: str, super_function_name: str, scenario_name: str) -> Dict:
        return {
            'thing_name': target_thing_name,
            'middleware_name': target_middleware_name,
            'super_thing_name': super_thing_name,
            'super_function_name': super_function_name,
            'scenario_name': scenario_name,
            'result': None
        }

    def dump_availablity(self) -> Dict:
        super_function_list = []

        for function in self._function_list:
            sub_function_list = []
            for subfunction in function.get_subfunction_list():
                sub_function_list.append({
                    'name': subfunction.get_name(),
                    'status': 1 if subfunction in
                    [function_info for function_info in
                     self._hierarchical_service_table.function_list] else 0
                })
            super_function_list.append({
                'name': function.get_name(),
                'status': 0 if 0 in
                [sub_function['status'] for sub_function in sub_function_list] else 1,
                'sub_functions': sub_function_list
            })
        availablity_info = {
            "super_functions": super_function_list
        }

        return availablity_info

    def make_sm_function_run_packet(self, target_scenario_name: str, target_middleware_name: str, target_thing_name: str, target_function_name: str, arg_list) -> Dict:
        return {'scenario': target_scenario_name,
                'middleware': target_middleware_name,
                'thing': target_thing_name,
                'function': target_function_name,
                'arguments': arg_list}

    # getter functions
    def get_local_function(self, function_name: str) -> SoPSuperFunction:
        local_function_list = self._function_list
        for local_function in local_function_list:
            local_function_name = local_function.get_name()
            if local_function_name == function_name:
                return local_function

    def get_super_function_target_scenario(self, super_function: str) -> str:
        local_function_list = self._function_list
        for local_function in local_function_list:
            local_function_name = local_function.get_name()
            if local_function_name == super_function:
                target_scenario = local_function.get_scenario_name()
                return target_scenario

    def get_super_service_info(self, target_function_info: SoPFunction, super_function_name: str) -> Tuple[str, str, str, str]:
        target_thing = target_function_info.get_thing_name()
        target_middleware = target_function_info.get_middleware_name()
        target_function = target_function_info.get_name()
        target_scenario = self.get_super_function_target_scenario(
            super_function_name)
        return target_thing, target_middleware, target_function, target_scenario

    # etc...
    def extract_subfunction_info(self) -> None:
        for function in self._function_list:
            if self._is_super:
                arg_list = function.get_arg_list()
                function._func(*arg_list)
                function._first_execute = False

    # ====================================
    #               _    _
    #              | |  | |
    #   __ _   ___ | |_ | |_   ___  _ __
    #  / _` | / _ \| __|| __| / _ \| '__|
    # | (_| ||  __/| |_ | |_ |  __/| |
    #  \__, | \___| \__| \__| \___||_|
    #   __/ |
    #  |___/
    # ====================================

    # override
    def get_function_list(self) -> List[SoPSuperFunction]:
        return [service for service in self._service_list if isinstance(service, SoPSuperFunction)]

    # ==================================
    #             _    _
    #            | |  | |
    #  ___   ___ | |_ | |_   ___  _ __
    # / __| / _ \| __|| __| / _ \| '__|
    # \__ \|  __/| |_ | |_ |  __/| |
    # |___/ \___| \__| \__| \___||_|
    # ==================================
