from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.user_profile.views.views_v1 import *
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register('specialization', SpecializationViewSet, basename='specialization')
router.register('counselor-profile', CounselorProfileViewSet, basename='couselor_profile')
router.register('client-profile', ClientProfileViewSet, basename='client_profile')
router.register('founder-profile', FounderProfileViewSet, basename='founder_profile')
router.register('achievements', AchievementsViewSet, basename='achievements')

urlpatterns = [
                  path(r'', include(router.urls)),
                  path('counselor-update-status/<str:id>/', CounselorProfileViewSet.as_view({'post': 'update_status'})),
                  path('get-counselor-list/', CounselorProfileViewSet.as_view({'get': 'get_counselor_list'})),
                  path('client-update-staus/<str:id>/', ClientProfileViewSet.as_view({'post': 'update_status'})),
              ] 

