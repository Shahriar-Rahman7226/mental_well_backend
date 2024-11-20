from django.db import transaction
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from external.pagination import CustomPagination
from external.swagger_query_params import set_query_params
from apps.client_progress.serializers.serializers_v1 import *
from ..models import *
from external.send_message import send_email, send_sms
from rest_framework import status
from external.permission_decorator import allowed_users


@extend_schema(tags=['Client Progress'])
class ClientProgressViewSet(ModelViewSet):
    model_class = ClientProgress
    serializer_class = ClientProgressSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    @extend_schema(
        examples=[
            OpenApiExample(
                "Create Client Progress",
                value={
                    "client": "string",
                    "status": "string",
                },
                request_only=True,
            )
        ]
    )
    @transaction.atomic()
    @allowed_users(allowed_roles=['COUNSELOR'])
    def create(self, request, *args, **kwargs):
        data = request.data
        counselor_instance = CounselorProfileModel.objects.filter(user__id=request.user.id, user__user_role='COUNSELOR').first()
        if not counselor_instance:
            return Response({'message': 'Invalid Counselor'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            data['counselor']=request.user.id
        
        client_instance = ClientProfileModel.objects.filter(user__id=data['client'], user__user_role='CLIENT').first()
        if not client_instance:
            return Response({'message': 'Invalid Client'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Client Progress created succesfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Client Progress",
                value={
                    "status": "string",
                },
                request_only=True,
            )
        ],
    )
    @transaction.atomic()
    @allowed_users(allowed_roles=['COUNSELOR'])
    def update(self, request, *args, **kwargs):
      
        instance = self.queryset.filter(id=kwargs['id']).first()

        if not instance:
            return Response({'message': 'Client Progress does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Client Progress updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @extend_schema(parameters=set_query_params('list', [
        {"name": 'status', "description": 'Filter by client progress status'},
    ]))
    @allowed_users(allowed_roles=['COUNSELOR'])
    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        status = request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @allowed_users(allowed_roles=['COUNSELOR'])
    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(id=request.user.id).first()
        if not obj:
            return Response({'message': 'Client Progress does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@extend_schema(tags=['Client Progress Details'])
class ClientProgressDetailsViewSet(ModelViewSet):
    model_class = ClientProgressDetails
    serializer_class = ClientProgressDetailsSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    @extend_schema(
        examples=[
            OpenApiExample(
                "Create Client Progress Details",
                value={
                    "progress": "string",
                    "appointment": "string",
                    "details": "string",
                },
                request_only=True,
            )
        ]
    )
    @transaction.atomic()
    @allowed_users(allowed_roles=['COUNSELOR'])
    def create(self, request, *args, **kwargs):
        data = request.data
        counselor_instance = CounselorProfileModel.objects.filter(user__id=request.user.id, user__user_role='COUNSELOR').first()
        if not counselor_instance:
            return Response({'message': 'Invalid Counselor'}, status=status.HTTP_400_BAD_REQUEST)
        
        progress_instance = ClientProgress.objects.filter(id=data['progress']).first()
        if not progress_instance:
            return Response({'message': 'Invalid Client Progress'}, status=status.HTTP_400_BAD_REQUEST)
        
        appointment_instance = AppointmentRequest.objects.filter(id=data['appointment']).first()
        if not appointment_instance:
            return Response({'message': 'Invalid Appointment Request'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Client Progress Details created succesfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Client Progress Details",
                value={
                    "details": "string",
                },
                request_only=True,
            )
        ],
    )
    @transaction.atomic()
    @allowed_users(allowed_roles=['COUNSELOR'])
    def update(self, request, *args, **kwargs):
      
        instance = self.queryset.filter(id=kwargs['id']).first()

        if not instance:
            return Response({'message': 'Client Progress Details does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Client Progress Details updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @extend_schema(parameters=set_query_params('list', [
        {"name": 'client_progress', "description": 'Filter by client progress'},
    ]))
    @allowed_users(allowed_roles=['COUNSELOR'])
    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        progress = request.query_params.get('client_progress', None)
        if progress:
            queryset = queryset.filter(progress=progress)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @allowed_users(allowed_roles=['COUNSELOR'])
    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(id=request.user.id).first()
        if not obj:
            return Response({'message': 'Client Progress Details does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
