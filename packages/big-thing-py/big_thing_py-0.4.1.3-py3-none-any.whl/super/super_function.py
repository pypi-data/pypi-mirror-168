from core.function import *


class SoPSuperFunction(SoPFunction):
    def __init__(self, name: str = '', tag_list: List[SoPTag] = ..., desc: str = '', func: Callable = None, energy: float = None,
                 arg_list: List[SoPArgument] = ..., return_type: SoPType = ..., exec_time: float = 1000 * 10, timeout: float = 1000 * 10, policy: SoPPolicy = ...) -> None:
        super().__init__(name, tag_list, desc, func, energy,
                         arg_list, return_type, exec_time, timeout, policy)

        self._subfunction_list: List[SoPFunction] = []
        self._requester_middleware_name: str = None
        self._first_execute: bool = True

    def add_subfunction(self, subfunction: SoPFunction):
        if not subfunction in self._subfunction_list:
            self._subfunction_list.append(subfunction)

    def remove_subfunction(self, subfunction: SoPFunction):
        if subfunction in self._subfunction_list:
            self._subfunction_list.remove(subfunction)

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

    def get_subfunction_list(self) -> List[SoPFunction]:
        return self._subfunction_list

    def get_requester_middleware_name(self) -> str:
        return self._requester_middleware_name

    def get_first_execute(self) -> bool:
        return self._first_execute

    # ==================================
    #             _    _
    #            | |  | |
    #  ___   ___ | |_ | |_   ___  _ __
    # / __| / _ \| __|| __| / _ \| '__|
    # \__ \|  __/| |_ | |_ |  __/| |
    # |___/ \___| \__| \__| \___||_|
    # ==================================

    def set_subfunction_list(self, target_subfunction_list: List[SoPFunction]) -> None:
        self._subfunction_list = target_subfunction_list

    def set_request_middleware_name(self, requester_middleware_name: str) -> None:
        self._requester_middleware_name = requester_middleware_name

    def set_first_execute(self, first_execute: bool) -> None:
        self._first_execute = first_execute
