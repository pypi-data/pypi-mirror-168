from tests.tools.test_tools_utils import *


class Expecter():

    def __init__(self, mqtt_client_list: Union[SoPMQTTMonitor, List[SoPMQTTMonitor]] = None, expect_file_path: Union[str, list] = None) -> None:
        if isinstance(mqtt_client_list, list):
            self._mqtt_client_list = mqtt_client_list
        elif isinstance(mqtt_client_list, SoPMQTTMonitor):
            self._mqtt_client_list = [mqtt_client_list, ]

        self._expect_start_time: float = None
        self._expect = self.load(expect_file_path)
        self._scenario_name = None
        self._delay_queue = Queue()
        self._result_queue = Queue()
        self._scenario_result = {
            'scenario': None,
            'start': None,
            'result': False,
            'function_result': []
        }

    def init(self):
        for mqtt_client in self._mqtt_client_list:
            mqtt_client.run()
        self.parse()
        self.verify_expect()
        self.exepct_subscribe()

        self._scenario_name = self._expect['scenario']
        self._scenario_result['scenario'] = self._scenario_name

    def load(self, expect_file_path: str):
        try:
            with open(expect_file_path, 'r') as f:
                return ''.join(f.readlines())
        except FileNotFoundError:
            return None

    def add_mqtt_client(self, mqtt_client: SoPMQTTMonitor):
        if mqtt_client not in self._mqtt_client_list:
            self._mqtt_client_list.append(mqtt_client)

    def parse(self) -> None:
        if self._expect is None:
            raise Exception('expect is required')
        elif type(self._expect) is str:
            self._expect = json_string_to_dict(self._expect.replace('\n', ''))
        elif type(self._expect) is list:
            self._expect = json_string_to_dict(
                ''.join(self._expect).replace('\n', ''))

    def verify_expect(self) -> None:
        if type(self._expect) is str:
            raise SOPTEST_LOG_DEBUG('expect json string to dict failed', -1)
        elif self._expect['expect'][-1]['type'] == 'delay':
            SOPTEST_LOG_DEBUG(
                'last line of expect should not be delay', 1)
            self._expect['expect'].pop()
        else:
            SOPTEST_LOG_DEBUG('verify expect done', 0)

    def add_mqtt_client(self, mqtt_client: SoPMQTTMonitor):
        self._mqtt_client_list.append(mqtt_client)

    def exepct_subscribe(self):
        expect_list: List[dict] = self._expect['expect']

        for expect_line in expect_list:
            expect_type = expect_line['type']
            expect_function_name = expect_line.get('function', None)
            expect_thing_name = expect_line.get('thing', '+')
            expect_middleware_name = expect_line.get('middleware', '+')

            if expect_type == 'execute':
                for mqtt_client in self._mqtt_client_list:
                    mqtt_client.subscribe(
                        SoPProtocolType.Default.TM_RESULT_EXECUTE.value % (expect_function_name, '#'))
                    mqtt_client.subscribe(
                        SoPProtocolType.Default.MT_EXECUTE.value % (expect_function_name, '#'))
            elif expect_type == 'super_execute':
                for mqtt_client in self._mqtt_client_list:
                    mqtt_client.subscribe(
                        SoPProtocolType.Super.PC_RESULT_EXECUTE.value % (expect_function_name, expect_thing_name, expect_middleware_name, '#'))
                    mqtt_client.subscribe(
                        SoPProtocolType.Super.MS_EXECUTE.value % (expect_function_name, expect_thing_name, expect_middleware_name, '#'))
        else:
            SOPTEST_LOG_DEBUG('expect subscribe ready...', 0)

    def select_mqtt_client(self, level):
        sel_mqtt_client: SoPMQTTMonitor = None
        for mqtt_client in self._mqtt_client_list:
            if mqtt_client._port == int(f'{level}1883'):
                sel_mqtt_client = mqtt_client

        return sel_mqtt_client

    def start(self, scenario_start_time: float = None):
        self._expect_start_time = time.time()
        expect_list: List[dict] = self._expect['expect']
        self._scenario_result['start'] = scenario_start_time

        try:
            for expect_line in expect_list:
                expect_type = expect_line['type']
                expect_tag_list = expect_line.get('tag_list', None)
                expect_function_name = expect_line.get('function', None)
                expect_return_value = expect_line.get('return_value', None)

                if expect_type == 'execute':
                    expect_thing_name = expect_line.get('thing', None)
                    expect_middleware_name = expect_line.get(
                        'middleware', None)
                    expect_level = expect_line.get('level', 1)
                    self.handle_execute_expect(expect_tag_list, expect_function_name,
                                               expect_return_value, expect_thing_name, expect_middleware_name,
                                               expect_type, expect_level)
                elif expect_type == 'super_execute':
                    expect_thing_name = expect_line.get('thing', '+')
                    expect_middleware_name = expect_line.get(
                        'middleware', '+')
                    expect_level = expect_line.get('level', 1)
                    self.handle_execute_expect(expect_tag_list, expect_function_name,
                                               expect_return_value, expect_thing_name, expect_middleware_name,
                                               expect_type, expect_level)
                elif expect_type == 'schedule':
                    # TODO: implement this
                    pass
                elif expect_type == 'sub_schedule':
                    # TODO: implement this
                    pass
                elif expect_type == 'delay':
                    expect_duration = expect_line.get('duration', None)
                    self.handle_delay_expect(expect_duration)
                elif expect_type == 'scenario':
                    expect_scenario_state = ScenarioStateType.get(
                        expect_line.get('state', None))
                    self.handle_scenario_expect(expect_scenario_state)
            else:
                SOPTEST_LOG_DEBUG(f'expect success!', 0)
                self._scenario_result['result'] = True
                return self._scenario_result
        except Exception as e:
            SOPTEST_LOG_DEBUG(f'expect failed...', -1, e)
            self._scenario_result['result'] = False
            return self._scenario_result

    def handle_delay_expect(self, expect_duration: float = None) -> None:
        '''
        Example

        {
            "type": "delay",
            "duration": {int|float}
        }
        '''

        if expect_duration != None:
            self._delay_queue.put(
                {'duration': expect_duration, 'cur_time': time.time()})
            time.sleep(expect_duration)
        else:
            raise Exception('duration is required')

    def handle_execute_expect(self, expect_tag_list: List[str] = None, expect_function_name: str = None,
                              expect_return_value=None, expect_thing_name: str = None, expect_middleware_name: str = None,
                              expect_type: str = None, expect_level: int = 1) -> None:
        '''
        Example

        {
            "type": "execute",
            "level": {int},
            "function": {string},
            "thing": {string},
            "scenario": {string},
            "return_value": {string},
            "return_type": {string},
            "tag_list": [
                {
                    "name": {string}
                },
                ...
            ],
        }
        '''

        sel_mqtt_client = self.select_mqtt_client(expect_level)

        if expect_function_name == None:
            raise Exception('function_name is required')

        if expect_type == 'execute':
            # SOPTEST_LOG_DEBUG(
            #     f'expecting execute {expect_function_name} -- {expect_thing_name}', 0)
            topic, payload, timestamp = sel_mqtt_client.expect(
                include_topic=SoPProtocolType.Default.MT_EXECUTE.value % (
                    expect_function_name, expect_thing_name if expect_thing_name is not None else ''),
                auto_subscribe=False, auto_unsubscribe=False)
        elif expect_type == 'super_execute':
            # SOPTEST_LOG_DEBUG(
            #     f'expecting super execute {expect_function_name}...', 0)
            topic, payload, timestamp = sel_mqtt_client.expect(
                target_topic=SoPProtocolType.Super.MS_EXECUTE.value % (
                    expect_function_name, expect_thing_name if expect_thing_name is not None else '+', expect_middleware_name, '#'),
                auto_subscribe=False, auto_unsubscribe=False)

        if payload == None:
            raise SOPTEST_LOG_DEBUG(
                f'function {expect_function_name} execute failed...', -1)
        else:
            function_result = {
                'function': expect_function_name,
                'thing': expect_thing_name,
                'result': SoPErrorType.UNKNOWN,
                'start': timestamp,
                'end': 0,
                'duration': 0
            }

        if expect_type == 'execute':
            # SOPTEST_LOG_DEBUG(
            #     f'expecting execute result {expect_function_name} -- {expect_thing_name}...', 0)
            topic, payload, timestamp = sel_mqtt_client.expect(
                include_topic=SoPProtocolType.Default.TM_RESULT_EXECUTE.value % (
                    expect_function_name, expect_thing_name if expect_thing_name is not None else ''),
                auto_subscribe=False, auto_unsubscribe=False)
        elif expect_type == 'super_execute':
            # SOPTEST_LOG_DEBUG(
            #     f'expecting super execute result {expect_function_name} -- {expect_thing_name}...', 0)
            topic, payload, timestamp = sel_mqtt_client.expect(
                target_topic=SoPProtocolType.Super.PC_RESULT_EXECUTE.value % (
                    expect_function_name, expect_thing_name if expect_thing_name is not None else '+', expect_middleware_name, '#'),
                auto_subscribe=False, auto_unsubscribe=False)

        if payload == None:
            raise SOPTEST_LOG_DEBUG(
                f'function {expect_function_name} execute failed...', -1)

        # check delay expectation
        if not self._delay_queue.empty():
            delay_info = self._delay_queue.get()
            expect_duration = delay_info['duration']
            prev_time = delay_info['cur_time']
            cur_time = time.time()
            time_error = 1
            if abs(cur_time - prev_time) < expect_duration + time_error:
                SOPTEST_LOG_DEBUG(
                    f'expect delay checked! -- expect: {expect_duration}, received: {cur_time - prev_time}', 0)
            else:
                raise SOPTEST_LOG_DEBUG('Scenario run failed...', -1,
                                        Exception(f'expect delay failed... -- expect: {expect_duration} | received: {cur_time - prev_time}'))

        # check function execute expectation
        recv_function_name = topic.split('/')[3]
        recv_thing_name = topic.split('/')[4]

        recv_error = payload['error']
        recv_return_type = payload['return_type']
        recv_return_value = payload['return_value']

        expect_tag_list = [expect_tag['name'] for expect_tag in (
            expect_tag_list if expect_tag_list != None else [])]
        if recv_error in [0, -4]:
            if expect_tag_list not in [None, []]:
                service_list = get_service_list(sel_mqtt_client)
                target_thing_tag_list = get_service_tag_list_from_service_list(
                    service_list, recv_function_name, recv_thing_name, expect_middleware_name)
                if not set(expect_tag_list).issubset(set(target_thing_tag_list)):
                    raise SOPTEST_LOG_DEBUG('Scenario run failed...', -1,
                                            Exception(f'expect delay failed... -- expect: {expect_duration} | received: {cur_time - prev_time}'))
            if expect_return_value not in [None, '']:
                if self.return_value_to_python_value(recv_return_value, recv_return_type) != expect_return_value:
                    raise SOPTEST_LOG_DEBUG('Scenario run failed...', -1,
                                            Exception(f'expect return value failed... -- expect: {expect_return_value} | received: {recv_return_value}'))
            if expect_return_value not in [None, '']:
                if self.return_value_to_python_value(recv_return_value, recv_return_type) != expect_return_value:
                    raise SOPTEST_LOG_DEBUG('Scenario run failed...', -1,
                                            Exception(f'expect return value failed... -- expect: {expect_return_value} | received: {recv_return_value}'))
            if expect_thing_name not in [None, ''] and expect_thing_name not in ['+', '#']:
                if expect_thing_name != recv_thing_name:
                    raise SOPTEST_LOG_DEBUG('Scenario run failed...', -1,
                                            Exception(f'expect thing name failed... -- expect: {expect_thing_name} | received: {recv_thing_name}'))

            # we can't compare middleware name, because middleware name is not in function execute packet
            #
            # if expect_middleware_name is not None:
            #     if expect_middleware_name != recv_middleware_name:
            #         raise SOPTEST_LOG_DEBUG('Scenario run failed...', -1,
            #                                 Exception(f'expect thing name failed... -- expect: {expect_middleware_name} | received: {recv_middleware_name}'))

            SOPTEST_LOG_DEBUG(
                f'function {expect_function_name} execute checked!', 0)
            function_result['end'] = timestamp
            function_result['duration'] = function_result['end'] - \
                function_result['start']
            function_result['thing'] = recv_thing_name
            function_result['result'] = SoPErrorType.NO_ERROR
            self._scenario_result['function_result'].append(function_result)
            return True
        elif recv_error in [-2]:
            SOPTEST_LOG_DEBUG(
                f'function {expect_function_name} execute timeout feature checked!', 0)
            function_result['end'] = timestamp
            function_result['duration'] = function_result['end'] - \
                function_result['start']
            function_result['thing'] = recv_thing_name
            function_result['result'] = SoPErrorType.TIMEOUT
            self._scenario_result['function_result'].append(function_result)
            return True
        elif recv_error in [-1]:
            SOPTEST_LOG_DEBUG(
                f'function {expect_function_name} execute fail feature checked!', 0)
            function_result['end'] = timestamp
            function_result['duration'] = function_result['end'] - \
                function_result['start']
            function_result['thing'] = recv_thing_name
            function_result['result'] = SoPErrorType.EXECUTE_FAIL
            self._scenario_result['function_result'].append(function_result)
            return True
        else:
            function_result['end'] = timestamp
            function_result['duration'] = function_result['end'] - \
                function_result['start']
            function_result['thing'] = recv_thing_name
            function_result['result'] = SoPErrorType.UNKNOWN
            self._scenario_result['function_result'].append(function_result)
            raise SOPTEST_LOG_DEBUG(
                f'function {expect_function_name} execute failed...', -1)

    # TODO: implement this
    def handle_scenario_expect(self, expect_scenario_state: ScenarioStateType = None, expect_level: int = None) -> None:
        '''
        Example

        {
            "type": "scenario",
            "level": {int},
            "scenario": {string},
            "state": {"created"|"scheduling"|"initialized"|"running"|"executing"|"stucked"|"completed"},
        }
        '''

        sel_mqtt_client = self.select_mqtt_client(expect_level)

        topic, payload, timestamp = sel_mqtt_client.publish_and_expect(
            encode_MQTT_message('EM/REFRESH/%s' %
                                sel_mqtt_client._client_id, f'{{}}'),
            'ME/RESULT/SCENARIO_LIST/%s' % sel_mqtt_client._client_id)

        if payload == None:
            raise SOPTEST_LOG_DEBUG(
                f'scenario {self._scenario_name} expect failed...', -1)

        # check delay expectation
        if not self._delay_queue.empty():
            delay_info = self._delay_queue.get()
            expect_duration = delay_info['duration']
            prev_time = delay_info['cur_time']
            cur_time = time.time()
            time_error = 1
            if abs(cur_time - prev_time) < expect_duration + time_error:
                SOPTEST_LOG_DEBUG(
                    f'expect delay checked! -- expect: {expect_duration}, received: {cur_time - prev_time}', 0)
            else:
                raise SOPTEST_LOG_DEBUG('Scenario run failed...', -1,
                                        Exception(f'expect delay failed... -- expect: {expect_duration} | received: {cur_time - prev_time}'))

        # check scenario state expectation
        target_scenario_info = find_scenario(
            sel_mqtt_client, self._scenario_name)
        if target_scenario_info['state'] == expect_scenario_state:
            SOPTEST_LOG_DEBUG(
                f'expect scenario state checked! -- expect: {target_scenario_info["state"]}, received: {expect_scenario_state}', 0)
        else:
            SOPTEST_LOG_DEBUG('Scenario run failed...', -1,
                              Exception(f'expect scenario state failed... -- expect: {target_scenario_info["state"]} | received: {expect_scenario_state}'))

    def return_value_to_python_value(self, return_value, return_type):
        if return_type == 'int':
            return int(return_value)
        elif return_type == 'double':
            return float(return_value)
        elif return_type == 'bool':
            if return_value in ['true', True] or int(return_value) == 1:
                return True
            elif return_value in ['true', False] or int(return_value) == 0:
                return False
            else:
                raise Exception('Return value is not bool type')
        elif return_type == 'string' or return_type == 'binary':
            return str(return_value)
        elif return_type == 'void':
            return None
        else:
            raise Exception('Unknown type...')
