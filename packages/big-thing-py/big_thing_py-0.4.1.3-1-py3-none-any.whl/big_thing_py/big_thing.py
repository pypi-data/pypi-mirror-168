from big_thing_py.core.thing import *

import paho.mqtt.client as mqtt
from zeroconf import IPVersion, ServiceBrowser, ServiceStateChange, Zeroconf, ZeroconfServiceTypes
from paho.mqtt.client import Client as SoPClient
import ssl

# ======================================================================
#  _____        ______ ______  _         _____  _      _
# /  ___|       | ___ \| ___ \(_)       |_   _|| |    (_)
# \ `--.   ___  | |_/ /| |_/ / _   __ _   | |  | |__   _  _ __    __ _
#  `--. \ / _ \ |  __/ | ___ \| | / _` |  | |  | '_ \ | || '_ \  / _` |
# /\__/ /| (_) || |    | |_/ /| || (_| |  | |  | | | || || | | || (_| |
# \____/  \___/ \_|    \____/ |_| \__, |  \_/  |_| |_||_||_| |_| \__, |
#                                  __/ |                          __/ |
#                                 |___/                          |___/
# ======================================================================


class SoPBigThing(SoPThing):
    def __init__(self, name: str, service_list: List[SoPService], alive_cycle: float, is_super: bool = False, is_parallel: bool = True,
                 ip: str = None, port: int = None, ssl_ca_path: str = None, ssl_enable: bool = None, log_enable: bool = True, append_mac_address: bool = True):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel)

        if log_enable:
            START_LOGGER(logging_mode=SoPLogger.LoggingMode.ALL)
        else:
            START_LOGGER(logging_mode=SoPLogger.LoggingMode.OFF)

        # MQTT
        self._mqtt_client = SoPClient(userdata=None)
        self._connected = False
        self._ip: str = get_ip_from_url(ip.strip())
        self._port: int = port
        self._mac_address: str = get_mac_address()
        self._ssl_ca_path: str = ssl_ca_path
        self._ssl_enable: bool = ssl_enable
        self._avahi_discovered_middleware_list: List[str] = []
        self._avahi_middleware_name = None

        self._g_exit: Event = Event()
        self._waiting_thread_list: List[SoPThread] = []
        self._running_thread_list: List[SoPThread] = []

        # Queue
        self._receive_queue: Queue = Queue()
        self._publish_queue: Queue = Queue()

        self._thread_func_list: List[Callable] = [
            self.receive_message_thread_func,
            self.publish_message_thread_func,
            self.alive_thread_func,
            self.value_publish_thread_func,
        ]

        # key = target_function_name
        # value = {
        #     [
        #         scenario_name1,
        #         scenario_name2,
        #         ...
        #     ]
        # }
        self._running_scenario_hash: Dict[str, list] = {}

        if append_mac_address:
            self._name = self._name + f'_{self._mac_address}'
        else:
            pass

    def __eq__(self, o: object) -> bool:
        is_parallel_check = (self._is_parallel == o._is_parallel)
        is_super_check = (self._is_super == o._is_super)

        return super().__eq__(o) and is_parallel_check and is_super_check

    def setup(self, avahi_enable=True):
        try:
            self.avahi_init(avahi_enable)
            self.connect()

            for func in self._thread_func_list:
                thread = SoPThread(func=func, mode='event')
                self._waiting_thread_list.append(thread)
            return True
        except KeyboardInterrupt:
            SOPLOG_DEBUG('Ctrl + C Exit', 'red')
            self._g_exit.set()
            return self.wrapup()
        except ConnectionRefusedError:
            SOPLOG_DEBUG(
                'Connection error while connect to broker. Check ip and port', 'red')
            self._g_exit.set()
            return self.wrapup()
        except Exception as e:
            print_error(e)
            self._g_exit.set()
            return self.wrapup()

    def run(self):
        try:
            # Start BigThing's Thread function
            for thread in self._waiting_thread_list:
                thread.start()
                self._running_thread_list.append(thread)

            # Register try
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

            # Maintain main thread
            while not self._g_exit.wait(THREAD_TIME_OUT):
                time.sleep(1000)
            else:
                raise Exception('_g_exit was set!!!')
        except KeyboardInterrupt as e:
            SOPLOG_DEBUG('Ctrl + C Exit', 'red')
        except ConnectionRefusedError:
            SOPLOG_DEBUG(
                'Connection error while connect to broker. Check ip and port', 'red')
        except Exception as e:
            print_error(e)
        finally:
            self._g_exit.set()
            return self.wrapup()

    def wrapup(self):
        try:
            self.send_TM_UNREGISTER(self._name)

            # FIXME: Fix it to guarantee UNREGISTER packet publishing is complete
            for thread in self._running_thread_list:
                if 'publish_message' not in thread.get_name():
                    thread.exit()

            while self._publish_queue.empty():
                time.sleep(0.1)
            else:
                time.sleep(0.1)

            for thread in self._running_thread_list:
                thread.exit()
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

    def receive_message_thread_func(self, stop_event: Event):
        try:
            while not stop_event.wait(THREAD_TIME_OUT):
                if self._receive_queue.empty():
                    continue

                msg = self._receive_queue.get()

                self.handle_mqtt_message(msg)
        except Exception as e:
            stop_event.set()
            print_error(e)
            return False

    def publish_message_thread_func(self, stop_event: Event):
        try:
            while not stop_event.wait(THREAD_TIME_OUT):
                if self._publish_queue.empty():
                    continue

                pub_msg = self._publish_queue.get()

                self.send_mqtt_message(pub_msg)
        except Exception as e:
            stop_event.set()
            print_error(e)
            return False

    def alive_thread_func(self, stop_event: Event) -> Union[bool, None]:
        while not self._registered:
            time.sleep(0.1)

        try:
            while not stop_event.wait(THREAD_TIME_OUT):
                current_time = get_current_time()
                if current_time - self._last_alive_time > self._alive_cycle:
                    self.send_TM_ALIVE(thing_name=self._name)
                    self._last_alive_time = current_time

        except Exception as e:
            stop_event.set()
            print_error(e)
            return False

    def value_publish_thread_func(self, stop_event: Event) -> Union[bool, None]:
        while not self._registered:
            time.sleep(0.1)

        try:
            while not stop_event.wait(THREAD_TIME_OUT):
                current_time = get_current_time()
                for value in self._value_list:
                    if (current_time - value.get_last_update_time()) > value.get_cycle():
                        arg_list = value.get_arg_list()
                        arg_list = tuple(arg_list)
                        update_result = value.update(*arg_list)
                        if update_result is not None:
                            value_name = value.get_name()
                            payload = value.dump_pub()
                            self.send_TM_VALUE_PUBLISH(
                                value_name=value_name, payload=payload)
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

        if topic[0] == 'MT':
            if topic[1] == 'RESULT':
                if topic[2] == 'REGISTER':
                    self.handle_MT_RESULT_REGISTER(msg)
                elif topic[2] == 'UNREGISTER':
                    self.handle_MT_RESULT_UNREGISTER(msg)
                elif topic[2] == 'BINARY_VALUE':
                    self.handle_MT_RESULT_BINARY_VALUE(msg)
                else:
                    SOPLOG_DEBUG(
                        '[handle_mqtt_message] Unexpected MT_RESULT topic!')
            elif topic[1] == 'EXECUTE':
                self.handle_MT_EXECUTE(msg)
            else:
                SOPLOG_DEBUG('[handle_mqtt_message] Unexpected MT topic!')

            return True
        else:
            return False

    def send_mqtt_message(self, msg: Union[mqtt.MQTTMessage, ExecuteResult, SuperExecuteResult, ScheduleResult]) -> None:
        if type(msg) == mqtt.MQTTMessage:
            topic, payload, timestamp = decode_MQTT_message(msg, str)
            payload = dict_to_json_string(payload)

            self._publish(topic, payload)
        elif type(msg) == ExecuteResult:
            msg_uppack = list(msg.unpack())
            scenario_name: str = msg_uppack[4]

            for k, v in self._running_scenario_hash.items():
                for running_scenario_name in v:
                    if scenario_name == running_scenario_name:
                        v.remove(running_scenario_name)
                        scenario_name = k

            if not scenario_name:
                # this mean there is no running scenario
                SOPLOG_DEBUG('[send_mqtt_message] Scenario was not found!!!')
            else:
                msg_uppack = tuple(msg_uppack)

            self.send_TM_RESULT_EXECUTE(*(msg_uppack))
        else:
            return False

        return True

    # ===============
    # ___  ___ _____
    # |  \/  ||_   _|
    # | .  . |  | |
    # | |\/| |  | |
    # | |  | |  | |
    # \_|  |_/  \_/
    # ===============

    def handle_MT_RESULT_REGISTER(self, msg: mqtt.MQTTMessage):
        topic, payload, timestamp = unpack_mqtt_message(msg)

        thing_name = topic[3]
        try:
            error = SoPErrorType(payload['error'])
        except ValueError as e:
            error = SoPErrorType(int(payload['error']))
        middleware_name = payload['middleware_name']

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

    def handle_MT_RESULT_UNREGISTER(self, msg: mqtt.MQTTMessage):
        topic, payload, timestamp = unpack_mqtt_message(msg)

        target_thing_name = topic[3]

        try:
            error = SoPErrorType(payload['error'])
        except ValueError as e:
            error = SoPErrorType(int(payload['error']))

        if not target_thing_name == self._name:
            return
        self._check_register_result(error)

        # unsubscribe function, value topics
        self._unsubscrube_all_topics()

    def handle_MT_EXECUTE(self, msg: mqtt.MQTTMessage):
        topic, payload, timestamp = unpack_mqtt_message(msg)

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

        for function in self._function_list:
            function_name = function.get_name()
            if function_name == target_function_name:
                function.execute(execute_request)
                return True
        else:
            SOPLOG_DEBUG('function not exist', 'red')
            return False

    # TODO: complete this function
    def handle_MT_RESULT_BINARY_VALUE(self, msg: mqtt.MQTTMessage) -> None:
        SOPLOG_DEBUG(
            '[handle_mqtt_message] MT_RESULT_BINARY_VALUE is not implemented yet!')

    # ===============
    #  _____ ___  ___
    # |_   _||  \/  |
    #   | |  | .  . |
    #   | |  | |\/| |
    #   | |  | |  | |
    #   \_/  \_|  |_/
    # ===============

    def send_TM_REGISTER(self, thing_name: str, payload: dict) -> None:
        topic = SoPProtocolType.Default.TM_REGISTER.value % thing_name
        msg = encode_MQTT_message(topic, payload)

        self._publish_queue.put(msg)

    def send_TM_UNREGISTER(self, thing_name: str):
        topic = SoPProtocolType.Default.TM_UNREGISTER.value % thing_name
        msg = encode_MQTT_message(topic, EMPTY_JSON)

        self._publish_queue.put(msg)

    def send_TM_ALIVE(self, thing_name: str):
        topic = SoPProtocolType.Default.TM_ALIVE.value % thing_name
        msg = encode_MQTT_message(topic, EMPTY_JSON)

        self._publish_queue.put(msg)

    # TM/VALUE_PUBLISH/[ThingName]/[ValueName]

    def send_TM_VALUE_PUBLISH(self, value_name: str, payload: dict) -> None:
        topic = SoPProtocolType.Default.TM_VALUE_PUBLISH.value % (
            self._name, value_name)
        topic_old = SoPProtocolType.Default.TM_VALUE_PUBLISH_OLD.value % (
            self._name, value_name)
        payload = dict_to_json_string(payload)
        msg = encode_MQTT_message(topic, payload)
        msg_old = encode_MQTT_message(topic_old, payload)

        self._publish_queue.put(msg)
        self._publish_queue.put(msg_old)

    def send_TM_RESULT_EXECUTE(self, function_name: str, thing_name: str, return_type: SoPType, return_value: Union[str, float, bool], scenario_name: str, error: SoPErrorType) -> None:
        topic = SoPProtocolType.Default.TM_RESULT_EXECUTE.value % (
            function_name, thing_name)
        payload = {
            'error': error.value,
            'scenario': scenario_name,
            'return_type': return_type.value,
            'return_value': return_value
        }

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

    def _subscribe_init_topics(self, thing_name: str):
        topic_list = [
            SoPProtocolType.Default.MT_RESULT_REGISTER.value % thing_name,
            SoPProtocolType.Default.MT_RESULT_UNREGISTER.value % thing_name,
            SoPProtocolType.Default.MT_RESULT_BINARY_VALUE.value % thing_name, ]

        for topic in topic_list:
            self._subscribe(topic)

    def _subscribe_service_topics(self, thing_name: str, function_list: List[SoPFunction]):
        topic_list = []

        for function in function_list:
            function_name = function.get_name()
            function.set_execute_result_queue(
                self._publish_queue)

            topic_list.append(SoPProtocolType.Default.MT_EXECUTE.value % (
                function_name, thing_name))

        for topic in topic_list:
            self._subscribe(topic)

    def _unsubscrube_all_topics(self):
        # whenever _unsubscribe function execute, it remove target topic from self._subscribed_topic_set
        # so it need to iterate with copy of self._subscribed_topic_set
        target_topic_list = list(self._subscribed_topic_set)
        for topic in target_topic_list:
            self._unsubscribe(topic)

    def _check_register_result(self, error: SoPErrorType):
        if error == SoPErrorType.NO_ERROR:
            SOPLOG_DEBUG(
                f'{PrintTag.GOOD} Thing {self._name} register success!')
            return True
        elif error == SoPErrorType.DUPLICATE:
            SOPLOG_DEBUG(
                f'{PrintTag.DUP} Thing {self._name} register success!')
            return True
        elif error == SoPErrorType.EXECUTE_FAIL:
            SOPLOG_DEBUG(
                f'{PrintTag.ERROR} Thing {self._name} register packset was nonvaild')
            return False
        else:
            SOPLOG_DEBUG(
                f'[MT_message_parser] Unexpected error occured!!!', 'red')
            return False

    def print_packet(self, msg: mqtt.MQTTMessage, mode: SoPPrintMode = SoPPrintMode.FULL):

        def mode_select(mode: SoPPrintMode, payload: str):
            if mode == SoPPrintMode.SKIP:
                return colored(f'skip... (print_packet mode={mode})', 'yellow'), payload
            elif mode == SoPPrintMode.ABBR:
                payload_raw = payload
                if payload.count('\n') > 10:
                    payload = '\n'.join(payload.split('\n')[:10]) + '\n' + \
                        colored(
                            f'skip... (print_packet mode={mode})', 'yellow')
                    return payload, payload_raw
                elif len(payload) > 1000:
                    payload = payload[:1000] + '\n' + \
                        colored(
                            f'skip... (print_packet mode={mode})', 'yellow')
                    return payload, payload_raw
                else:
                    return payload, payload_raw
            elif mode == SoPPrintMode.FULL:
                return payload, payload
            else:
                SOPLOG_DEBUG(
                    f'[print_packet] Unknown mode!!! mode should be [skip|abbr|full] mode : {mode}', 'red')

        def print_result_topic(topic, payload):
            topic_str = topic_join(topic)
            topic_indicator = f'{topic[0]}_{topic[1]}_{topic[2]}'

            payload, payload_raw = mode_select(mode, payload)
            payload = colored(payload, attrs=['bold'])

            SOPLOG_DEBUG(
                f'[{topic_indicator:20}] topic : {topic_str} payload : {payload}')

        def print_topic(topic, payload):
            topic_str = topic_join(topic)
            topic_indicator = f'{topic[0]}_{topic[1]}'

            payload, payload_raw = mode_select(mode, payload)
            payload = colored(payload, attrs=['bold'])

            SOPLOG_DEBUG(
                f'[{topic_indicator:20}] topic : {topic_str} payload : {payload}')

        topic, payload, timestamp = decode_MQTT_message(msg, str)
        topic = topic_split(topic)

        payload = dict_to_json_string(payload)

        if topic[0] == 'MT':
            if topic[1] == 'RESULT':
                if topic[2] in ['REGISTER', 'UNREGISTER', 'BINARY_VALUE']:
                    print_result_topic(topic, payload)
                else:
                    SOPLOG_DEBUG(
                        f'[print_packet] Unknown {topic[0]}_{topic[1]} Topic!!!', 'red')
            else:
                if topic[1] in ['EXECUTE']:
                    print_topic(topic, payload)
                else:
                    SOPLOG_DEBUG(
                        f'[print_packet] Unknown {topic[0]} Topic!!!', 'red')
        elif topic[0] == 'TM':
            if topic[1] == 'RESULT':
                if topic[2] in ['EXECUTE']:
                    print_result_topic(topic, payload)
                else:
                    SOPLOG_DEBUG(
                        f'[print_packet] Unknown {topic[0]}_{topic[1]} Topic!!!', 'red')
            else:
                if topic[1] in ['REGISTER', 'UNREGISTER', 'ALIVE', 'VALUE_PUBLISH']:
                    print_topic(topic, payload)
                else:
                    SOPLOG_DEBUG(
                        f'[print_packet] Unknown {topic[0]} Topic!!!', 'red')
        elif topic[0] == 'MS':
            if topic[1] == 'RESULT':
                if topic[2] in ['SCHEDULE', 'EXECUTE', 'SERVICE_LIST']:
                    print_result_topic(topic, payload)
                else:
                    SOPLOG_DEBUG(
                        f'[print_packet] Unknown {topic[0]}_{topic[1]} Topic!!!', 'red')
            else:
                if topic[1] in ['SCHEDULE', 'EXECUTE']:
                    print_topic(topic, payload)
                else:
                    SOPLOG_DEBUG(
                        f'[print_packet] Unknown {topic[0]} Topic!!!', 'red')
        elif topic[0] == 'SM':
            if topic[1] == 'RESULT':
                if topic[2] in ['SCHEDULE', 'EXECUTE']:
                    print_result_topic(topic, payload)
                else:
                    SOPLOG_DEBUG(
                        f'[print_packet] Unknown {topic[0]}_{topic[1]} Topic!!!', 'red')
            else:
                if topic[1] in ['SCHEDULE', 'EXECUTE', 'AVAILABILITY', 'REFRESH']:
                    print_topic(topic, payload)
                else:
                    SOPLOG_DEBUG(
                        f'[print_packet] Unknown {topic[0]} Topic!!!', 'red')
        elif topic[0] == 'ME':
            if topic[1] == 'NOTIFY_CHANGE':
                print_topic(topic, payload)
            else:
                SOPLOG_DEBUG(
                    f'[print_packet] Unknown {topic[0]} Topic!!!', 'red')
        elif topic[0] == self._name:
            if topic[1] in [value.get_name() for value in self._value_list]:
                print_topic(topic, payload)
            else:
                SOPLOG_DEBUG(
                    f'[print_packet] Unknown VALUE PUBLISH Topic!!!, topic : {topic}', 'red')
        else:
            topic = topic_join(topic)
            SOPLOG_DEBUG(
                f'[print_packet] Unexpected topic!!! : {topic} ', 'red')

    # MQTT utils
    # ========================
    #         _    _  _
    #        | |  (_)| |
    #  _   _ | |_  _ | | ___
    # | | | || __|| || |/ __|
    # | |_| || |_ | || |\__ \
    #  \__,_| \__||_||_||___/
    # ========================

    def connect(self):
        self._mqtt_client.on_connect = self._on_connect
        self._mqtt_client.on_disconnect = self._on_disconnect
        self._mqtt_client.on_publish = self._on_publish
        self._mqtt_client.on_subscribe = self._on_subscribe
        self._mqtt_client.on_unsubscribe = self._on_unsubscribe
        self._mqtt_client.on_message = self._on_message

        self._mqtt_client.connect(self._ip, self._port)
        self._mqtt_client.loop_start()

    def disconnect(self):
        self._mqtt_client.loop_stop()
        ret = self._mqtt_client.disconnect()

        SOPLOG_DEBUG(
            f'{PrintTag.DISCONNECT} disconnect from Host: {self._ip}:{self._port}', 'red')

    def _subscribe(self, topic: str, qos: int = 2):
        if topic not in self._subscribed_topic_set:
            ret = self._mqtt_client.subscribe(topic, qos=qos)
            self.get_subscribed_topic_set().add(topic)

        SOPLOG_DEBUG(f'{PrintTag.SUBSCRIBE} {topic}')

    def _unsubscribe(self, topic: str):
        if topic in self._subscribed_topic_set:
            ret = self._mqtt_client.unsubscribe(topic)
            self.get_subscribed_topic_set().remove(topic)

        SOPLOG_DEBUG(f'{PrintTag.UNSUBSCRIBE} {topic}')

    def _publish(self, topic: str, payload, qos: int = 2):
        cnt = 3
        while cnt:
            ret = self._mqtt_client.publish(topic, payload, qos=qos)
            if ret.rc != 0:
                SOPLOG_DEBUG('Publish failed!!!', 'red')
                SOPLOG_DEBUG(f'Topic : {topic}', 'red')
                SOPLOG_DEBUG(f'Payload : {payload}', 'red')
                SOPLOG_DEBUG(f'Retry {4-cnt}', 'red')
                cnt -= 1
                time.sleep(5)
            else:
                break
        else:
            SOPLOG_DEBUG(
                'Publish mqtt was not work... exit program', 'red')
            sys.exit(1)

        msg = encode_MQTT_message(topic, payload)
        self.print_packet(msg, mode=SoPPrintMode.ABBR)

    # Avahi feature (WARNING: not work on python3.6<)
    def avahi_discover(self, MQTT_SOPIOT_AVAHI_LIST=["_mqtt_sopiot._tcp.local.", "_mqtt_ssl_sopiot._tcp.local."]):

        def on_service_state_change(zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange) -> None:
            # SOPLOG_DEBUG(
            #     f"Service {name} of type {service_type} state changed: {state_change}")

            if state_change is ServiceStateChange.Added:
                info = zeroconf.get_service_info(
                    service_type, name)
                # SOPLOG_DEBUG("Info from zeroconf.get_service_info: %r" % (info))

                if info:
                    addresses = ["%s:%d" % (addr, cast(int, info.port))
                                 for addr in info.parsed_scoped_addresses()]
                    ipv4_address = addresses[0]
                    ipv6_address = addresses[1]
                    ip = ipv4_address.split(':')[0]
                    port = int(ipv4_address.split(':')[1])

                    discovered_middleware = {
                        'ip': ip,
                        'port': port,
                        'name': info.server,
                    }

                    SOPLOG_DEBUG(f"Server name: {info.server}")
                    SOPLOG_DEBUG(f"Address: {ip}")
                    SOPLOG_DEBUG(
                        f"Weight: {info.weight}, priority: {info.priority}")
                    if info.properties:
                        for key, value in info.properties.items():
                            SOPLOG_DEBUG(
                                f"Properties -> {key.decode('utf-8')}: {value.decode('utf-8')}")
                    else:
                        SOPLOG_DEBUG("No properties", 'yellow')

                    self._avahi_discovered_middleware_list.append(
                        discovered_middleware)
                    self._avahi_middleware_name = info.server
                else:
                    SOPLOG_DEBUG("No info")

        zeroconf = Zeroconf(ip_version=IPVersion.V4Only)
        services = MQTT_SOPIOT_AVAHI_LIST
        # services = list(ZeroconfServiceTypes.find(zc=zeroconf))
        browser = ServiceBrowser(zeroconf, services, handlers=[
                                 on_service_state_change])
        time.sleep(3)
        browser.cancel()
        zeroconf.close()

    def set_ssl_config(self):
        SOPLOG_DEBUG('SSL enabled...')
        try:
            self._mqtt_client.tls_set(
                ca_certs=f'{self._ssl_ca_path}/ca.crt',
                certfile=f'{self._ssl_ca_path}/client.crt',
                keyfile=f'{self._ssl_ca_path}/client.key',
                cert_reqs=ssl.CERT_REQUIRED,
                tls_version=ssl.PROTOCOL_TLSv1_2,
                ciphers=None)
            self._mqtt_client.tls_insecure_set(True)
        except ValueError as e:
            SOPLOG_DEBUG('SSL/TLS has already been configured.', 'yellow')

    def avahi_init(self, avahi_enable):

        def save_middleware_info():
            middleware_info = {
                "middleware_list": [
                    {
                        "name": self._avahi_middleware_name,
                        "ip": self._ip,
                        "port": self._port,
                        "lastest_connect_time": time.time()
                    }
                ]
            }
            json_file_write('middleware_info.json',
                            middleware_info)

        def set_connect_info(selected_middleware: dict):
            self._ip = selected_middleware['ip']
            self._port = selected_middleware['port']

        if avahi_enable:
            if sys.version_info[0] <= 3 and sys.version_info[1] < 6:
                raise Exception(
                    'Avahi feature is not supported on python3.6<. try python3.7 or higher. or disable avahi feature. (avahi_enable=False)')

            self.avahi_discover(MQTT_SOPIOT_AVAHI_LIST=[
                "_mqtt_sopiot._tcp.local.",
                "_mqtt_ssl_sopiot._tcp.local."])
            if len(self._avahi_discovered_middleware_list) > 1:
                SOPLOG_DEBUG('More than 2 avahi_enable host searched...')
                middleware_info = json_file_read('middleware_info.json')

                if middleware_info:
                    middleware_list = sorted(
                        middleware_info['middleware_list'], key=lambda x: x['lastest_connect_time'])
                    set_connect_info(middleware_list[0])
                    SOPLOG_DEBUG(
                        'Connect to lastest connected middleware...')
                else:
                    SOPLOG_DEBUG('middleware_info.json was empty...:')
                    for i, discovered_middleware in enumerate(self._avahi_discovered_middleware_list):
                        ip = discovered_middleware['ip']
                        port = discovered_middleware['port']
                        middleware_name = discovered_middleware['name']
                        SOPLOG_DEBUG(
                            f'{i}: {ip}:{port} ({middleware_name})')
                    while True:
                        user_input = int(input('select middleware : '))
                        if user_input not in range(len(self._avahi_discovered_middleware_list)):
                            SOPLOG_DEBUG(
                                'Invalid input...', 'red')
                        else:
                            break
                    set_connect_info(
                        self._avahi_discovered_middleware_list[user_input])
                    save_middleware_info()

                if self._ssl_enable == True:
                    self.set_ssl_config()
                elif self._port == 8883:
                    self.set_ssl_config()
                else:
                    SOPLOG_DEBUG('SSL is not enabled...')

            elif len(self._avahi_discovered_middleware_list) == 1:
                set_connect_info(self._avahi_discovered_middleware_list[0])
                save_middleware_info()
            else:
                SOPLOG_DEBUG(
                    'avahi_enable search failed... connect to default ip...')
        else:
            SOPLOG_DEBUG('Skip avahi_enable search...')

