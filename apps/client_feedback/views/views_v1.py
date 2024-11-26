from django.db import transaction
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from external.pagination import CustomPagination
from external.swagger_query_params import set_query_params
from apps.client_feedback.serializers.serializers_v1 import *
from ..models import *
from external.send_message import send_email, send_sms
from rest_framework import status
from external.permission_decorator import allowed_users
from apps.appointment_management.models import AppointmentRequest


@extend_schema(tags=['FAQ'])
class FAQViewSet(ModelViewSet):
    model_class = FAQModel
    serializer_class = FAQSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    @extend_schema(
        examples=[
            OpenApiExample(
                "Create FAQ",
                value={
                    "question": "string",
                },
                request_only=True,
            )
        ]
    )
    @transaction.atomic()
    @allowed_users(allowed_roles=['CLIENT'])
    def create(self, request, *args, **kwargs):
        client_instance = ClientProfileModel.objects.filter(user__id=request.user.id).first()
        if not client_instance:
            return Response({'message': 'Invalid Client'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            request.data['client'] = client_instance.id

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'FAQ created succesfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @extend_schema(
        examples=[
            OpenApiExample(
               "Update FAQ Status",
                value={
                    "answer": "string",
                    "is_published": "string",
                },
                request_only=True,
            )
        ],
    )
    @allowed_users(allowed_roles=['ADMIN'])
    def update_status(self, request, *args, **kwargs):
      
        instance = self.queryset.filter(id=kwargs['id']).first()

        if not instance:
            return Response({'message': 'FAQ does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'FAQ answered successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @allowed_users(allowed_roles=['CLIENT', 'COUNSELOR'])
    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(is_published=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(parameters=set_query_params('list', [
        {"name": 'is_published', "description": 'Filter by published status'},
    ]))
    @allowed_users(allowed_roles=['ADMIN'])
    def get_faq(self, request, *args, **kwargs):
        queryset = self.queryset
        is_published = request.query_params.get('is_published', None)
        if is_published:
            queryset = queryset.filter(is_published=is_published)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@extend_schema(tags=['Review'])
class ReviewViewSet(ModelViewSet):
    model_class = Review
    serializer_class = ReviewSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    @extend_schema(
        examples=[
            OpenApiExample(
                "Create Review",
                value={
                    "counselor": "string",
                    "rating": 5,
                    "review_text": "string",
                    "is_anonymous": "string",
                },
                request_only=True,
            )
        ]
    )
    @transaction.atomic()
    @allowed_users(allowed_roles=['CLIENT'])
    def create(self, request, *args, **kwargs):
        client_instance = ClientProfileModel.objects.filter(user__id=request.user.id).first()
        if not client_instance:
            return Response({'message': 'Invalid Client'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            request.data['client'] = client_instance.id

        counselor_instance = CounselorProfileModel.objects.filter(user__id=request.data['counselor']).first()
        if not counselor_instance:
            return Response({'message': 'Invalid Counselor'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            request.data['counselor_name'] = counselor_instance.user.full_name

        appointment_qs = AppointmentRequest.objects.filter(client=request.user.id, status='COMPLETED')
        request.data['appointment_count'] = appointment_qs.count()

        if (request.data['is_anonymous']==False):
            request.data['client_name']=client_instance.user.full_name
        else:
            request.data['client_name']='Anonymous'

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Review created succesfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Review Status",
                value={
                    "is_published": "string",
                },
                request_only=True,
            )
        ],
    )
    @allowed_users(allowed_roles=['ADMIN'])
    def update_status(self, request, *args, **kwargs):
      
        instance = self.queryset.filter(id=kwargs['id']).first()

        if not instance:
            return Response({'message': 'Review does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Review updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    @allowed_users(allowed_roles=['CLIENT', 'COUNSELOR'])
    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(is_published=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(parameters=set_query_params('list', [
        {"name": 'is_published', "description": 'Filter by published status'},
        {"name": 'counselor', "description": 'Filter by counselor id'},
    ]))
    @allowed_users(allowed_roles=['ADMIN'])
    def get_review(self, request, *args, **kwargs):
        queryset = self.queryset
        is_published = request.query_params.get('is_published', None)
        counselor = request.query_params.get('counselor', None)
        if is_published:
            queryset = queryset.filter(is_published=is_published)
        if counselor:
            queryset = queryset.filter(counselor__user__id=counselor)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
