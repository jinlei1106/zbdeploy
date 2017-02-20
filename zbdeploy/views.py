import os
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import Project
from .serializers import ProjectListSerializer


class DeployViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer
    permission_classes = (AllowAny,)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # 获取部署方式，默认为生产环境部署
        deploy_type = request.query_params.get('type', '')
        if deploy_type == 'test':
            command = instance.test_c
        else:
            command = instance.prod_c
        # 生成shell脚本并上传
        filename = '{}.sh'.format(instance.code)
        filepath = os.path.join(settings.BASE_DIR, 'shell', filename)
        if not os.path.exists(filepath):
            f = open(filepath, 'w')
            f.write('#!/bin/bash')
            f.write('\n')
            f.write('cd {0} &&'.format(instance.work_dir))
            f.write('\n')
            f.write('git pull origin {} &&'.format(instance.branch))
            f.write('\n')
            f.write('sh {}'.format(command))
            f.close()
        os.system('scp {0} zboper@{1}:www/'.format(filepath, instance.host))
        os.system('ssh zboper@{0} "chmod +x ~/www/{1}.sh"'.format(instance.host, instance.code))
        # 远程调脚本执行部署任务
        os.system('ssh zboper@{0} /home/zboper/www/{1}.sh'.format(instance.host, instance.code))
        return Response({'message': '成功'}, status=status.HTTP_200_OK)
