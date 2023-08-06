from enum import Enum
from common import *


class EventType(Enum):
    UNDEFINED = 'UNDEFINED'

    DELAY = 'DELAY'

    MIDDLEWARE_RUN = 'MIDDLEWARE_RUN'
    MIDDLEWARE_KILL = 'MIDDLEWARE_KILL'

    THING_RUN = 'THING_RUN'
    THING_KILL = 'THING_KILL'
    THING_REGISTER = 'THING_REGISTER'
    THING_UNREGISTER = 'THING_UNREGISTER'

    THING_REGISTER_RESULT = 'THING_REGISTER_RESULT'
    THING_UNREGISTER_RESULT = 'THING_UNREGISTER_RESULT'

    FUNCTION_EXECUTE = 'FUNCTION_EXECUTE'
    FUNCTION_EXECUTE_RESULT = 'FUNCTION_EXECUTE_RESULT'

    VALUE_PUBLISH = 'VALUE_PUBLISH'

    SCENARIO_VERIFY = 'SCENARIO_VERIFY'
    SCENARIO_ADD = 'SCENARIO_ADD'
    SCENARIO_RUN = 'SCENARIO_RUN'
    SCENARIO_STOP = 'SCENARIO_STOP'
    SCENARIO_UPDATE = 'SCENARIO_UPDATE'
    SCENARIO_DELETE = 'SCENARIO_DELETE'

    SCENARIO_VERIFY_RESULT = 'SCENARIO_VERIFY_RESULT'
    SCENARIO_ADD_RESULT = 'SCHEDULE_SCENARIO_RESULT'
    SCENARIO_RUN_RESULT = 'SCENARIO_RUN_RESULT'
    SCENARIO_STOP_RESULT = 'SCENARIO_STOP_RESULT'
    SCENARIO_UPDATE_RESULT = 'SCHEDULE_SCENARIO_RESULT'
    SCENARIO_DELETE_RESULT = 'SCENARIO_DELETE_RESULT'

    SUPER_FUNCTION_EXECUTE = 'SUPER_FUNCTION_EXECUTE'
    SUPER_FUNCTION_EXECUTE_RESULT = 'SUPER_FUNCTION_EXECUTE_RESULT'
    SUB_FUNCTION_EXECUTE = 'SUB_FUNCTION_EXECUTE'
    SUB_FUNCTION_EXECUTE_RESULT = 'SUB_FUNCTION_EXECUTE_RESULT'
    SUB_SCHEDULE = 'SUB_SCHEDULE'
    SUB_SCHEDULE_RESULT = 'SUB_SCHEDULE_RESULT'
    SUPER_SCHEDULE = 'SUPER_SCHEDULE'
    SUPER_SCHEDULE_RESULT = 'SUPER_SCHEDULE_RESULT'

    @classmethod
    def get(cls, name: str):
        try:
            return cls[name.upper()]
        except Exception:
            return cls.UNDEFINED


class ActionType(Enum):
    UNDEFINED = 'UNDEFINED'

    RUN = 'RUN'
    KILL = 'KILL'
    UNREGISTER = 'UNREGISTER'
    SCENARIO_VERIFY = 'SCENARIO_VERIFY'
    SCENARIO_ADD = 'SCENARIO_ADD'
    SCENARIO_RUN = 'SCENARIO_RUN'
    SCENARIO_STOP = 'SCENARIO_STOP'
    SCENARIO_UPDATE = 'SCENARIO_UPDATE'
    SCENARIO_DELETE = 'SCENARIO_DELETE'
    DELAY = 'DELAY'

    @classmethod
    def get(cls, name: str):
        try:
            return cls[name.upper()]
        except Exception:
            return cls.UNDEFINED


class ElementType(Enum):
    UNDEFINED = 'UNDEFINED'

    MIDDLEWARE = 'MIDDLEWARE'
    THING = 'THING'
    SCENARIO = 'SCENARIO'
    DELAY = 'DELAY'

    @classmethod
    def get(cls, name: str):
        try:
            return cls[name.upper()]
        except Exception:
            return cls.UNDEFINED


