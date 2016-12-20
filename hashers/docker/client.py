#!/usr/bin/evn python
# -*- coding: utf-8 -*-
from docker import Client


class Docker(object):

    def __init__(self, host='localhost', port='2375', registry=None, version='1.24'):
        self.base_url = 'tcp://{host}:{port}'.format(host=host, port=port)
        self.version = version
        self.client = self.__get_client
        if registry is not None:
            self.login_registry(**registry)

    @property
    def __get_client(self):
        return Client(base_url=self.base_url, version=self.version, timeout=5)

    def login_registry(self, username=None, password=None, registry=None):
        self.client.login(username=username, password=password, registry=registry)

    def images(self):
        def map_func(info):
            if info['RepoTags'] is None:
                return [info['Id'][7:][0:12], info['RepoDigests'][0].split('@')[0], 'None']
            temp = []
            for tag in info['RepoTags']:
                temp += [info['Id'][7:][0:12]] + tag.split(':')
            return temp

        return map(map_func, self.client.images())

    def pull_image(self, tags):
        try:
            repository, tags = tags.split(':')
        except ValueError:
            repository = tags
            tags = 'latest'
        return self.client.pull(repository, tag=tags)

    def containers_list(self):
        return self.client.containers(all=True)

    def start_container(self, container_id):
        return self.client.start(container_id)

    def create_container(self, *args, **kwargs):
        return self.client.create_container(*args, **kwargs)

    def logs(self):
        self.client.logs()

    def remove_container(self, container_id):
        self.client.stop(container_id, timeout=30)
        self.client.remove_container(container_id)

    def create_host_config(self, *args, **kwargs):
        return self.client.create_host_config(*args, **kwargs)

    def stop_container(self, container_id):
        return self.client.stop(container_id)

    def stats(self, container_id):
        return self.client.stats(container_id, stream=False)

    def __del__(self):
        self.client.close()
