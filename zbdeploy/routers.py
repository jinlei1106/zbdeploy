from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'deploy', views.DeployViewSet, base_name='deploy')
