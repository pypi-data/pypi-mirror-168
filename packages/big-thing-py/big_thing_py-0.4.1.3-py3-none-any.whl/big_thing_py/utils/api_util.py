from common import *
from utils import *
import requests


def API_response_check(res: requests.Response):
    if res.status_code != 200:
        return False
    else:
        return res


def API_request(url, header='', body='', login_retry=False,
                verify=False, method=RequestMethod.GET) -> Dict:
    try:
        if method == RequestMethod.GET:
            res = requests.get(url, headers=header, verify=False)
            if API_response_check(res):
                data = res.json()
                return data
            else:
                return False
        elif method == RequestMethod.POST:
            # 'https://goqual.io/openapicontrol/eb65ca597dbc149d4esv4q'
            # {'Authorization': 'Bearer 1e9bb043-3525-4a44-924c-f645dcb56f52', 'Accept': '*/*', 'Connection': 'close', 'Content-Type': 'application/json;charset-UTF-8'}
            # '{\n    "requirments": {\n        "power1": true\n    }\n}'
            res = requests.post(url, headers=header, data=body, verify=False)
            if API_response_check(res):
                return res
            else:
                return False
        elif method == RequestMethod.PUT:
            res = requests.put(url, headers=header, data=body, verify=False)
            if API_response_check(res):
                return res
            else:
                return False
        elif method == RequestMethod.DELETE:
            SOPLOG_DEBUG('Not implement yet')
        else:
            SOPLOG_DEBUG(
                f'[decode_MQTT_message] Unexpected request!!!', 'red')
    except Exception as e:
        print_error(e)
        return False
