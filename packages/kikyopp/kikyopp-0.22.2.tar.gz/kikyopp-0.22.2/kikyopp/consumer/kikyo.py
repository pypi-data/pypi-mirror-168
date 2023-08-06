import logging
import threading
import time

from kikyo import Kikyo, DataHub

from kikyopp.consumer.base import BaseConsumer

log = logging.getLogger(__name__)


class KikyoConsumer(BaseConsumer):

    def __init__(self, worker):
        self.worker = worker
        self.is_running = True
        self.consumer = None
        self._delay = self.worker.settings.get('consumer_delay')
        self._lock = threading.Lock()

    @property
    def kikyo(self) -> Kikyo:
        return self.worker.kikyo

    @property
    def worker_name(self) -> str:
        return self.worker.name

    def run(self, name):
        with self._lock:
            if self.consumer is None:
                datahub = self.kikyo.component(cls=DataHub)
                self.consumer = datahub.subscribe(
                    name,
                    subscription_name=f'kikyopp.{self.worker_name}',
                    auto_ack=False,
                )

        while self.is_running:
            try:
                if not self.is_running:
                    break
                with self._lock:
                    msg = self.consumer.receive()

                if self._delay is not None:
                    t = msg.publish_time.timestamp() + self._delay - time.time()
                    if t > 600:
                        log.warning(f'Need to wait {t} seconds')
                    if t > 1:
                        time.sleep(t)

                data = msg.value
                self.worker.process(data)
                if not self.worker.debug:
                    self.consumer.ack(msg)
            except Exception as e:
                log.error(f'Error when consume data: {e}')

    def stop(self):
        self.is_running = False
