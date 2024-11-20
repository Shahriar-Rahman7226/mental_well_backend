# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.counselor_resources.views.views_v1 import *

router = DefaultRouter()
router.register('counselor-resource', CounselorResourceViewSet, basename='counselor_resource')
router.register('other-resource', OtherResourceViewSet, basename='other_resource')

urlpatterns = [
    path(r'', include(router.urls)),
]


