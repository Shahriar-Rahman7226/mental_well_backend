from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.appointment_management.views.views_v1 import *

router = DefaultRouter()
router.register('appointment-request', AppointmentRequestViewSet, basename='appointment_request')

urlpatterns = [
    path(r'', include(router.urls)),
    path('get-request/', AppointmentRequestViewSet.as_view({'get': 'get_request'})),
]




