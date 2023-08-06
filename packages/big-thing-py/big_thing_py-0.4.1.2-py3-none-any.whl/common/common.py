from common.error import *
from common.soptype import *

from typing import *
from termcolor import *
from abc import *
from enum import Enum


EMPTY_JSON = '{}'
THREAD_TIME_OUT = 0.01


class SoPManagerMode(Enum):
    UNDEFINED = 'UNDEFINED'
    JOIN = 'JOIN'
    SPLIT = 'SPLIT'

    @classmethod
    def get(cls, name: str):
        try:
            return cls[name.upper()]
        except Exception:
            return cls.UNDEFINED


class SoPNewStaffThingLevel(Enum):
    NEW = 0
    OLD = 1
    UPDATE = 2


class RequestMethod(Enum):
    GET = 0
    POST = 1
    PUT = 2
    DELETE = 3


class SoPPrintMode(Enum):
    FULL = 0
    ABBR = 1
    SKIP = 2


class PrintTag:
    # MQTT protocol
    GOOD = '[%-30s]' % colored('✔✔✔', 'green')
    DUP = '[%-30s]' % colored('DUP✔', 'green')
    ERROR = '[%-30s]' % colored('✖✖✖', 'red')

    CONNECT = '[%-30s]' % colored('-> CONNECT', 'blue')
    DISCONNECT = '[%-30s]' % colored('-> DISCONNECT', 'blue')

    SUBSCRIBE = '[%-30s]' % colored('-> SUBSCRIBE', 'white')
    UNSUBSCRIBE = '[%-30s]' % colored('-> UNSUBSCRIBE', 'white')


class SoPPolicy(Enum):
    ALL = 0
    SINGLE = 1


class Request(metaclass=ABCMeta):
    def __init__(self) -> None:
        self.user_date = None

    @abstractmethod
    def unpack(self) -> Tuple:
        pass

    def set_user_data(self, user_date: Any) -> None:
        self.user_date = user_date

    def get_user_date(self) -> Any:
        return self.user_date


class ExecuteRequest(Request):
    def __init__(self, function_name: str = None, thing_name: str = None, arg_list: Tuple = None, scenario_name: str = None, is_parallel: bool = None) -> None:
        self.function_name = function_name
        self.thing_name = thing_name
        self.arg_list = arg_list
        self.scenario_name = scenario_name
        self.is_parallel = is_parallel

    def unpack(self) -> Tuple[str, str, str, bool, Tuple]:
        return self.function_name, self.thing_name, self.arg_list, self.scenario_name, self.is_parallel

    def set_user_data(self, user_date: Dict) -> None:
        self.user_date: Dict = user_date

    def get_user_date(self) -> Dict:
        return self.user_date


class SuperExecuteRequest(ExecuteRequest):
    def __init__(self, super_function_name: str = None, super_thing_name: str = None, super_middleware_name: str = None, requester_middleware_name: str = None,
                 function_name: str = None, thing_name: str = None, arg_list: Tuple = None, scenario_name: str = None, is_parallel: bool = None) -> None:
        super().__init__(function_name, thing_name, arg_list, scenario_name, is_parallel)

        self.super_function_name = super_function_name
        self.super_thing_name = super_thing_name
        self.super_middleware_name = super_middleware_name
        self.requester_middleware_name = requester_middleware_name

    def unpack(self) -> Tuple[str, str, str, str, str, bool, Tuple]:
        return (self.super_function_name, self.super_thing_name, self.super_middleware_name, self.requester_middleware_name) + super().unpack()

    def set_user_data(self, user_date: Dict) -> None:
        self.user_date: Dict = user_date

    def get_user_date(self) -> Dict:
        return self.user_date


class ScheduleRequest(Request):
    def __init__(self, super_function_name: str = None, super_thing_name: str = None, super_middleware_name: str = None, requester_middleware_name: str = None,
                 scenario_name: str = None, period: float = None) -> None:
        self.super_function_name = super_function_name
        self.super_thing_name = super_thing_name
        self.super_middleware_name = super_middleware_name
        self.requester_middleware_name = requester_middleware_name
        self.scenario_name = scenario_name
        self.period = period

    def unpack(self) -> Tuple[str, str, str, str, str, float]:
        return (self.super_function_name, self.super_thing_name, self.super_middleware_name,
                self.requester_middleware_name, self.scenario_name, self.period)

    def set_user_data(self, user_date: Dict) -> None:
        self.user_date: Dict = user_date

    def get_user_date(self) -> Dict:
        return self.user_date


class SubScheduleRequest(ScheduleRequest):
    def __init__(self, target_subfunction_name: str = None, target_thing_name: str = None, target_middleware_name: str = None,
                 super_function_name: str = None, super_thing_name: str = None, super_middleware_name: str = None,
                 requester_middleware_name: str = None, scenario_name: str = None, period: float = None) -> None:
        super().__init__(super_function_name, super_thing_name, super_middleware_name,
                         requester_middleware_name, scenario_name, period)

        self.target_subfunction_name = target_subfunction_name
        self.target_thing_name = target_thing_name
        self.target_middleware_name = target_middleware_name

    def unpack(self) -> Tuple[str, str, str, str, str, float]:
        return (self.target_subfunction_name, self.target_thing_name, self.target_middleware_name, self.super_thing_name,
                self.scenario_name, self.period)

    def set_user_data(self, user_date: Dict) -> None:
        self.user_date: Dict = user_date

    def get_user_date(self) -> Dict:
        return self.user_date


