from big_thing import *
from manager.staff_thing import *


class SoPManagerThing(SoPBigThing, metaclass=ABCMeta):

    MANAGER_THREAD_TIME_OUT = THREAD_TIME_OUT

    class ManagerModeHandler:
        def __init__(self, mode: SoPManagerMode) -> None:
            self._mode = mode

        def dump_register_packet(self, staff_thing: SoPStaffThing) -> mqtt.MQTTMessage:
            if self._mode == SoPManagerMode.JOIN:
                # in join mode, manager thing don't need to send each staff thing's register packet
                # it's only need to send manager thing's register packet to middleware
                pass
            elif self._mode == SoPManagerMode.SPLIT:
                if staff_thing.get_registered():
                    SOPLOG_DEBUG(
                        '[dump_register_packet] staff thing already registered')
                    return False

                topic = SoPProtocolType.Default.TM_REGISTER.value % (
                    staff_thing.get_name())
                payload = staff_thing.dump()
                msg = mqtt.MQTTMessage(topic, payload)
                return staff_thing.get_name(), payload
            else:
                raise ManagerModeError(
                    '[dump_register_packet] please set mode {SoPManagerMode.JOIN|SoPManagerMode.SPLIT}')

        def dump_alive_packet(self, staff_thing_list: List[SoPStaffThing]) -> Union[mqtt.MQTTMessage, List[mqtt.MQTTMessage]]:
            if self._mode == SoPManagerMode.JOIN:
                # in join mode, manager thing don't need to send each staff thing's alive packet
                # it's only need to send manager thing's alive packet to middleware
                pass
            elif self._mode == SoPManagerMode.SPLIT:
                packet_list = []

                for staff_thing in staff_thing_list:
                    if staff_thing.get_registered():
                        continue
                    topic = SoPProtocolType.Default.TM_ALIVE.value % (
                        staff_thing.get_name())
                    payload = EMPTY_JSON
                    msg = mqtt.MQTTMessage(topic, payload)
                    packet_list.append(msg)

                return packet_list
            else:
                raise ManagerModeError(
                    '[dump_alive_packet] please set mode {SoPManagerMode.JOIN|SoPManagerMode.SPLIT}')

        def dump_value_packet(self, staff_thing_list: List[SoPStaffThing]) -> Union[mqtt.MQTTMessage, List[mqtt.MQTTMessage]]:
            if self._mode == SoPManagerMode.JOIN:
                # in join mode, manager thing don't need to send each staff thing's value packet
                # it's only need to send manager thing's value packet to middleware
                pass
            elif self._mode == SoPManagerMode.SPLIT:
                packet_list = []

                for staff_thing in staff_thing_list:
                    if staff_thing.get_registered():
                        continue
                    for value in staff_thing.get_value_list():
                        value_dump = value.dump()

                        topic = SoPProtocolType.Default.TM_ALIVE.value % (
                            staff_thing.get_name())
                        payload = EMPTY_JSON
                        msg = mqtt.MQTTMessage(topic, payload)
                        packet_list.append(msg)

                return packet_list
            else:
                raise ManagerModeError(
                    '[dump_value_packet] please set mode {SoPManagerMode.JOIN|SoPManagerMode.SPLIT}')

        def dump_execute_result_packet(self, staff_thing_list: List[SoPStaffThing]) -> Union[mqtt.MQTTMessage, List[mqtt.MQTTMessage]]:
            if self._mode == SoPManagerMode.JOIN:
                pass
            elif self._mode == SoPManagerMode.SPLIT:
                pass
            else:
                raise ManagerModeError(
                    '[dump_execute_result_packet] please set mode {SoPManagerMode.JOIN|SoPManagerMode.SPLIT}')

    def __init__(self, name: str = None, service_list: List[SoPService] = None, alive_cycle: float = 60, is_super: bool = False, is_parallel: bool = True, ip: str = None, port: int = None, ssl_ca_path: str = None, ssl_enable: bool = None, log_enable: bool = True, append_mac_address: bool = True,
                 mode: SoPManagerMode = SoPManagerMode.SPLIT, network_type: SoPNetworkType = SoPNetworkType.MQTT, scan_cycle=5):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel,
                         ip, port, ssl_ca_path, ssl_enable, log_enable, append_mac_address)

        self._staff_client = None
        self._last_scan_time = 0
        self._scan_cycle = scan_cycle

        self._mode = mode
        self._network_type = network_type

        # TODO: this is necessary?
        # self._network_status = SoPNetworkStatus.RESET

        self._staff_thing_list: List[SoPStaffThing] = []
        self.manager_mode_handler = self.ManagerModeHandler(mode=self._mode)

        # Threading
        self._thread_func_list += [
            self.scan_staff_message,
            self.receive_staff_message_thread_func,
            self.publish_staff_message_thread_func,
            self.register_thread_func,
            self.alive_check_thread_func,
            self.value_update_thread_func
        ]

        # Queue
        self._staff_register_queue = Queue()
        self._staff_alive_queue = Queue()
        self._staff_value_queue = Queue()
        self._staff_receive_queue = Queue()
        self._staff_publish_queue = Queue()

    def run(self):
        try:
            # Start BigThing's Thread function
            for thread in self._waiting_thread_list:
                thread.start()
                self._running_thread_list.append(thread)

            # Register try
            if self._mode == SoPManagerMode.JOIN:
                retry = 5
                while not self._registered and retry:
                    SOPLOG_DEBUG(f'Register try {6-retry}', 'yellow')
                    retry -= 1
                    payload = self.dump()

                    self._subscribe_init_topics(self._name)
                    self.send_TM_REGISTER(
                        thing_name=self._name, payload=payload)

                    current_time = get_current_time()
                    while get_current_time() - current_time < 5:
                        if self._registered:
                            break
                        else:
                            time.sleep(0.1)
            else:
                pass

            # Maintain main thread
            while not self._g_exit.wait(THREAD_TIME_OUT):
                time.sleep(1000)
            else:
                raise Exception('_g_exit was set!!!')
        except KeyboardInterrupt as e:
            SOPLOG_DEBUG('Ctrl + C Exit', 'red')
        except ConnectionRefusedError as e:
            SOPLOG_DEBUG(
                'Connection error while connect to broker. Check ip and port', 'red')
            print_error(e)
        except Exception as e:
            SOPLOG_DEBUG(
                'Some error', 'red')
            print_error(e)
        finally:
            self._g_exit.set()
            return self.wrapup()

    def wrapup(self):
        try:
            for staff_thing in self._staff_thing_list:
                self.send_TM_UNREGISTER(staff_thing.get_name())

            # FIXME: Fix it to guarantee UNREGISTER packet publishing is complete
            # while self._publish_queue.empty():
            #     time.sleep(0.1)
            time.sleep(2)

            for thread in self._running_thread_list:
                thread.exit()

            if not self._g_exit:
                for thread in self._running_thread_list:
                    thread.join()

            self._mqtt_client.disconnect()
            SOPLOG_DEBUG('Thing Exit', 'red')
            return True
        except Exception as e:
            print_error(e)
            return False

    # ===========================================================================================
    #  _    _                             _    __                      _    _
    # | |  | |                           | |  / _|                    | |  (_)
    # | |_ | |__   _ __   ___   __ _   __| | | |_  _   _  _ __    ___ | |_  _   ___   _ __   ___
    # | __|| '_ \ | '__| / _ \ / _` | / _` | |  _|| | | || '_ \  / __|| __|| | / _ \ | '_ \ / __|
    # | |_ | | | || |   |  __/| (_| || (_| | | |  | |_| || | | || (__ | |_ | || (_) || | | |\__ \
    #  \__||_| |_||_|    \___| \__,_| \__,_| |_|   \__,_||_| |_| \___| \__||_| \___/ |_| |_||___/
    # ===========================================================================================

    def scan_staff_message(self, stop_event: Event):
        try:
            while not stop_event.wait(self.MANAGER_THREAD_TIME_OUT):
                msg = self._receive_staff_packet()

                if msg is None:
                    # print('msg is None...')
                    continue
                else:
                    self._staff_receive_queue.put(msg)
        except Exception as e:
            stop_event.set()
            print_error(e)
            return False

    def receive_staff_message_thread_func(self, stop_event: Event):
        try:
            while not stop_event.wait(self.MANAGER_THREAD_TIME_OUT):
                msg = self._staff_receive_queue.get()

                if msg is None:
                    continue
                else:
                    self._handle_staff_message(msg)
        except Exception as e:
            stop_event.set()
            print_error(e)
            return False

    def publish_staff_message_thread_func(self, stop_event: Event):
        try:
            while not stop_event.wait(self.MANAGER_THREAD_TIME_OUT):
                msg = self._staff_publish_queue.get()

                self._send_staff_message(msg)
        except Exception as e:
            stop_event.set()
            print_error(e)
            return False

    def register_thread_func(self, stop_event: Event) -> Tuple[SoPNewStaffThingLevel, SoPStaffThing]:

        # TODO: There is a problem that Thing detect does not work well
        def get_new_staff_thing_level(new_staff_thing: SoPStaffThing):
            for staff_thing in self._staff_thing_list:
                new_staff_thing_name = new_staff_thing.get_name()
                if new_staff_thing_name == staff_thing.get_name():
                    if new_staff_thing == staff_thing:
                        return SoPNewStaffThingLevel.OLD, staff_thing
                    else:
                        return SoPNewStaffThingLevel.UPDATE, staff_thing
            else:
                return SoPNewStaffThingLevel.NEW, None

        try:
            while not stop_event.wait(self.MANAGER_THREAD_TIME_OUT):
                register_info: SoPStaffThingInfo = self._staff_register_queue.get()
                new_staff_thing: SoPStaffThing = self._create_staff(
                    register_info)
                register_result = StaffRegisterResult(
                    staff_thing_name=new_staff_thing.get_name(), device_id=new_staff_thing.get_device_id(), assigned_device_id=None)

                # staff thing이 새로운 것인지 중복인지 업데이트인지 확인
                staff_thing_level, old_staff_thing = get_new_staff_thing_level(
                    new_staff_thing)
                if staff_thing_level == SoPNewStaffThingLevel.NEW:
                    SOPLOG_DEBUG(
                        f'New staff_thing!!! name = {new_staff_thing.get_name()}', 'green')
                    self._staff_thing_list.append(new_staff_thing)
                    self._subscribe_init_topics(new_staff_thing.get_name())
                    register_result.assigned_device_id = new_staff_thing.get_device_id()
                elif staff_thing_level == SoPNewStaffThingLevel.OLD:
                    SOPLOG_DEBUG(
                        f'hue staff thing {new_staff_thing.get_name()} already in list', 'yellow')
                    continue
                elif staff_thing_level == SoPNewStaffThingLevel.UPDATE:
                    # SOPLOG_DEBUG(
                    #     f'staff_thing {new_staff_thing.get_name()} info was updated!!!', 'green')
                    # self._staff_thing_list.remove(old_staff_thing)
                    # self._staff_thing_list.append(new_staff_thing)
                    SOPLOG_DEBUG(
                        f'hue staff thing {new_staff_thing.get_name()} already in list', 'yellow')
                    continue

                # mode에 따라 동작 구분
                register_info = self.manager_mode_handler.dump_register_packet(
                    new_staff_thing)

                if register_info:
                    self.send_TM_REGISTER(register_info[0], register_info[1])

                self._staff_publish_queue.put(register_result)

        except Exception as e:
            # 'str' object has no attribute 'value'
            stop_event.set()
            print_error(e)
            return False

    def alive_check_thread_func(self, stop_event: Event):
        try:
            while not stop_event.wait(THREAD_TIME_OUT):
                msg = self._staff_alive_queue.get()

                staff_thing_name = msg['staff_thing_name']
                alive_recv_time = msg['alive_recv_time']

                for staff_thing in self._staff_thing_list:
                    if get_current_time() - staff_thing.get_last_alive_time() > self.get_alive_cycle():
                        # if staff alive was not come in alive cycle
                        pass
                    else:
                        pass

        except Exception as e:
            stop_event.set()
            print_error(e)
            return False

    def value_update_thread_func(self, stop_event: Event):
        try:
            while not stop_event.wait(THREAD_TIME_OUT):
                msg = self._staff_value_queue.get()
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

    def handle_MT_RESULT_REGISTER(self, msg: mqtt.MQTTMessage):
        topic, payload, timestamp = unpack_mqtt_message(msg)

        thing_name = topic[3]
        try:
            error = SoPErrorType(payload['error'])
        except ValueError as e:
            error = SoPErrorType(int(payload['error']))
        middleware_name = payload['middleware_name']

        if self._mode == SoPManagerMode.JOIN:
            if not thing_name == self._name:
                return
            ret = self._check_register_result(error)

            if ret:
                self._middleware_name = middleware_name
                self._registered = True
                self._subscribe_service_topics(self._name, self._function_list)
            else:
                SOPLOG_DEBUG(
                    f'[handle_MT_RESULT_REGISTER] Register failed... error code : {error}')
        elif self._mode == SoPManagerMode.SPLIT:
            for staff_thing in self._staff_thing_list:
                if not thing_name == staff_thing.get_name():
                    continue
                ret = self._check_register_result(error)

                if ret:
                    staff_thing.set_middleware_name(middleware_name)
                    staff_thing.set_registered(True)
                    self._subscribe_service_topics(
                        staff_thing.get_name(), staff_thing.get_function_list())
                else:
                    SOPLOG_DEBUG(
                        f'[handle_MT_RESULT_REGISTER] Register failed... error code : {error}')

    def handle_MT_EXECUTE(self, msg: mqtt.MQTTMessage):
        topic, payload, timestamp = unpack_mqtt_message(msg)
        # ZigbeeSwitch3_eb65ca597dbc149d4esv4q
        target_function_name = topic[2]
        target_thing_name = topic[3]
        scenario_name = payload['scenario']
        arg_list = payload['arguments']

        if target_function_name not in self._running_scenario_hash:
            self._running_scenario_hash[target_function_name] = []
        self._running_scenario_hash[target_function_name].append(scenario_name)

        execute_request = ExecuteRequest(
            target_function_name, target_thing_name, scenario_name, self._is_parallel, arg_list)
        execute_request.set_user_data(self._running_scenario_hash)

        for staff_thing in self._staff_thing_list:
            if topic[-1] == staff_thing._name:
                for function in staff_thing.get_function_list():
                    function_name = function.get_name()
                    if function_name == target_function_name:
                        function.execute(execute_request)
                        return True
                else:
                    SOPLOG_DEBUG('function not exist', 'red')
                    return False

    # ==================================================================================================================================
    #  _   _                    _  _                     _                   _                           _
    # | | | |                  | || |                   | |                 | |                         | |
    # | |_| |  __ _  _ __    __| || |  ___   ___  _   _ | |__   _ __    ___ | |_ __      __  ___   _ __ | | __  _ __ ___   ___   __ _
    # |  _  | / _` || '_ \  / _` || | / _ \ / __|| | | || '_ \ | '_ \  / _ \| __|\ \ /\ / / / _ \ | '__|| |/ / | '_ ` _ \ / __| / _` |
    # | | | || (_| || | | || (_| || ||  __/ \__ \| |_| || |_) || | | ||  __/| |_  \ V  V / | (_) || |   |   <  | | | | | |\__ \| (_| |
    # \_| |_/ \__,_||_| |_| \__,_||_| \___| |___/ \__,_||_.__/ |_| |_| \___| \__|  \_/\_/   \___/ |_|   |_|\_\ |_| |_| |_||___/ \__, |
    #                                                                                                                            __/ |
    #                                                                                                                           |___/
    # ==================================================================================================================================

    @abstractmethod
    def _handle_staff_message(self, msg):
        pass

    @abstractmethod
    def _send_staff_message(self):
        pass

    @abstractmethod
    def _receive_staff_packet(self):
        pass

    @abstractmethod
    def _publish_staff_packet(self, msg):
        pass

    # ========================
    #         _    _  _
    #        | |  (_)| |
    #  _   _ | |_  _ | | ___
    # | | | || __|| || |/ __|
    # | |_| || |_ | || |\__ \
    #  \__,_| \__||_||_||___/
    # ========================

    @abstractmethod
    def _create_staff(self, staff_info):
        pass

    def make_staff_value_name(self, staff_thing_name, value_name):
        return f'{staff_thing_name}/{value_name}'

    def append_staff_thing_value(self, new_staff_thing: SoPStaffThing):
        self._staff_thing_list.append(new_staff_thing)
        for value in new_staff_thing.get_value_list():
            if not value in self._value_list:
                staff_value_name = self.make_staff_value_name(
                    new_staff_thing.get_name(), value.get_name())
                value.set_name(staff_value_name)
                self._value_list.append(value)