# ===================================================================================
# ___  ___ _____  _____  _____   _____         _  _  _                   _
# |  \/  ||  _  ||_   _||_   _| /  __ \       | || || |                 | |
# | .  . || | | |  | |    | |   | /  \/  __ _ | || || |__    __ _   ___ | | __ ___
# | |\/| || | | |  | |    | |   | |     / _` || || || '_ \  / _` | / __|| |/ // __|
# | |  | |\ \/' /  | |    | |   | \__/\| (_| || || || |_) || (_| || (__ |   < \__ \
# \_|  |_/ \_/\_\  \_/    \_/    \____/ \__,_||_||_||_.__/  \__,_| \___||_|\_\|___/
# ===================================================================================

    def _on_connect(self, client: SoPClient, userdata, flags, rc):
        if rc == 0:
            self._connected = True
            SOPLOG_DEBUG(
                f'{PrintTag.CONNECT} connect to Host: {self._ip}:{self._port}')
        else:
            self._connected = False
            SOPLOG_DEBUG(
                f'{PrintTag.ERROR} Bad connection Returned code=', rc)

    def _on_disconnect(self, client: SoPClient, userdata, flags, rc=0):
        pass

    def _on_subscribe(self, client: SoPClient, userdata: str, mid, granted_qos):
        pass

    def _on_unsubscribe(self, client: SoPClient, userdata: str, mid, granted_qos=2):
        pass

    def _on_publish(self, client: SoPClient, userdata: mqtt.MQTTMessage, mid):
        pass

    # MQTT Message receive part
    def _on_message(self, client: SoPClient, userdata: Callable, msg: mqtt.MQTTMessage):
        self.print_packet(msg, mode=SoPPrintMode.ABBR)
        self._receive_queue.put(msg)

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

    # ==================================
    #             _    _
    #            | |  | |
    #  ___   ___ | |_ | |_   ___  _ __
    # / __| / _ \| __|| __| / _ \| '__|
    # \__ \|  __/| |_ | |_ |  __/| |
    # |___/ \___| \__| \__| \___||_|
    # ==================================