class SimulationData():

    def __init__(self, level: int = None, timestamp: float = None, event_type: EventType = None, name: str = None, host: str = None, port: int = None,
                 is_local: bool = None, remote_user: str = None, remote_host: str = None, remote_port: int = None, remote_password: str = None,
                 parent_host: str = None, parent_port: int = None, local_server_port: int = None, web_socket_port: int = None, ssl_web_socket_port: int = None, ssl_port: int = None, middleware_path: str = None, middleware_out_path: str = None,
                 args: List[str] = None, is_super: bool = None, is_manager: bool = None, thing_file_path: str = None,
                 scenario_file_path: str = None, period: float = None,
                 duration: float = None,
                 chunk: dict = None) -> None:

        # Basic SoPElement data
        self.level = level
        self.timestamp = timestamp
        self.event_type = EventType.get(event_type)
        self.name = name
        self.host = host
        self.port = port

        # Remote config (Optional)
        self.is_local = is_local
        self.remote_user = remote_user
        self.remote_host = remote_host
        self.remote_port = remote_port
        self.remote_password = remote_password

        # Additional SoPMiddlewareElement data
        self.parent_host = parent_host
        self.parent_port = parent_port
        self.local_server_port = local_server_port
        self.web_socket_port = web_socket_port
        self.ssl_web_socket_port = ssl_web_socket_port
        self.ssl_port = ssl_port
        self.middleware_out_path = middleware_out_path
        self.middleware_path = middleware_path

        # Additional SoPThingElement data
        self.args = args
        self.is_super = is_super
        self.is_manager = is_manager
        self.thing_file_path = thing_file_path

        # Additional SoPScenarioElement data
        self.scenario_file_path = scenario_file_path
        self.period = period

        # Additional SoPDelayElement data
        self.duration = duration

        if chunk is not None:
            self.load(chunk)

    def load(self, data: dict):

        # Basic SoPElement data
        self.level = data.get('level', None)
        self.timestamp = data.get('timestamp', None)
        self.event_type = EventType.get(data.get('event_type', None))
        self.name = data.get('name', None)
        self.host = data.get('host', None)
        self.port = data.get('port', None)

        # Remote config (Optional)
        self.is_local = data.get('is_local', True)
        self.remote_user = data.get('remote_user', None)
        self.remote_host = data.get('remote_host', None)
        self.remote_port = data.get('remote_port', None)
        self.remote_password = data.get('remote_password', None)

        # Additional SoPMiddlewareElement data
        self.parent_host = data.get('parent_host', None)
        self.parent_port = data.get('parent_port', None)
        self.local_server_port = data.get('local_server_port', None)
        self.web_socket_port = data.get('web_socket_port', None)
        self.ssl_web_socket_port = data.get('ssl_web_socket_port', None)
        self.ssl_port = data.get('ssl_port', None)
        self.middleware_path = data.get('middleware_path', None)
        self.middleware_out_path = data.get('middleware_out_path', None)

        # Additional SoPThingElement data
        self.args = data.get('args', None)
        self.is_super = data.get('is_super', None)
        self.is_manager = data.get('is_manager', None)
        self.thing_file_path = data.get('thing_file_path', None)

        # Additional SoPScenarioElement data
        self.scenario_file_path = data.get('scenario_file_path', None)
        self.period = data.get('period', None)

        # Additional SoPDelayElement data
        self.duration = data.get('duration', None)

        return self


class EventHolder():

    def __init__(self, thing_name: str = None, middleware_name: str = None, scenario_name: str = None, function_name: str = None, value_name: str = None,
                 event_type: EventType = None, level: int = None, timestamp: float = None, duration: float = None,
                 return_value=None, return_type: SoPType = SoPType.UNDEFINED, result: SoPErrorType = SoPErrorType.NO_ERROR, energy=None,
                 host: str = None, port: int = None,
                 target_function_name: str = None, target_thing_name: str = None, target_middleware_name: str = None, requester_middleware_name: str = None) -> None:
        self.host = host
        self.port = port

        self.thing_name = thing_name
        self.middleware_name = middleware_name
        self.scenario_name = scenario_name
        self.function_name = function_name
        self.value_name = value_name

        self.event_type = event_type
        self.level = level
        self.timestamp = timestamp
        self.duration = duration
        self.return_value = return_value
        self.return_type = return_type
        self.result = result
        self.energy = energy

        self.target_function_name = target_function_name
        self.target_thing_name = target_thing_name
        self.target_middleware_name = target_middleware_name
        self.requester_middleware_name = requester_middleware_name

    def load(self, data: Any):
        pass
