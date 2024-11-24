from django.db import transaction
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from external.pagination import CustomPagination
from external.swagger_query_params import set_query_params
from apps.appointment_management.serializers.serializers_v1 import *
from ..models import *
from external.send_message import send_email, send_sms
from rest_framework import status
from external.permission_decorator import allowed_users
from apps.payment.serializers.serializers_v1 import PaymentSerializer
from apps.schedule_management.serializers.serializers_v1 import CounselorScheduleSerializer

@extend_schema(tags=['Appointment Management'])
class AppointmentRequestViewSet(ModelViewSet):
    model_class = AppointmentRequest
    serializer_class = AppointmentRequestSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    @extend_schema(
        examples=[
            OpenApiExample(
                "Create Appointment Request",
                value={
                    "counselor": "string",
                    "schedule": "string",
                    "booking_date": "string",
                },
                request_only=True,
            )
        ]
    )
    @transaction.atomic()
    @allowed_users(allowed_roles=['CLIENT'])
    def create(self, request, *args, **kwargs):
        data = request.data
        counselor_instance = CounselorProfileModel.objects.filter(user__id=data['counselor'], user__user_role='COUNSELOR').first()
        if not counselor_instance:
            return Response({'message': 'Invalid Counselor'}, status=status.HTTP_400_BAD_REQUEST)
        
        client_instance = ClientProfileModel.objects.filter(user__id=request.user.id, user__user_role='CLIENT').first()
        if not client_instance:
            return Response({'message': 'Invalid Client'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            data['client']=request.user.id
        
        schedule_instance = CounselorSchedule.objects.filter(id=data['schedule']).first()
        if not schedule_instance:
             return Response({'message': 'Invalid Schedule'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            schedule_data = {
                'is_booked': True
            }
            schedule_serializer = CounselorScheduleSerializer(instance=schedule_instance, data=schedule_data)
            if schedule_serializer.is_valid(raise_exception=True):
                schedule_serializer.save()
            else:
                return Response(schedule_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        data['appointment_details'] = f"Appointment booked by client {data['client'].user.full_name} with counselor {data['counselor'].user.full_name} on {data['schedule'].day} from {data['schedule'].start_time} to {data['schedule'].end_time}."
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            appointment_obj = serializer.save()

            payment_data = {
                'counselor': appointment_obj.counselor,
                'client': appointment_obj.client,
                'appointment': appointment_obj.id,
                'due_amount': appointment_obj.counselor.pay_per_session,
            }
            payment_serializer = PaymentSerializer(data=payment_data)
            if payment_serializer.is_valid(raise_exception=True):
                payment_serializer.save()
            else:
                return Response(payment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            subject = 'Mental Well'
            client_message = f'Your appointment was confirmed wth Dr.{appointment_obj.counselor.user.full_name}. Timing: {appointment_obj.schedule.day} - {appointment_obj.start_time} to {appointment_obj.end_time}.'
            counselor_message = f'Your appointment was confirmed with client {appointment_obj.client.user.full_name}. Timing: {appointment_obj.schedule.day} - {appointment_obj.start_time} to {appointment_obj.end_time}.'
            send_email(None, subject, client_message, request.user.id)
            send_email(appointment_obj.counselor.user.id, subject, counselor_message, None)
            return Response({'message': 'Appointment Request created succesfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(parameters=set_query_params('list', [
        {"name": 'counselor_id', "description": 'Filter by counselor_id'},
        {"name": 'status', "description": 'Filter by status'},
    ]))
    @allowed_users(allowed_roles=['ADMIN'])
    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        counselor_id = request.query_params.get('counselor_id', None)
        appointment_status = request.query_params.get('status', None)
        if counselor_id:
            queryset = queryset.filter(counselor=counselor_id)
        if appointment_status:
            queryset = queryset.filter(status=appointment_status)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @extend_schema(parameters=set_query_params('list', [
        {"name": 'status', "description": 'Filter by status'},
    ]))
    @allowed_users(allowed_roles=['COUNSELOR'])
    def get_appointment_list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(counselor__user=request.user.id)
        appointment_status = request.query_params.get('status', None)
        if appointment_status:
            queryset = queryset.filter(status=appointment_status)
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
        obj = queryset.filter(id=kwargs['id']).first()
        if not obj:
            return Response({'message': 'Appointment Request does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)



@extend_schema(tags=['Appointment Management(Cancel Request)'])
class AppointmentRequestCancelViewSet(ModelViewSet):
    model_class = AppointmentRequestCancel
    serializer_class = AppointmentRequestCancelSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    @extend_schema(
        examples=[
            OpenApiExample(
                "Create Appointment Cancel Request",
                value={
                    "appointment": "string",
                    "details": "string",
                    "emergency_document": "string",
                },
                request_only=True,
            )
        ]
    )
    @transaction.atomic()
    @allowed_users(allowed_roles=['COUNSELOR', 'CLIENT'])
    def create(self, request, *args, **kwargs):
        data = request.data
        user_instance = UserModel.objects.filter(id=data['user']).first()
        if not user_instance:
            return Response({'message': 'Invalid User'}, status=status.HTTP_400_BAD_REQUEST)
        
        appointment_instance = AppointmentRequest.objects.filter(id=data['appointment']).first()
        if not appointment_instance:
            return Response({'message': 'Invalid Appointment'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            appointment_cancel_obj = serializer.save()
            subject = 'Mental Well'
            message = f'Your appointment cancel is {appointment_cancel_obj.status}.'
            send_email(None, subject, message, request.user.id)
            return Response({'message': 'Appointment Cancel Request created succesfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Appointment Request Cancel Status.",
                value={
                    "status": "string",
                    "is_refund": "string",
                },
                request_only=True,
            )
        ],
    )
    @allowed_users(allowed_roles=['ADMIN'])
    def update(self, request, *args, **kwargs):
      
        instance = self.queryset.filter(id=kwargs['id']).first()
        if not instance:
            return Response({'message': 'Appointment Cancellation Request does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        # appointment_instance = AppointmentRequest.objects.filter(id=instance.appointment).first()
        # if not appointment_instance:
        #     return Response({'message': 'Appointment Request does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        if (request.data['status']=='APPROVED'):
            appointment_data = {
                'status': 'CANCELLED',
            }
            appointment_serializer = AppointmentRequestSerializer(instance=instance.appointment, data=appointment_data)
            if appointment_serializer.is_valid(raise_exception=True):
                appointment_serializer.save()
            else:
                return Response(appointment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            schedule_data = {
                'is_booked': 'CANCELLED',
            }
            schedule_serializer = CounselorScheduleSerializer(instance=instance.appointment.schedule, data=schedule_data)
            if schedule_serializer.is_valid(raise_exception=True):
                schedule_serializer.save()
            else:
                return Response(schedule_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            appointment_cancel_obj = serializer.save()

            subject = 'Mental Well'
            if (appointment_cancel_obj.status == 'APPROVED' and appointment_cancel_obj.user.user_role=='COUNSELOR'):
                counselor_message = f'Your appointment with client {appointment_cancel_obj.appointment.counselor.user.full_name} on {appointment_cancel_obj.appointment.schedule.day} was cancelled.'
                client_message = f'Your appointment with counselor {appointment_cancel_obj.appointment.client.user.full_name} on {appointment_cancel_obj.appointment.schedule.day} was cancelled due to some emergency. You will get your refund soon. Sorry for any inconveniences.'
            elif (appointment_cancel_obj.status == 'APPROVED' and appointment_cancel_obj.user.user_role=='CLIENT'):
                counselor_message = f'Your appointment with client {appointment_cancel_obj.appointment.counselor.user.full_name} on {appointment_cancel_obj.appointment.schedule.day} was cancelled due to some emergency. Sorry for any inconveniences.'
                client_message = f'Your appointment with counselor {appointment_cancel_obj.appointment.client.user.full_name} on {appointment_cancel_obj.appointment.schedule.day} was cancelled. Sorry but we are unable to provide your refund.'
            elif (appointment_cancel_obj.status == 'APPROVED' and appointment_cancel_obj.user.user_role=='CLIENT' and appointment_cancel_obj.is_refund):
                counselor_message = f'Your appointment with client {appointment_cancel_obj.appointment.counselor.user.full_name} on {appointment_cancel_obj.appointment.schedule.day} was cancelled due to some emergency. Sorry for any inconveniences.'
                client_message = f'Your appointment with counselor {appointment_cancel_obj.appointment.client.user.full_name} on {appointment_cancel_obj.appointment.schedule.day} was cancelled. You will get your refund soon.'

            if (appointment_cancel_obj.status == 'REJECTED'):
                message = "Sorry, but we cannot cancel your appointment at this moment."
                send_email(appointment_cancel_obj.user.id, subject, message, None)
            else:
                send_email(appointment_cancel_obj.appointment.counselor.user.id, subject, counselor_message, None)
                send_email(appointment_cancel_obj.appointment.client.user.id, subject, client_message, None)
            return Response({'message': 'Appointment Request Cancel status updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @extend_schema(parameters=set_query_params('list', [
        {"name": 'status', "description": 'Filter by status'},
    ]))
    @allowed_users(allowed_roles=['ADMIN'])
    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        cancel_status = request.query_params.get('status', None)
        if cancel_status:
            queryset = queryset.filter(status=cancel_status)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
     
    @allowed_users(allowed_roles=['ADMIN'])
    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(id=kwargs['id']).first()
        if not obj:
            return Response({'message': 'Appointment Cancellation Request does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
