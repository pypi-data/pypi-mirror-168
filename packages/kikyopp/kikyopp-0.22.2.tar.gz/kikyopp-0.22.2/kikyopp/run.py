import base64
import io
import logging
import signal

import requests
import yaml

from kikyopp.utils.logging import configure_logger
from kikyopp.worker import BaseWorker

log = logging.getLogger(__name__)


def run_worker(worker_cls, config_url: str, debug=False):
    log_level = 'debug' if debug else 'info'
    configure_logger('kikyopp', log_level)

    try:
        conf = _configure_by_consul(config_url)
        conf['debug'] = debug
        worker = worker_cls(conf)
        _set_signal_handlers(worker)
        worker.start()
    except Exception as e:
        log.error('Failed to start worker: %s', e, exc_info=True)


def _configure_by_consul(config_url) -> dict:
    resp = requests.get(config_url)
    resp.raise_for_status()
    v = resp.json()[0]['Value']
    s = base64.b64decode(v)
    conf = yaml.safe_load(io.BytesIO(s))
    return conf


def _set_signal_handlers(worker: BaseWorker):
    def _exit(signum, frame):
        log.info('Received exit signal: %s', signum)
        worker.stop()

    signal.signal(signal.SIGINT, _exit)
    signal.signal(signal.SIGTERM, _exit)
