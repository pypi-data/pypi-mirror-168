from big_thing import *
from utils.mqtt_util import *
from queue import Queue, Empty


class SoPMQTTMonitor:
    def __init__(self, name: str = None, host: str = '127.0.0.1', port: int = 1883, level: int = None, debug: bool = False):
        self._client: SoPClient = SoPClient(client_id=name, clean_session=True)
        self._client_id = name
        self._host = host
        self._port = port
        self._level = level
        self._debug = debug
        self._pub_message = None
        self._recv_message = None

        self._pub_message_queue: Queue = Queue()
        self._recv_message_queue: Queue = Queue()

        self._subscribe_list = set()
        self._is_run = False

        self.set_callback()

    def connect(self):
        try:
            self._client.connect(self._host, self._port)
        except Exception as e:
            time.sleep(0.1)

    def set_debug(self, debug: bool):
        self._debug = debug

    def set_callback(self):
        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect
        self._client.on_publish = self._on_publish
        self._client.on_subscribe = self._on_subscribe
        self._client.on_unsubscribe = self._on_unsubscribe
        self._client.on_message = self._on_message

    def publish(self, topic, payload, qos=2, retain=False):
        self._pub_message = encode_MQTT_message(topic, payload, time.time())
        ret = self._client.publish(topic, payload, qos, retain)
        if self._debug:
            if ret.rc == 0:
                pass
                SOPLOG_DEBUG(
                    f'{"✅ Published":>16}(qos={qos}): {topic:<80}, {payload} on {self._host}:{self._port}', 'yellow')
            else:
                pass
                SOPLOG_DEBUG(f'Publish failed...', 'red')

    def subscribe(self, topic: Union[List, str], qos=2):
        if type(topic) is not list:
            self._client.subscribe(topic, qos)
            self._subscribe_list.add(topic)
            if self._debug:
                SOPLOG_DEBUG(
                    f'{"✅ Subscribed":>16}(qos={qos}): {topic:<80}, on {self._host}:{self._port}', 'yellow')
        else:
            for item in topic:
                self._client.subscribe(item, qos)
                self._subscribe_list.add(item)
                if self._debug:
                    SOPLOG_DEBUG(
                        f'{"✅ Subscribed":>16}(qos={qos}): {item:<80}, on {self._host}:{self._port}', 'yellow')

    def unsubscribe(self, topic, properties=None):
        if type(topic) is not list:
            self._client.unsubscribe(topic, properties)
            if topic in self._subscribe_list:
                self._subscribe_list.remove(topic)
            if self._debug:
                SOPLOG_DEBUG(
                    f'{"❌ Unsubscribed":>16}: {topic:<80}, on {self._host}:{self._port}', 'yellow')
        else:
            for item in topic:
                self._client.unsubscribe(item, properties)
                if item in self._subscribe_list:
                    self._subscribe_list.remove(item)
                if self._debug:
                    SOPLOG_DEBUG(
                        f'{"❌ Unsubscribed":>16}: {item:<80}, on {self._host}:{self._port}', 'yellow')

    def loop_start(self):
        self._client.loop_start()

    def loop_stop(self):
        self._client.loop_stop()

    def run(self):
        if self._is_run:
            return self
        else:
            self.connect()
            self.loop_start()
            self._is_run = True
            # self.subscribe_predefine_topics()
            return self

    def stop(self):
        self.loop_stop()

    def recv_queue_clear(self):
        with self._recv_message_queue.mutex:
            self._recv_message_queue.queue.clear()

    def expect(self, target_topic: str = None, auto_subscribe: bool = True, auto_unsubscribe: bool = True, timeout: int = 10) -> Union[Tuple[str, dict], str]:
        if not self._is_run:
            self.run()

        try:
            if auto_subscribe:
                self.subscribe(target_topic)

            while True:
                cur_time = time.time()
                if timeout < 0:
                    raise Empty('Timeout')

                topic, payload, timestamp = decode_MQTT_message(
                    self._recv_message_queue.get(timeout=timeout))

                if target_topic:
                    topic_slice = topic.split('/')
                    target_topic_slice = target_topic.split('/')
                    for i in range(len(target_topic_slice)):
                        if target_topic_slice[i] not in ['#', '+'] and target_topic_slice[i] != topic_slice[i]:
                            break
                    else:
                        return topic, payload, timestamp
                else:
                    self._recv_message_queue.put(
                        encode_MQTT_message(topic, payload, timestamp))
                    timeout -= (time.time() - cur_time)
        except Empty as e:
            SOPLOG_DEBUG('SOPMQTTMonitor Timeout...', 'red')
            return None, None, None
        except Exception as e:
            raise e
        finally:
            if auto_unsubscribe:
                if target_topic:
                    self.unsubscribe(target_topic)

    def publish_and_expect(self, trigger_msg: mqtt.MQTTMessage = None, target_topic: str = None, auto_subscribe: bool = True, auto_unsubscribe: bool = True, timeout: int = 10):
        if not self._is_run:
            self.run()

        if auto_subscribe:
            self.subscribe(target_topic)
        trigger_topic, trigger_payload, timestamp = decode_MQTT_message(
            trigger_msg, mode=str)
        self.publish(trigger_topic, trigger_payload, retain=False)

        return self.expect(target_topic, False, auto_unsubscribe, timeout)

    # TODO: change command method to SoPElementConroller's method
    def command_and_expect(self, trigger_command: Union[List[str], str] = None, target_topic: str = None,
                           auto_subscribe: bool = True, auto_unsubscribe: bool = True, timeout: int = 10):
        if not self._is_run:
            self.run()

        if auto_subscribe:
            self.subscribe(target_topic)
        if isinstance(trigger_command, list):
            for command in trigger_command:
                os.system(command)
        else:
            os.system(trigger_command)
        return self.expect(target_topic, auto_subscribe, auto_unsubscribe, timeout)

    def _on_connect(self, client: SoPClient, userdata, flags, rc):
        pass
        # print(f'Connected with result code {rc}')

    def _on_disconnect(self, client, userdata, rc):
        pass
        # print(f'Disconnected with result code {rc}')

    def _on_log(self, client, userdata, level, buf):
        pass
        # print(f'Log: {buf}')

    def _on_subscribe(self, client, userdata, mid, granted_qos):
        pass

    def _on_unsubscribe(self, client, userdata, mid):
        pass

    def _on_publish(self, client, userdata, mid):
        pass
        # print(f'Published: {mid}')
        # print(f'Publish: {self.pub_message}')

    def _on_message(self, client: SoPClient, userdata, message: mqtt.MQTTMessage):
        self._recv_message = message
        self._recv_message_queue.put(message)
        qos = message.qos
        topic, payload, timestamp = decode_MQTT_message(message)

        if self._debug:
            SOPLOG_DEBUG(
                f'{"✅ Received":>16}(qos={qos}): {topic:<80}, {payload} on {self._host}:{self._port}', 'yellow')

        if isinstance(userdata, dict):
            func = userdata.get('function', None)
            func(self, userdata, message)
        else:
            pass


def main():
    client = SoPMQTTMonitor('mid1', '147.46.114.165', 21283)
    client.run()

    input('Press Enter to continue...')
    client.publish(
        'mid1',
        'MS/SCHEDULE/on_all/SuperThingTest_D45D64A628DB/SoPIoT-MW-thsvkd1_E45F01615B50/SoPIoT-MW-thsvkd1_E45F01615B50',
        '{ "scenario": "test1", "period": 0 }')

    input('Press Enter to continue...')
    client.publish(
        'mid1',
        'MS/SCHEDULE/on_all/SuperThingTest_D45D64A628DB/SoPIoT-MW-thsvkd1_E45F01615B50/SoPIoT-MW-thsvkd1_E45F01615B50',
        '{ "scenario": "test1", "period": 0 }')

    input('Press Enter to continue...')
    client.publish(
        'mid1',
        'MS/RESULT/SCHEDULE/on/BigThingTest_D45D64A628DB/SoPIoT-MW-thsvkd0_E45F016E0066/SuperThingTest_D45D64A628DB',
        '{ "error": 0, "scenario": "test1" }')


if __name__ == '__main__':
    main()
