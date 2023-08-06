import inspect
import json
import logging
import threading
from collections import defaultdict
from functools import partial

from kikyo import Kikyo, DataHub
from kikyo.settings import Settings

from kikyopp.annotation import KIKYOPP_SOURCE, KIKYOPP_SINK
from kikyopp.consumer.base import BaseConsumer
from kikyopp.consumer.kikyo import KikyoConsumer

log = logging.getLogger(__name__)


class BaseWorker:
    name: str
    kikyo: Kikyo
    consumer: BaseConsumer

    def __init__(self, settings: dict):
        self.settings = Settings(settings)

        log.info('settings: %s', json.dumps(self.settings, ensure_ascii=False, indent=4))

        assert self.name is not None
        self.debug = self.settings.get('debug', False)
        self.workers = self.settings.get('workers', 1)

        self._sink = None
        self._sink_method = None
        self._source = None
        self._source_method = None
        self._producer = None

        self._source = defaultdict(list)
        for name in dir(self):
            method = getattr(self, name)
            if inspect.ismethod(method):
                if hasattr(method, KIKYOPP_SOURCE):
                    self._source = getattr(method, KIKYOPP_SOURCE)
                    self._source_method = method
                if hasattr(method, KIKYOPP_SINK):
                    self._sink = getattr(method, KIKYOPP_SINK)
                    self._sink_method = method

        self.is_running = False

        self._init_components()
        if self._sink:
            self._producer = self.kikyo.component(cls=DataHub).create_producer(self._sink)

    def _init_components(self):
        from kikyo import configure_by_consul

        self.kikyo = configure_by_consul(self.settings['kikyo_config_url'])
        self.consumer = KikyoConsumer(self)

    def start(self):
        if self.is_running:
            return

        if not self._source:
            log.warning('No defined source')

        self.is_running = True

        jobs = []
        for i in range(self.workers):
            jobs.append(
                threading.Thread(target=partial(self.consumer.run, self._source))
            )
        for i in jobs:
            i.start()
        for i in jobs:
            i.join()
            log.warning('Thread is done')

    def process(self, data: dict):
        try:
            res = self._source_method(data)
            if res:
                if self._sink:
                    if not isinstance(res, list):
                        res = [res]
                    for r in res:
                        self._producer.send(r)
                        self._sink_method(r)
        except Exception as e:
            log.error(f'Error occurred: {e}', exc_info=True)

    def stop(self):
        if not self.is_running:
            return
        self.is_running = False
        self.consumer.stop()
