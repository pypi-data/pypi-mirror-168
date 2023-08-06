from redis.exceptions import ConnectionError
from threading import Thread
from queue import Queue, Empty
import redis
import time
import json


class IotRedisSubscriber(Thread):
    """Class for consume info, inheritance Thread

    This class provides basic connetion to redis and consumes
    a list of channels to subscribe when is started.
    func_handler can be parsed to develop async distribution of data
    to a custom function.
    """

    def __init__(self, *channels_to_consume: str, func_handler=None) -> None:
        super().__init__()
        self.daemon = True
        self.data_list = Queue()
        self.init_channels = list(channels_to_consume)
        self.func_handler = func_handler
        # Create redis database client
        self.rdb = redis.Redis(
            host='localhost',
            port=6379,
            charset="utf-8",
            decode_responses=True,
            db=0
        )
        # Create pubsub instance for subscribe
        self.pubsub = self.rdb.pubsub(ignore_subscribe_messages=True)

    @property
    def channels(self):
        return self.pubsub.channels

    def run(self) -> None:
        # Subscribe
        self._subscribe_channels(*self.init_channels)
        print("Run IotRedis Consumer: Init Consumer and channels")
        while True:
            try:
                self.pubsub.ping()
                print("Ping successful")
                self.listen()
            except ConnectionError as err:
                print("Problem trying to listen, relisten...")
            except AttributeError as err:
                print("None type of msg")

    def listen(self) -> None:
        for msg in self.pubsub.listen():
            if msg is not None and isinstance(msg, dict):
                # Save info in queue.
                if self.func_handler is not None:
                    self.func_handler((msg['channel'], msg['data']))
                else:
                    self.data_list.put((msg['channel'], msg['data']))

    def _subscribe_channels(self, *channels_to_consume: str) -> None:
        while True:
            try:  # Suscribe to every channel
                self.pubsub.subscribe(*channels_to_consume)
            except ConnectionError as err:
                print(f"Error trying to connect to server: {err}")
                time.sleep(1)
            else:  # If no error
                print("Connected to subscribe")
                break

    def data_available(self) -> bool:
        return not self.data_list.empty()

    def retrieve_data(self) -> tuple:
        try:
            return self.data_list.get_nowait()
        except Empty as _:
            return


class IotRedisPublisher(object):
    def __init__(self) -> None:
        super().__init__()
        # Create redis database client
        self.rdb = redis.Redis(
            host='localhost',
            port=6379,
            charset="utf-8",
            decode_responses=True,
            db=0
        )

    def publish(self, channel: str, data: dict) -> None:
        try:  # Publish data to channel
            if not isinstance(data, dict):
                raise TypeError("Type has to be a dictionary")
            return self.rdb.publish(channel, json.dumps(data))
        except ConnectionError as err:
            print("error trying to publish")


if __name__ == '__main__':
    sample_consumer = IotRedisSubscriber('prueba1', 'prueba2')
    sample_consumer.start()
    while True:
        try:
            pass
        except KeyboardInterrupt as _:
            break
    print("Simulation ended")
