from django.views.generic import View
from django.shortcuts import render_to_response
from django.http import JsonResponse
import requests
from models import Registry


class RegistryAdd(View):

    def get(self, request, *args, **kwargs):
        return render_to_response('docker_ui/registry/add.html')


class RegistryList(View):

    def get(self, request, *args, **kwargs):
        return render_to_response('docker_ui/registry/list.html')


class RegistryApi(View):
    perm = ['add', 'change', 'delete']

    def get(self, request, *args, **kwargs):
        data = requests.get('http://127.0.0.1:8000/v1/users')
        manager = [p for p in self.perm if request.user.has_perm(p)]
        data_list = []
        for d in data.json():
            d['manager'] = manager
            data_list.append(d)
        return JsonResponse({'data': data_list})
