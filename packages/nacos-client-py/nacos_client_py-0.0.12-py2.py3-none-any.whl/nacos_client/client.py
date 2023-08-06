import io
import json
import logging
import os
import random
import socket
import ssl
import threading
import time
from functools import wraps
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import nacos
import requests

logging.basicConfig()
logger = logging.getLogger(__name__)


class NacosClientException(Exception):
    pass


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        return s.getsockname()[0]
    finally:
        s.close()


class NacosClient:
    debug = False
    config = {}

    def set_debugging(self):
        if not self.debug:
            global logger
            logger.info('debuging...')
            logger = logging.getLogger("nacos_client")
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s:%(message)s"))
            logger.addHandler(handler)
            logger.setLevel(level=logging.DEBUG)
            self.debug = True
            self.client.set_debugging()

    def __init__(self, server_addresses, namespace=None, username=None, password=None):
        self.server_address = server_addresses
        self.namespace = namespace
        self.client = nacos.NacosClient(server_addresses, namespace=namespace, username=username, password=password)
        self.pulling_lock = self.client.pulling_lock
        self._service_map = {}
        self.service_name = None

    def register(self, service_name, ip, port, cluster_name='DEFAULT', group_name='public', weight=1, metadata=None):
        self.service_name = service_name
        cluster, group = os.environ.get('WCloud_Cluster'), os.environ.get('WCloud_Cluster_Group')
        if cluster and group:
            cluster_name = f'{cluster}__{group}'
        if metadata is None:
            metadata = {}
        logger.info("[register] service_name:%s, ip:%s, port:%s, cluster_name:%s, group_name:%s, weight:%s" % (
            service_name, ip, port, cluster_name, group_name, weight))
        try:
            re = self.client.add_naming_instance(
                service_name, ip, port, cluster_name=cluster_name, group_name=group_name, weight=weight, metadata=metadata)
            logger.info(f"[register] success! {re}")
            thread = threading.Thread(target=self._health_check, args=(
                service_name, ip, port, cluster_name, group_name, weight, metadata, ))
            thread.daemon = True
            thread.start()
        except:
            logging.error("[regiser] failed!", exc_info=True)

    def _health_check(self, service_name, ip, port, cluster_name, group_name, weight, metadata):
        logger.info("[health_check] service_name:%s, ip:%s, port:%s, cluster_name:%s, group_name:%s, weight:%s" % (
            service_name, ip, port, cluster_name, group_name, weight))
        while True:
            time.sleep(5)
            try:
                result = self.client.send_heartbeat(
                    f'{group_name}@@{service_name}', ip, port, cluster_name=cluster_name, weight=weight, group_name=group_name, metadata=metadata)
                if result.get('code') != 10200:
                    logger.info(f'[send_heartbeat] failed! register again')
                    self.register(service_name, ip, port, cluster_name=cluster_name,
                                  group_name=group_name, weight=weight)
                    break
            except:
                logging.error("[send_heartbeat] error!", exc_info=True)

    def add_config_listener(self, service_name=None):
        if service_name is not None and self.service_name is None:
            self.service_name = service_name
        thread = threading.Thread(target=self._config_listener, args=('BASE-CONFIG', 'public', 30000, ))
        thread.daemon = True
        thread.start()

    def _config_listener(self, data_id, group, timeout=None, no_snapshot=True, content=None):
        while True:
            try:
                content_md5 = self.client.get_md5(content)
                url = f'{self.server_address}/nacos/v1/cs/configs/listener?username={self.client.username}&password={self.client.password}'
                data = {'Listening-Configs': f'{data_id}\x02{group}\x02{content_md5}\x02{self.namespace}\x01'}
                headers = {"Long-Pulling-Timeout": timeout}
                req = Request(url, data=urlencode(data).encode(), headers=headers, method='POST')
                ctx = ssl.SSLContext()
                resp = urlopen(req, timeout=timeout + 10, context=ctx)
                if resp.read().decode():
                    content = self.client.get_config(data_id, group, no_snapshot=no_snapshot)
                    self.config = json.loads(content)
            except:
                logging.error("[config_listener] error!", exc_info=True)

    def get_service_host(self, service_name, clusters=None, group_name=None):
        logger.info("[get_service_host] service_name:%s, clusters:%s, group_name:%s" %
                    (service_name, clusters, group_name))
        key = f'{service_name}:{clusters}:{group_name}'
        service_data = self._service_map.get(key, {})
        if not service_data or int(time.time()) > service_data.get('timestamp') + 10:
            try:
                config_dic = self.client.list_naming_instance(
                    service_name, clusters, namespace_id=self.namespace, group_name=group_name, healthy_only=True)
                hosts = config_dic.get("hosts")
                self._service_map[key] = service_data = {
                    'timestamp': int(time.time()),
                    'hosts': [f"{i['ip']}:{i['port']}" for i in hosts]
                }
            except Exception as e:
                logger.error(f'[get_service_host] api error! service: {service_name}, error:{str(e)}')
                return None
        return random.choice(service_data['hosts']) if service_data['hosts'] else None

    def request(self, service, path, method, clusters=None, group_name='public', https=False):
        def decorate(func):
            @wraps(func)
            def wrapper(**kwargs):
                host = self.get_service_host(service, clusters=clusters, group_name=group_name)
                if not host:
                    raise NacosClientException(f'no service avaliable! service: {service}')
                # 自动鉴权
                if self.service_name in self.config.get('service_tokens', {}) and not kwargs.get('headers', {}).get('Authorization'):
                    headers = kwargs.get('headers', {})
                    headers['Authorization'] = 'Token ' + self.config['service_tokens'][self.service_name]['token']
                    kwargs['headers'] = headers
                url = f'{"https" if https else "http"}://{host}{path}'
                return requests.request(method, url, **kwargs)
            return wrapper
        return decorate
