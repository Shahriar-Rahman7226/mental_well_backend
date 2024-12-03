from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.client_progress.views.views_v1 import *

router = DefaultRouter()
router.register('client-progress', ClientProgressViewSet, basename='client_progress')
router.register('client-progress-details', ClientProgressDetailsViewSet, basename='client_progress_details')

urlpatterns = [
    path(r'', include(router.urls)),
]
