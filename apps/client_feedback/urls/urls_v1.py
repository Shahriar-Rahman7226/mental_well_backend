from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.client_feedback.views.views_v1 import *

router = DefaultRouter()
router.register('faq', FAQViewSet, basename='faq')
router.register('review', ReviewViewSet, basename='review')

urlpatterns = [
    path(r'', include(router.urls)),
     path('get-faq/', FAQViewSet.as_view({'get': 'get_faq'})),
]
