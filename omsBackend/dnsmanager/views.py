# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import viewsets
from rest_framework.response import Response
from dnsmanager.models import DnsApiKey
from dnsmanager.serializers import DnsApiKeySerializer, DnspodDomainSerializer, DnspodRecordSerializer, \
    GodaddyDomainSerializer, GodaddyRecordSerializer
from dnsmanager.dnspod_api import DnspodApi
from dnsmanager.dnspod_key import DMSPOD_KEYINFO
from dnsmanager.godaddy_api import GodaddyApi
from dnsmanager.godaddy_key import GODADDY_KEYINFO


class DnsApiKeyViewSet(viewsets.ModelViewSet):
    queryset = DnsApiKey.objects.all()
    serializer_class = DnsApiKeySerializer
    filter_fields = ['name']


class DnspodDomainViewSet(viewsets.ViewSet):
    serializer_class = DnspodDomainSerializer

    def list(self, request):
        dnsapi = DnspodApi(user=DMSPOD_KEYINFO['user'], pwd=DMSPOD_KEYINFO['pwd'])
        query = dnsapi.get_domains()
        serializer = DnspodDomainSerializer(query, many=True)
        return Response(serializer.data)


class DnspodRecordViewSet(viewsets.ViewSet):
    serializer_class = DnspodRecordSerializer

    def list(self, request):
        dnsapi = DnspodApi(user=DMSPOD_KEYINFO['user'], pwd=DMSPOD_KEYINFO['pwd'])
        domain = request.GET['domain']
        query = dnsapi.get_records(domain)
        serializer = DnspodRecordSerializer(query, many=True)
        return Response(serializer.data)

    def post(self, request, record_type="A", ttl=600):
        dnsapi = DnspodApi(user=DMSPOD_KEYINFO['user'], pwd=DMSPOD_KEYINFO['pwd'])
        domain = request.data['domain']
        if request.data['action'] == 'create':
            sub_domain = request.data['sub_domain']
            value = request.data['value']
            record_type = request.data.get('record_type', record_type)
            ttl = request.data.get('ttl', ttl)
            query = dnsapi.add_record(domain, sub_domain, value, record_type, ttl=ttl)
        elif request.data['action'] == 'update':
            sub_domain = request.data['sub_domain']
            value = request.data['value']
            record_type = request.data.get('record_type', record_type)
            ttl = request.data.get('ttl', ttl)
            record_id = request.data['record_id']
            query = dnsapi.update_record(domain, record_id, sub_domain, value, record_type, ttl=ttl)
        elif request.data['action'] == 'remove':
            record_id = request.data['record_id']
            query = dnsapi.delete_record(domain, record_id)
        return Response(query)


class GodaddyDomainViewSet(viewsets.ViewSet):
    serializer_class = GodaddyDomainSerializer

    def list(self, request):
        godaddy = GodaddyApi(api_key=GODADDY_KEYINFO['key'], api_secret=GODADDY_KEYINFO['secret'])
        query = godaddy.get_domains()
        serializer = GodaddyDomainSerializer(query, many=True)
        return Response(serializer.data)


class GodaddyRecordViewSet(viewsets.ViewSet):
    serializer_class = GodaddyRecordSerializer

    def list(self, request):
        domain = request.GET['domain']
        godaddy = GodaddyApi(api_key=GODADDY_KEYINFO['key'], api_secret=GODADDY_KEYINFO['secret'])
        query = godaddy.get_records(domain)
        serializer = GodaddyRecordSerializer(query, many=True)
        return Response(serializer.data)

    def post(self, request, record_type="A", ttl=600):
        godaddy = GodaddyApi(api_key=GODADDY_KEYINFO['key'], api_secret=GODADDY_KEYINFO['secret'])
        domain = request.data['domain']
        if request.data['action'] == 'create':
            sub_domain = request.data['sub_domain']
            value = request.data['value']
            record_type = request.data.get('record_type', record_type)
            ttl = request.data.get('ttl', ttl)
            query = godaddy.add_record(domain, sub_domain, value, record_type, ttl=ttl)
        return Response(query)
