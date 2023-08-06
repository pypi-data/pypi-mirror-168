from tests.tools.test_tools_utils import SOPTEST_LOG_DEBUG
from utils import *

import time
from enum import Enum
import paramiko


class SoPElementController:
    def __init__(self, user: str = None, host: str = None, port: int = None, password: int = None) -> None:
        self._user = user
        self._host = host
        self._port = port
        self._password = password
        self._connected = None

        if self._user and self._host and self._port and self._password:
            self._ssh_client = self.connect()
            self._connected = True
        else:
            self._connected = False

    def set_config(self, user: str = None, host: str = None, port: int = None, password: str = None):
        if user:
            self._user = user
        if host:
            self._host = host
        if port:
            self._port = port
        if password:
            self._password = password

    def get_duplicate_proc_pid(self, proc_name: str, user: str = None,
                               local_ip: str = None, local_port: int = None, foreign_ip: str = None, foreign_port: int = None,
                               args: Union[List[str], str] = ''):

        def get_proc_info():
            netstat_result = None
            ps_ef_result = None

            if not self._connected:
                netstat_result: List[str] = os.popen(
                    f'netstat -nap 2> /dev/null | grep {proc_name}').read().split('\n')
                ps_ef_result: List[str] = os.popen(
                    f'ps -ef 2> /dev/null | grep {proc_name}').read().split('\n')
            else:
                netstat_result: List[str] = self.send_command(
                    f'netstat -nap | grep {proc_name}', False)
                ps_ef_result: List[str] = self.send_command(
                    f'ps -ef | grep {proc_name}', False)

            return ps_ef_result, netstat_result

        def parse_ps_ef_line(line: str):
            line = line.split()
            if len(line) < 1:
                return False
            else:
                return {
                    'user': line[0],
                    'pid': int(line[1]),
                    'proc_name': line[7].lstrip('./'),
                    'args': line[8:],
                }

        def parse_netstat_line(line: str):
            line = line.split()
            if len(line) < 1 or 'tcp6' in line:
                return False
            elif 'tcp' in line:
                return {
                    'local_ip': line[3].split(':')[0],
                    'local_port': int(line[3].split(':')[1]),
                    'foreign_ip': line[4].split(':')[0],
                    'foreign_port': int(line[4].split(':')[1]) if '*' not in line[4].split(':')[1] else 0,
                    'proc_name': '/'.join(line[6].split('/')[1:]).lstrip('./'),
                    'pid': int(line[6].split('/')[0])
                }

        ps_ef_result, netstat_result = get_proc_info()
        target_pid_list_netstat = []
        target_pid_list_ps_ef = []

        for line in ps_ef_result:
            parse_result = parse_ps_ef_line(line)
            if parse_result:
                proc_name_check = proc_name in parse_result['proc_name'].split(
                    '/')[-1]
                args_check = args in ' '.join(parse_result['args'])
                if proc_name_check and args_check:
                    target_pid_list_ps_ef.append(parse_result['pid'])

        for line in netstat_result:
            parse_result = parse_netstat_line(line)
            if parse_result:
                proc_name_check = proc_name in parse_result['proc_name']

                local_ip_check = local_ip == parse_result['local_ip']
                local_port_check = local_port == parse_result['local_port']
                foreign_ip_check = foreign_ip == parse_result['foreign_ip']
                foreign_port_check = foreign_port == parse_result['foreign_port']

                local_address_check = local_ip_check and local_port_check
                foreign_address_check = foreign_ip_check and foreign_port_check
                address_check = local_address_check or foreign_address_check

                if proc_name_check and address_check:
                    target_pid_list_netstat.append(parse_result['pid'])

        if not proc_name == 'python':
            target_pid_list = list(
                set(target_pid_list_netstat).intersection(target_pid_list_ps_ef))
        else:
            target_pid_list = list(set(target_pid_list_ps_ef))
        return target_pid_list

    def send_command(self, command: Union[List[str], str], ignore_result: bool = False) -> Union[bool, List[str]]:
        if isinstance(command, str):
            command = [command]

        for item in command:
            if self._connected:
                stdin, stdout, stderr = self._ssh_client.exec_command(item)
                if ignore_result:
                    return True
                else:
                    stdout_result = stdout.readlines()
                    return [line.strip() for line in stdout_result]
            else:
                result = os.popen(item)
                if ignore_result:
                    return True
                else:
                    return result.read().split('\n')

    def send_file(self, local_path: str, remote_path: str):
        if self._connected:
            self._ssh_client.open_sftp().put(local_path, remote_path)
        else:
            SOPTEST_LOG_DEBUG('Connect to host before send file', 1)

    def connect(self, user: str = None, host: str = None, port: int = None, password: str = None) -> paramiko.SSHClient:
        if not self._connected:
            self.set_config(user=user, host=host, port=port, password=password)

            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            if self._host != None and self._port != None and self._user != None and self._password != None:
                client.connect(self._host, port=self._port,
                               username=self._user.split('/')[-1], password=self._password)
            else:
                raise SOPTEST_LOG_DEBUG(
                    'Please set the user, host, port, password before connect to ssh host', -1)

        return client


if __name__ == '__main__':
    client = SoPElementController(
        user='pi', host='192.168.50.2', port=22, password='/PeaCE/')

    test_command = '''/sbin/mosquitto -c /home/pi/Workspace/middleware/src/middleware/middleware_level1_1_mosquitto.conf'''
    # test_command = '''mosquitto'''
    # test_command = '''
    # ls
    # '''
    ret = client.send_command(test_command, ignore_result=True)
    # ret = client.send_file('./expecter.py', '/home/pi/expecter.py')
    for ret_line in ret:
        print(ret_line)
