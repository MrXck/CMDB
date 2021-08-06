import datetime

from django.db.models import Q

from api import models
from api.service.cpu import process_cpu_info
from api.service.disk import process_disk_info
from api.service.basic import process_basic_info
from api.service.board import process_board_info
from api.service.memory import process_memory_info
from api.service.network import process_network_info

from rest_framework.views import APIView
from rest_framework.response import Response


class ServerView(APIView):

    def get(self, request, *args, **kwargs):
        today = datetime.date.today()
        host_list = models.Server.objects.filter(Q(Q(last_date__isnull=True) | Q(last_date__lt=today)), status=1).values_list(
            'hostname')
        host_list = [i[0] for i in host_list]
        return Response({'status': True, 'data': host_list})

    def post(self, request, *args, **kwargs):
        server_info_dict = request.data
        hostname = server_info_dict['host']
        host_obj = models.Server.objects.filter(hostname=hostname).first()
        if not host_obj:
            return Response({'status': False})
        info_dict = server_info_dict['info']
        disk_dict = info_dict['disk']
        network_dict = info_dict['network']
        cpu_dict = info_dict['cpu']
        memory_dict = info_dict['memory']
        board_dict = info_dict['board']
        basic_dict = info_dict['basic']
        process_disk_info(host_obj, disk_dict)
        process_network_info(host_obj, network_dict)
        process_cpu_info(host_obj, cpu_dict)
        process_memory_info(host_obj, memory_dict)
        process_board_info(host_obj, board_dict)
        process_basic_info(host_obj, basic_dict)
        host_obj = models.Server.objects.filter(hostname=hostname).first()
        host_obj.last_date = datetime.date.today()
        host_obj.save()
        return Response({'status': True})
