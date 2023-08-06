from core.function import *
from core.value import *


class SoPServiceInfo(SoPValue, SoPFunction):
    def __init__(self, thing_name: str = None, middleware_name: str = None, hierarchy: str = None,
                 service_type: SoPServiceType = None, policy: SoPPolicy = None,
                 is_alive: bool = None, is_super: bool = None,
                 value: SoPValue = None, function: SoPFunction = None) -> None:

        self.value = value
        self.function = function

        if self.value:
            SoPValue.__init__(self,
                              name=value.get_name(),
                              tag_list=value.get_tag_list(),
                              func=value.get_func(),
                              desc=value.get_desc(),
                              type=value.get_type(),
                              bound=value.get_bound(),
                              format=value.get_format(),
                              cycle=value.get_cycle())
        elif self.function:
            SoPFunction.__init__(self,
                                 name=function.get_name(),
                                 tag_list=function.get_tag_list(),
                                 desc=function.get_desc(),
                                 func=function.get_func(),
                                 arg_list=function.get_arg_list(),
                                 return_type=function.get_return_type(),
                                 exec_time=function.get_exec_time(),
                                 timeout=function.get_timeout())
        else:
            raise Exception(
                '[SoPServiceInfo.__init__]: No value or function is given.')

        self._policy = policy
        self._thing_name = thing_name
        self._middleware_name = middleware_name
        self._hierarchy = hierarchy
        self._service_type = service_type
        self._is_alive = is_alive
        self._is_super = is_super

    def __eq__(self, o: object) -> bool:
        instance_check = isinstance(o, SoPValue) or isinstance(
            self.function, SoPFunction)
        if instance_check:
            if self.value:
                return SoPValue.__eq__(self, o)
            elif self.function:
                return SoPFunction.__eq__(self, o)
            else:
                raise Exception(
                    '[SoPServiceInfo.__eq__]: No value or function is given.')
        else:
            raise Exception(
                '[SoPServiceInfo.__eq__]: Not SoPValue or SoPFunction.')

    def get_policy(self):
        return self._policy

    def get_thing_name(self):
        return self._thing_name

    def get_middleware_name(self):
        return self._middleware_name

    def get_hierarchy(self):
        return self._hierarchy

    def get_service_type(self):
        return self._service_type

    def get_is_alive(self):
        return self._is_alive

    def get_is_super(self):
        return self._is_super
