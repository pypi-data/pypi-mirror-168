import io
import json
import logging
import os
import random
import socket
import threading
import time
from functools import wraps

import nacos
import requests
from nacos.client import WatcherWrap, process_common_config_params
from nacos.commons import synchronized_with_attr

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
            thread = threading.Thread(target=self.health_check, args=(
                service_name, ip, port, cluster_name, group_name, weight, metadata, ))
            thread.start()
        except:
            logging.error("[regiser] failed!", exc_info=True)

    def health_check(self, service_name, ip, port, cluster_name, group_name, weight, metadata):
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

    def get_config(self, service_name=None):
        if service_name is not None and self.service_name is None:
            self.service_name = service_name
        self.client.set_options(no_snapshot=True)
        content = self.client.get_config('BASE-CONFIG', 'public')
        self.config = json.loads(content)
        return self.config

    @synchronized_with_attr("pulling_lock")
    def add_config_watcher(self, data_id, group, content=None):
        data_id, group = process_common_config_params(data_id, group)
        logger.info("[add-watcher] data_id:%s, group:%s, namespace:%s" % (data_id, group, self.namespace))
        cache_key = '+'.join([data_id, group, self.namespace])
        wl = self.client.watcher_mapping.get(cache_key)
        if not wl:
            wl = list()
            self.client.watcher_mapping[cache_key] = wl
        last_md5 = nacos.NacosClient.get_md5(content)
        cb = self.config_callback
        wl.append(WatcherWrap(cache_key, cb, last_md5))
        logger.info("[add-watcher] watcher has been added for key:%s, new callback is:%s, callback number is:%s" % (
            cache_key, cb.__name__, len(wl)))

        if self.client.puller_mapping is None:
            logger.debug("[add-watcher] pulling should be initialized")
            self.client._init_pulling()

        if cache_key in self.client.puller_mapping:
            logger.debug("[add-watcher] key:%s is already in pulling" % cache_key)
            return

        for key, puller_info in self.client.puller_mapping.items():
            if len(puller_info[1]) < self.client.pulling_config_size:
                logger.debug("[add-watcher] puller:%s is available, add key:%s" % (puller_info[0], cache_key))
                puller_info[1].append(cache_key)
                self.client.puller_mapping[cache_key] = puller_info
                break
        else:
            logger.debug("[add-watcher] no puller available, new one and add key:%s" % cache_key)
            key_list = self.client.process_mgr.list()
            key_list.append(cache_key)
            puller = threading.Thread(target=self.client._do_pulling, args=(key_list, self.client.notify_queue))
            puller.start()
            self.client.puller_mapping[cache_key] = (puller, key_list)

    def config_callback(self, data):
        if data and data.get('content', None) is not None:
            self.config = json.loads(data['content'])

    def get_service_host(self, service_name, clusters=None, group_name=None):
        logger.info("[get_service_host] service_name:%s, clusters:%s, group_name:%s" %
                    (service_name, clusters, group_name))

        service_data = self._service_map.get(service_name, {})
        if not service_data or int(time.time()) > service_data.get('timestamp') + 10:
            try:
                config_dic = self.client.list_naming_instance(
                    service_name, clusters, namespace_id=self.namespace, group_name=group_name, healthy_only=True)
                hosts = config_dic.get("hosts")
                self._service_map[service_name] = service_data = {
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
