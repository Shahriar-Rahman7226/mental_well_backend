from django.db import transaction
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from external.pagination import CustomPagination
from external.swagger_query_params import set_query_params
from apps.schedule_management.serializers.serializers_v1 import *
from ..models import *
from external.send_message import send_email, send_sms
from rest_framework import status
from external.permission_decorator import allowed_users


@extend_schema(tags=['Schedule Management'])
class CounselorScheduleViewSet(ModelViewSet):
    model_class = CounselorSchedule
    serializer_class = CounselorScheduleSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    @extend_schema(
        examples=[
            OpenApiExample(
                "Create Counselor Schedule",
                value={
                    "day": "string",
                    "start_time": "06:00",
                    "end_time": "07:30",
                },
                request_only=True,
            )
        ]
    )
    @transaction.atomic()
    @allowed_users(allowed_roles=['COUNSELOR'])
    def create(self, request, *args, **kwargs):
        data = request.data
        instance = CounselorProfileModel.objects.filter(user__id=request.user.id, user__user_role='COUNSELOR').first()
        if not instance:
            return Response({'message': 'Invalid Counselor'}, status=status.HTTP_400_BAD_REQUEST)

        if data['start_time'] > data['end_time']:
            return Response({'message': 'Start time cannot be greater than end time'}, status=status.HTTP_400_BAD_REQUEST)
        data['counselor']=instance.id

        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            schedule_obj = serializer.save()
            subject = 'Mental Well'
            message = f"Your schedule has been created! It is now {schedule_obj.status}."
            send_email(None, subject, message, request.user.id)
            return Response({'message': 'Counselor schedule created succesfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Counselor Schedule",
                value={
                    "day": "string",
                    "start_time": "06:00",
                    "end_time": "07:30",
                },
                request_only=True,
            )
        ],
    )
    @allowed_users(allowed_roles=['COUNSELOR'])
    def update(self, request, *args, **kwargs):
      
        instance = self.queryset.filter(id=kwargs['id']).first()

        if not instance:
            return Response({'message': 'Counselor schedule does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        if request.data['start_time'] > request.data['end_time']:
            return Response({'message': 'Start time cannot be greater than end time'}, status=status.HTTP_400_BAD_REQUEST)
        request.data['status']="PENDING"
        
        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            schedule_obj = serializer.save()
            subject = 'Mental Well'
            message = f"Your schedule has been updated! It is now {schedule_obj.status}."
            send_email(None, subject, message, request.user.id)
            return Response({'message': 'Counselor schedule updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Counselor Schedule Status",
                value={
                    "status": "string",
                },
                request_only=True,
            )
        ],
    )
    @allowed_users(allowed_roles=['ADMIN'])
    def update_status(self, request, *args, **kwargs):
      
        instance = self.queryset.filter(id=kwargs['id']).first()

        if not instance:
            return Response({'message': 'Counselor schedule does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            schedule_obj = serializer.save()
            subject = 'Mental Well'
            message = f'Your schedule for {schedule_obj.day} was {schedule_obj.status}. Please contact our authorities for any queries.'
            send_email(schedule_obj.counselor.user.id, subject, message, None)
            return Response({'message': 'Counselor schedule status updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(parameters=set_query_params('list', [
        {"name": 'counselor_id', "description": 'Filter by counselor_id'},
        {"name": 'status', "description": 'Filter by status'}
    ]))
    @allowed_users(allowed_roles=['ADMIN'])
    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        counselor_id = request.query_params.get('counselor_id', None)
        schedule_status = request.query_params.get('status', None)
        if counselor_id:
            queryset = queryset.filter(counselor=counselor_id)
        if schedule_status:
            queryset = queryset.filter(status=schedule_status)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @extend_schema(parameters=set_query_params('list', [
        {"name": 'status', "description": 'Filter by status'}
    ]))
    @allowed_users(allowed_roles=['COUNSELOR'])
    def get_schedule(self, request, *args, **kwargs):
        queryset = self.queryset.filter(counselor=request.user.id)
        schedule_status = request.query_params.get('status', None)
        if schedule_status:
            queryset = queryset.filter(status=schedule_status)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @extend_schema(parameters=set_query_params('list', [
        {"name": 'counselor_id', "description": 'Filter by counselor_id'},
    ]))
    @allowed_users(allowed_roles=['CLIENT'])
    def get_schedule_for_client(self, request, *args, **kwargs):
        queryset = self.queryset.filter(status='APPROVED')
        counselor_id = request.query_params.get('counselor_id', None)
        if counselor_id:
            queryset = queryset.filter(counselor=counselor_id)
            
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
     
    @allowed_users(allowed_roles=['ADMIN', 'COUNSELOR'])
    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter().first()
        if not obj:
            return Response({'message': 'Counselor schedule does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
