from big_thing_py.core.argument import *
from big_thing_py.core.service import *
from big_thing_py.common.thread import *

from func_timeout import func_timeout, FunctionTimedOut, func_set_timeout
from multiprocessing import Pool, TimeoutError


class SoPFunction(SoPService):

    def __init__(self, name: str = '', tag_list: List[SoPTag] = [], desc: str = '', func: Callable = None, energy: float = None,
                 arg_list: List[SoPArgument] = [], return_type: SoPType = SoPType.UNDEFINED, exec_time: float = 1000 * 10,
                 timeout: float = 1000 * 10, policy: SoPPolicy = SoPPolicy.SINGLE) -> None:
        super().__init__(name=name, tag_list=tag_list, desc=desc, func=func, energy=energy)

        self._arg_list = arg_list
        self._return_type = return_type
        self._return_value = None
        self._exec_time = exec_time
        self._timeout = timeout
        self._thread: SoPThread = None

        self._running: bool = False
        # TODO: is it necessary? -> only used for super function feature
        self._policy = policy

        # Queue
        self._result_queue = Queue()

    def __eq__(self, o: object) -> bool:
        arg_list_check = o._arg_list == self._arg_list
        return_type_check = o._return_type == self._return_type
        exec_time_check = o._exec_time == self._exec_time
        timeout_check = o._timeout == self._timeout

        return super().__eq__(o) and arg_list_check and return_type_check and exec_time_check and timeout_check

    def wrapper(self, execute_request: Union[ExecuteRequest, SuperExecuteRequest]) -> bool:
        SOPLOG_DEBUG(
            f'[FUNC RUN] run {self._thread.get_name()} function', 'green')

        if type(execute_request) == ExecuteRequest:
            function_name, thing_name, scenario_name, is_parallel, arg_list = execute_request.unpack()
            execute_result = ExecuteResult()
        elif type(execute_request) == SuperExecuteRequest:
            function_name, super_thing_name, super_middleware_name, requester_middleware_name, \
                _, thing_name, arg_list, scenario_name, is_parallel = execute_request.unpack()
            execute_result = SuperExecuteResult(super_thing_name=super_thing_name,
                                                super_function_name=function_name,
                                                super_middleware_name=super_middleware_name,
                                                requester_middleware_name=requester_middleware_name)

        running_scenario_hash = execute_request.get_user_date()
        real_arguments = self.decode_arguments(arg_list)

        if not is_parallel and self._running:
            while self._running:
                SOPLOG_DEBUG(
                    '[FUNC WAITING] wait fot previous function execution request finish...', 'yellow')
                time.sleep(0.2)
        try:
            self._running = True

            if not function_name == self._name:
                raise Exception(
                    '[FUNC ERROR] self._name was not match to request function_name')

            self._return_value = func_timeout(
                self._timeout/1000, self._func, args=(*real_arguments, ))

        except KeyboardInterrupt as e:
            # TODO: for warpup main thread, but not test it yet
            print_error(e)
            SOPLOG_DEBUG('Ctrl + C Exit', 'red')
            raise Exception('Ctrl + C Exit')
        except FunctionTimedOut as e:
            print_error(e)
            SOPLOG_DEBUG(
                f'[FUNC TIMEOUT] function {self._thread.get_name()} timeout!!!', 'red')
            execute_result.error = SoPErrorType.TIMEOUT
        except Exception as e:
            print_error(e)
            execute_result.error = SoPErrorType.EXECUTE_FAIL
            SOPLOG_DEBUG(
                f'[FUNC ERROR] function {self._thread.get_name()} error while execute function!!!', 'red')
        else:
            execute_result.error = SoPErrorType.NO_ERROR
            execute_result.return_value = self._return_value
            SOPLOG_DEBUG(
                f'[FUNC FINISH] function {self._name} finish. -> return value : {self._return_value}', 'green')
        finally:
            execute_result.thing_name = thing_name
            execute_result.function_name = function_name
            execute_result.scenario_name = scenario_name
            execute_result.return_type = self._return_type
            self._running = False
            if self._name in running_scenario_hash:
                self._result_queue.put(execute_result)
                return True
            else:
                SOPLOG_DEBUG(
                    f'[FUNC 404] function {self._name} was not in running scenario_hash', 'red')
                self._result_queue.put(execute_result)
                return False

    def execute(self, execute_request: Union[ExecuteRequest, SuperExecuteRequest]) -> None:
        self._thread = SoPThread(
            func=self.wrapper,
            name=f'{self._func.__name__}_thread',
            daemon=True,
            arg_list=(execute_request, ))
        self._thread.start()

    def set_execute_result_queue(self, queue: Queue):
        self._result_queue = queue

    def decode_arguments(self, arg_list: Tuple) -> Tuple[Tuple, str]:
        index = 0
        real_arguments = ()

        for arg in arg_list:
            if int(arg['order']) == index:
                real_arguments += (arg['value'], )
                index += 1
        return real_arguments

    def dump(self) -> Dict:
        return {
            "name": self._name,
            "description": self._desc,
            "exec_time": self._exec_time if self._exec_time is not None else 0,
            "return_type": self._return_type.value,
            "energy": self._energy,
            "tags": [tag.dump() for tag in self._tag_list],
            "use_arg": 1 if self._arg_list else 0,
            "arguments": [argument.dump() for argument in self._arg_list] if self._arg_list else []
        }

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

    def get_exec_time(self) -> float:
        return self._exec_time

    def get_timeout(self) -> float:
        return self._timeout

    def get_arg_list(self) -> List[SoPArgument]:
        return self._arg_list

    def get_return_type(self) -> SoPType:
        return self._return_type

    def get_running(self) -> bool:
        return self._running

    def get_policy(self) -> SoPPolicy:
        return self._policy

    # ==================================
    #             _    _
    #            | |  | |
    #  ___   ___ | |_ | |_   ___  _ __
    # / __| / _ \| __|| __| / _ \| '__|
    # \__ \|  __/| |_ | |_ |  __/| |
    # |___/ \___| \__| \__| \___||_|
    # ==================================

    def set_exec_time(self, exec_time: float) -> None:
        self._exec_time = exec_time

    def set_timeout(self, timeout: float) -> None:
        self._timeout = timeout

    def set_arg_list(self, arg_list: List[SoPArgument]) -> None:
        self._arg_list = arg_list

    def set_return_type(self, return_type: SoPType) -> None:
        self._return_type = return_type

    def set_running(self, running: bool) -> None:
        self._running = running

    def set_policy(self, policy: SoPPolicy) -> None:
        self._policy = policy
