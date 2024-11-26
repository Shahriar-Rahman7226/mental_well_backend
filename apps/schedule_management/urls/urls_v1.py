# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.schedule_management.views.views_v1 import *

router = DefaultRouter()
router.register('counselor-schedule', CounselorScheduleViewSet, basename='counselor_schedule')

urlpatterns = [
    path(r'', include(router.urls)),
    path('counselor-update-staus/<str:id>/', CounselorScheduleViewSet.as_view({'post': 'update_status'})),
    path('get-schedule/', CounselorScheduleViewSet.as_view({'get': 'get_schedule'})),
    path('get-schedule_for_client/', CounselorScheduleViewSet.as_view({'get': 'get_schedule_for_client'})),
]