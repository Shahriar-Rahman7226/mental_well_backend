from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.user.views.views_v1 import *

router = DefaultRouter()
router.register('user-registration', UserResgistrationViewSet, basename='user_registration')

urlpatterns = [
                  path(r'', include(router.urls)),
                  path('create-admin/', UserResgistrationViewSet.as_view({'post': 'create_admin'})),
                  path('create-counselor/', UserResgistrationViewSet.as_view({'post': 'create_counselor'})),
                  path('create-client/', ClientResgistrationViewSet.as_view({'post': 'create_client'})),
              ] 




