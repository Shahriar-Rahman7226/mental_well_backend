# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.dashboard.views.views_v1 import *

router = DefaultRouter()
router.register('banner', BannerViewSet, basename='banner')
router.register('motivation', MotivationViewSet, basename='motivation')
router.register('legal-document', LegalDocumentViewSet, basename='legal_document')
router.register('privacy-policy', PrivacyPolicyViewSet, basename='privacy_policy')
router.register('about-us', AboutUsViewSet, basename='about_us')
router.register('footer', FooterViewSet, basename='footer')

urlpatterns = [
    path(r'', include(router.urls)),
]