class Result(metaclass=ABCMeta):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def unpack(self) -> Tuple:
        pass

    @abstractmethod
    def topic(self) -> str:
        pass

    @abstractmethod
    def payload(self) -> str:
        pass

    def set_user_data(self, user_date: Dict) -> None:
        self.user_date: Dict = user_date

    def get_user_date(self) -> Dict:
        return self.user_date


# TODO: complete this class
class ExecuteResult(Result):
    def __init__(self, function_name: str = None, thing_name: str = None,  return_type: SoPType = None,
                 return_value: Union[float, str, bool] = None, scenario_name: str = None,  error: SoPErrorType = None) -> None:
        super().__init__()
        self.function_name = function_name
        self.thing_name = thing_name
        self.return_type = return_type
        self.return_value = return_value
        self.scenario_name = scenario_name
        self.error = error

    def unpack(self) -> Tuple[str, str, SoPErrorType, str, SoPType, Union[float, str, bool]]:
        return (self.function_name, self.thing_name, self.return_type, self.return_value, self.scenario_name, self.error)

    def topic(self) -> str:
        return SoPProtocolType.Default.TM_RESULT_EXECUTE.value % (self.function_name, self.thing_name)

    def payload(self) -> Dict:
        return {
            'error': self.error.value,
            'scenario': self.scenario_name,
            'return_type': self.return_type,
            'return_value': self.return_value
        }

    def set_user_data(self, user_date: Dict) -> None:
        self.user_date: Dict = user_date

    def get_user_date(self) -> Dict:
        return self.user_date


class SuperExecuteResult(ExecuteResult):
    def __init__(self, super_function_name: str = None, super_thing_name: str = None, super_middleware_name: str = None, requester_middleware_name: str = None,
                 function_name: str = None, thing_name: str = None, return_type: SoPType = None, return_value: Union[float, str, bool] = None,
                 scenario_name: str = None, error: SoPErrorType = None) -> None:
        super().__init__(function_name, thing_name,
                         return_type, return_value, scenario_name, error)

        self.super_function_name = super_function_name
        self.super_thing_name = super_thing_name
        self.super_middleware_name = super_middleware_name
        self.requester_middleware_name = requester_middleware_name

    def unpack(self) -> Tuple[str, str, int, str, str, float]:
        # self.function_name, self.thing_name, self.error, self.scenario_name, self.return_type, self.return_value
        return super().unpack() + (self.super_thing_name, self.super_middleware_name, self.requester_middleware_name)

    def topic(self) -> str:
        return SoPProtocolType.Super.SM_RESULT_EXECUTE.value % (self.super_function_name, self.super_thing_name,
                                                                self.super_middleware_name, self.requester_middleware_name)

    def payload(self) -> Dict:
        return super().payload()

    def set_user_data(self, user_date: Dict) -> None:
        self.user_date: Dict = user_date

    def get_user_date(self) -> Dict:
        return self.user_date


class ScheduleResult(Result):
    def __init__(self, function_name: str = None, thing_name: str = None, middleware_name: str = None, requester_middleware_name: str = None,
                 super_thing_name: str = None, error: SoPErrorType = None, scenario_name: str = None) -> None:
        super().__init__()
        self.function_name = function_name
        self.thing_name = thing_name
        self.middleware_name = middleware_name
        self.requester_middleware_name = requester_middleware_name
        self.super_thing_name = super_thing_name
        self.error = error
        self.scenario_name = scenario_name

    def unpack(self) -> Tuple[str, str, str, str, SoPErrorType, str]:
        return (self.function_name, self.thing_name, self.middleware_name, self.requester_middleware_name,
                self.super_thing_name, self.error, self.scenario_name)

    def topic(self) -> str:
        return SoPProtocolType.Super.MS_RESULT_SCHEDULE.value % (self.function_name, self.thing_name, self.middleware_name, self.super_thing_name)

    def payload(self) -> Dict:
        return {
            'error': self.error.value,
            'scenario': self.scenario_name
        }

    def set_user_data(self, user_date: Dict) -> None:
        self.user_date: Dict = user_date

    def get_user_date(self) -> Dict:
        return self.user_date


# TODO: implement this
class SoPStaffThingInfo:
    def __init__(self, device_id: str) -> None:
        self.device_id = device_id


class SoPRFStaffThingInfo(SoPStaffThingInfo):
    def __init__(self, device_id: str, addresses: Tuple[int, int], value_name: str, value_cycle: float, alive_cycle: float) -> None:
        super().__init__(device_id)
        self.addresses = addresses
        self.value_name = value_name
        self.value_cycle = value_cycle
        self.alive_cycle = alive_cycle


class SoPHueStaffThingInfo(SoPStaffThingInfo):
    def __init__(self, device_id: str, idx: int, hue_info: dict) -> None:
        super().__init__(device_id)
        self.idx = idx
        self.hue_info = hue_info


class SoPHejhomeStaffThingInfo(SoPStaffThingInfo):
    def __init__(self, device_id: str, hejhome_info: dict) -> None:
        super().__init__(device_id)
        self.hejhome_info = hejhome_info


class StaffRegisterResult:
    def __init__(self, staff_thing_name: str, device_id: str, assigned_device_id: str) -> None:
        self.staff_thing_name = staff_thing_name
        self.device_id = device_id
        self.assigned_device_id = assigned_device_id
