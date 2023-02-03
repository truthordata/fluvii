from confluent_kafka.schema_registry import SchemaRegistryClient
from urllib.parse import urlparse, quote


# fixes a bug in confluent-kafka TODO: keep a look out for this in >1.8.2, should be fixed since I took it from a MR.
def patched_schema_loads(schema_str):
    from confluent_kafka.schema_registry.avro import Schema
    schema_str = schema_str.strip()
    if schema_str[0] != "{" and schema_str[0] != "[":
        schema_str = '{"type":' + schema_str + '}'
    return Schema(schema_str, schema_type='AVRO')


import confluent_kafka
confluent_kafka.schema_registry.avro._schema_loads = patched_schema_loads
import logging
from .config import SchemaRegistryConfig

LOGGER = logging.getLogger(__name__)


class SchemaRegistry:
    def __init__(self, config=SchemaRegistryConfig(), auto_init=True):
        self.registry = None
        self._url = config.url
        self._started = False
        if auto_init:
            self.start()

    def __getattr__(self, attr):
        """Note: this includes methods as well!"""
        try:
            return self.__getattribute__(attr)
        except AttributeError:
            return self.registry.__getattribute__(attr)

    def _init_registry(self):
        url = urlparse(self._url)
        auth = ''
        if self.username:
            auth = f"{quote(self.username)}:{quote(self.password)}@"
        scheme = url.scheme
        if scheme:
            url = url._replace(path=url.netloc, netloc='')
        else:
            if auth:
                scheme = 'https'
            else:
                scheme = 'http'
        url = url._replace(scheme='')
        self.registry = SchemaRegistryClient({'url': f'{scheme}://{auth}{url.geturl()}'})
        LOGGER.info('Registry client initialized successfully!')

    def start(self):
        if not self._started:
            self._init_registry()
            self._started = True
