#!/usr/bin/evn python
# -*- coding: utf-8 -*-
from docker import Client
from addict import Dict


class Docker(object):

    def __init__(self, base_url=None, host='localhost', port='2375', version='1.24'):
        if base_url is None:
            self.base_url = 'tcp://{host}:{port}'.format(host=host, port=port)
        else:
            self.base_url = base_url
        self.version = version
        self.client = Client(base_url=self.base_url)

    def login(self, username=None, password=None, registry=None):
        self.client.login(username=username, password=password, registry=registry)

    def images(self):
        _images = [Dict(image) for image in self.client.images()]
        return _images

    def pull_image(self, tags):
        try:
            repository, tags = tags.split(':')
        except ValueError:
            repository = tags
            tags = 'latest'
        return self.client.pull(repository, tag=tags)

    def containers(self, all=False):
        return [Dict(container) for container in self.client.containers(all=all)]

    def start_container(self, container_id):
        return self.client.start(container_id)

    def create_container(self, *args, **kwargs):
        return self.client.create_container(*args, **kwargs)

    def remove_container(self, container_id):
        self.client.stop(container_id, timeout=30)
        self.client.remove_container(container_id)

    def create_host_config(self, *args, **kwargs):
        """
        binds=None, port_bindings=None, lxc_conf=None,
                       publish_all_ports=False, links=None, privileged=False,
                       dns=None, dns_search=None, volumes_from=None,
                       network_mode=None, restart_policy=None, cap_add=None,
                       cap_drop=None, devices=None, extra_hosts=None,
                       read_only=None, pid_mode=None, ipc_mode=None,
                       security_opt=None, ulimits=None, log_config=None,
                       mem_limit=None, memswap_limit=None, mem_swappiness=None,
                       cgroup_parent=None, group_add=None, cpu_quota=None,
                       cpu_period=None, blkio_weight=None,
                       blkio_weight_device=None, device_read_bps=None,
                       device_write_bps=None, device_read_iops=None,
                       device_write_iops=None, oom_kill_disable=False,
                       shm_size=None, version=None, tmpfs=None,
                       oom_score_adj=None
        """

        return self.client.create_host_config(*args, **kwargs)

    def stop_container(self, container_id):
        return self.client.stop(container_id)

    def stats(self, container_id):
        return self.client.stats(container_id, stream=False)

    def __del__(self):
        self.client.close()
