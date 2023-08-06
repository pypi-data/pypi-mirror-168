from tests.tools.mqtt_monitor_client import *
from tests.tools.test_tools_common import *
from pathlib import Path
import datetime


def SOPTEST_LOG_DEBUG(msg: str, error: int, e: Exception = None):
    # error = 0  : PASS ✅
    # error = 1  : WARN ⚠ -> use b'\xe2\x9a\xa0\xef\xb8\x8f'.decode()
    # error = -1 : FAIL ❌
    log_msg = ''
    WARN_emoji = b'\xe2\x9a\xa0\xef\xb8\x8f'.decode()

    if error == 0:
        log_msg = f'[PASS✅] {msg} --> {str(e)}'
        SOPLOG_DEBUG(log_msg, 'green')
    elif error == 1:
        log_msg = f'[WARN{WARN_emoji} ] {msg} --> {str(e)}'
        SOPLOG_DEBUG(log_msg, 'yellow')
    elif error == -1:
        log_msg = f'[FAIL❌] {msg} --> {str(e)}'
        SOPLOG_DEBUG(log_msg, 'red')
        return e


def topic_seperator(topic: SoPProtocolType, back_num: int):
    topic_slice = topic.value.split('/')
    for _ in range(back_num):
        topic_slice.pop()

    result = '/'.join(topic_slice)
    return result


def get_mapped_thing_list(schedule_info: Dict, function_name: str = None, all_prefix: bool = False):
    if function_name:
        for mapping_info in schedule_info:
            if not all_prefix:
                if mapping_info['service'].split('.')[1] == function_name:
                    return mapping_info['things']
            elif mapping_info['service'].split('.')[1] == function_name and '*' in mapping_info['service']:
                return mapping_info['things']
    else:
        return [
            {
                'function_name': mapping_info['service'].split('.')[1],
                'thing_list': [thing['id'] for thing in mapping_info['things']]
            } for mapping_info in schedule_info
        ]


def len_no_ansi(string):
    import re
    return len(re.sub(
        r'[\u001B\u009B][\[\]()#;?]*((([a-zA-Z\d]*(;[-a-zA-Z\d\/#&.:=?%@~_]*)*)?\u0007)|((\d{1,4}(?:;\d{0,4})*)?[\dA-PR-TZcf-ntqry=><~]))', '', string))


def len_ansi(string):
    import re
    return len(string) - len(re.sub(
        r'[\u001B\u009B][\[\]()#;?]*((([a-zA-Z\d]*(;[-a-zA-Z\d\/#&.:=?%@~_]*)*)?\u0007)|((\d{1,4}(?:;\d{0,4})*)?[\dA-PR-TZcf-ntqry=><~]))', '', string))


def home_dir_append(path: str, user: str = None) -> str:
    if path:
        if user:
            return path.replace('~', f'/home/{user}')
        else:
            return path.replace('~', os.path.expanduser('~'))
    else:
        return path


def get_upper_path(path: str):
    path = Path(path)
    return path.parent.absolute()


def unixtime_to_date(unixtime: float = None):
    return datetime.datetime.fromtimestamp(0)


def exception_wrapper(func: Callable = None,
                      empty_case_func: Callable = None,
                      key_error_case_func: Callable = None,
                      else_case_func: Callable = None,
                      final_case_func: Callable = None,):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Empty as e:
            print_error(e)
            if empty_case_func:
                return empty_case_func()
        except KeyError as e:
            print_error(e)
            if key_error_case_func:
                return key_error_case_func()
        except Exception as e:
            if e is Empty:
                if empty_case_func:
                    return empty_case_func()
            elif e in [ValueError, IndexError, TypeError, KeyError]:
                print_error(e)
            else:
                if self.__class__.__name__ == 'Simulator':
                    self.wrapup()
            print_error(e)
            raise e
        finally:
            if final_case_func:
                final_case_func()
    return wrapper


def check_result_payload(payload: dict = None, element: str = None, name: str = None, action: str = None, check_error_code: bool = True):
    if payload is not None:
        if check_error_code:
            error_code = payload.get('error', None)
            error_string = payload.get('error_string', None)
            if error_code in [0, -4]:
                SOPTEST_LOG_DEBUG(
                    f'{element} {name} {action} checked!', 0)
                return True
            else:
                raise SOPTEST_LOG_DEBUG(
                    f'{element} {name} {action} failed...', -1,
                    Exception(f'error_code: {error_code}, error_string : {error_string}'))
                # return False
        else:
            return True
    else:
        SOPTEST_LOG_DEBUG(
            f'Payload was None!!!', -1)
        return False
