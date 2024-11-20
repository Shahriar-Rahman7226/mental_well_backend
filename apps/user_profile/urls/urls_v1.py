from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.user_profile.views.views_v1 import *
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register('specialization', SpecializationViewSet, basename='specialization')
router.register('counselor-profile', CounselorProfileViewSet, basename='couselor_profile')
router.register('client-profile', ClientProfileViewSet, basename='client_profile')
router.register('founder-profile', ClientProfileViewSet, basename='founder_profile')
router.register('achievements', AchievementsViewSet, basename='achievements')

urlpatterns = [
                  path(r'', include(router.urls)),
                  path('counselor-update-staus/', CounselorProfileViewSet.as_view({'post': 'update_status'})),
                  path('client-update-staus/', ClientProfileViewSet.as_view({'post': 'update_status'})),
              ] 

