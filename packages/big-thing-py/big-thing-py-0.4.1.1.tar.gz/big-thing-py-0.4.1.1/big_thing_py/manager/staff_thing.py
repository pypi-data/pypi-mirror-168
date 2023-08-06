from core.thing import *
from utils import *
from common import *


class SoPStaffThing(SoPThing):
    def __init__(self, name: str, service_list: List[SoPService], alive_cycle: float, device_id: str, is_super: bool = False):
        super().__init__(name, service_list, alive_cycle, is_super)
        self._device_id = device_id

    # TODO: Check this method works correct
    def __eq__(self, o: object) -> bool:
        return super().__eq__(o) and (o._device_id == self._device_id)

    def get_device_id(self) -> str:
        return self._device_id

    def set_device_id(self, id: str) -> None:
        self._device_id = id
