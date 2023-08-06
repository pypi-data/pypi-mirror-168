from core.tag import *

import copy


class SoPService(metaclass=ABCMeta):
    def __init__(self, name: str, tag_list: List[SoPTag], desc: str, func: Callable, energy: float) -> None:
        self._name: str = name

        # TODO: why only deepcopy make it works?
        self._tag_list: List[SoPTag] = copy.deepcopy(tag_list)
        # self._tag_list: List[SoPTag] = tag_list
        self._desc = desc
        self._func = func
        self._energy = energy

    def __eq__(self, o: object) -> bool:
        instance_check = isinstance(o, SoPService)
        name_check = (o._name == self._name)
        tag_list_check = (o._tag_list == self._tag_list)

        return instance_check and name_check and tag_list_check

    def add_tag(self, tag: SoPTag) -> None:
        self._tag_list.append(tag)

    @abstractmethod
    def dump(self) -> Dict:
        pass

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

    def get_name(self) -> str:
        return self._name

    def get_tag_list(self) -> List[SoPTag]:
        return self._tag_list

    def get_desc(self) -> str:
        return self._desc

    def get_func(self) -> Callable:
        return self._func

    def get_energy(self) -> float:
        return self._energy

    # ==================================
    #             _    _
    #            | |  | |
    #  ___   ___ | |_ | |_   ___  _ __
    # / __| / _ \| __|| __| / _ \| '__|
    # \__ \|  __/| |_ | |_ |  __/| |
    # |___/ \___| \__| \__| \___||_|
    # ==================================

    def set_name(self, name: str) -> None:
        self._name = name

    def set_tag_list(self, tag_list: List[SoPTag]) -> None:
        self._tag_list = tag_list

    def set_desc(self, desc: str) -> None:
        self._desc = desc

    def set_func(self, func: Callable) -> None:
        self._func = func

    def set_func(self, energy: float) -> None:
        self._energy = energy
