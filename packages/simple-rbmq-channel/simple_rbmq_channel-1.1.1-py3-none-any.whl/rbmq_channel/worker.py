import time
import datetime
import signal
import logging
from typing import Optional
from abc import ABC, abstractmethod

from rbmq_channel.channel import RBMQChannel

logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging
logger = logger.getLogger(__name__)

RUNNING = True


def signal_handler(signum, frame):
    logger.warning(f'Signal number: {signum}: Frame {frame}')
    global RUNNING
    RUNNING = False
    logger.warning('Exit')


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


class RBMQWorker(ABC):
    def __init__(
            self,
            config: dict,
            read_queue: str,
            write_queue: Optional = None,
            stop_if_empty: bool = True,
            sleep_if_empty: int = 100
    ):
        self.read_channel = RBMQChannel(auth=config, queue_name=read_queue)
        self.write_channel = RBMQChannel(auth=config, queue_name=write_queue) if write_queue else None
        self.stop_if_empty = stop_if_empty
        self.sleep_if_empty = sleep_if_empty
        super().__init__()

    @abstractmethod
    def handle_event(self, event):
        pass

    def get_event(self):
        event, method_frame = self.read_channel.get_event()

        if method_frame:
            return event, method_frame

        return None, None

    def run(self):
        while RUNNING:
            event, method_frame = self.get_event()
            if event:
                self.handle_event(event)
                self.read_channel.channel.basic_ack(method_frame.delivery_tag)
            else:
                if self.stop_if_empty:
                    logger.warning(f'{datetime.datetime.now()}: Queue {self.read_channel.queue_name} is empty: STOP')
                    break
                if self.sleep_if_empty:
                    logger.warning(f'{datetime.datetime.now()}: Queue {self.read_channel.queue_name} '
                                   f'is empty SLEEP : {self.sleep_if_empty}')
                    time.sleep(self.sleep_if_empty)




