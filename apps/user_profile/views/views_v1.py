from django.db import transaction
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from external.pagination import CustomPagination
from external.swagger_query_params import set_query_params
from apps.user_profile.serializers.serializers_v1 import *
from apps.user_profile.models import *
from external.send_message import send_email, send_sms
from rest_framework import status
from external.permission_decorator import allowed_users


@extend_schema(tags=['Specialization'])
class SpecializationViewSet(ModelViewSet):
    model_class = SpecializationModel
    serializer_class = SpecializationSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    @extend_schema(
        examples=[
            OpenApiExample(
                "Create Specialization",
                value={
                    "title": "string",
                    "description": "string",
                },
                request_only=True,
            )
        ]
    )
    @allowed_users(allowed_roles=['ADMIN'])
    def create(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Specialization created succesfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Specialization",
                value={
                    "title": "string",
                    "description": "string",
                },
                request_only=True,
            )
        ],
    )
    @allowed_users(allowed_roles=['ADMIN'])
    def update(self, request, *args, **kwargs):
      
        instance = self.queryset.filter(id=kwargs['id']).first()

        if not instance:
            return Response({'message': 'Specialization does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Specialization updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def list(self, request, *args, **kwargs):
        queryset = self.queryset
    
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@extend_schema(tags=['Counselor Profile'])
class CounselorProfileViewSet(ModelViewSet):
    model_class = CounselorProfileModel
    serializer_class = CounselorProfileListSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return CounselorProfileCreateSerializer
        elif self.action =='update_status':
            return CounselorProfileUpdateSerializer
        return self.serializer_class

    @extend_schema(
        examples=[
            OpenApiExample(
                "Create Counselor Profile",
                value={
                    "certificate": "string",
                    "identity_document": "string",
                    "specializations": ["string", "string"],
                    "description": "string",
                    "license_number": "string",
                    "website": "string",
                    "linked_in": "string",
                    "pay_per_session": 0,
                },
                request_only=True,
            )
        ]
    )
    @transaction.atomic()
    @allowed_users(allowed_roles=['COUNSELOR'])
    def create(self, request, *args, **kwargs):
        print(request.data)
        print(request.user.id)
        instance = UserModel.objects.filter(id=request.user.id, user_role='COUNSELOR').first()
        if not instance:
            return Response({'message': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)
        profile_instance = self.queryset.filter(user=instance.id).first()
        if profile_instance:
            return Response({'message': 'Counselor profile already created'}, status=status.HTTP_400_BAD_REQUEST)
        data=request.data.copy()
        data['user'] = instance.id

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            profile_obj = serializer.save()
            subject = 'Mental Well'
            message = f"Your profile has been created! It is now {profile_obj.status}."
            send_email(None, subject, message, request.user.id)
            return Response({'message': 'Profile created succesfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Counselor Profile",
                value={
                    "certificate": "string",
                    "dentity_document": "string",
                    "specializations": ["string", "string"],
                    "description": "string",
                    "license_number": "string",
                    "website": "string",
                    "linked_in": "string",
                    "pay_per_session": 0,
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
            return Response({'message': 'Counselor profile does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        request.data['status'] = 'PENDING'

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            profile_obj = serializer.save()
            subject = 'Mental Well'
            message = f"Your profile has been updated! It is now {profile_obj.status}."
            send_email(None, subject, message, request.user.id)
            return Response({'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Counselor Profile Status",
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
            return Response({'message': 'Counselor profile does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            profile_obj = serializer.save()
            subject = 'Mental Well'
            message = f"Your profile was {profile_obj.status}. Please contact our authorities for any queries."
            send_email(profile_obj.user.id, subject, message, None)
            return Response({'message': 'Profile status updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(parameters=set_query_params('list', [
        {"name": 'status', "description": 'Filter by status'},
    ]))
    @allowed_users(allowed_roles=['ADMIN'])
    def get_counselor_list(self, request, *args, **kwargs):
        queryset = self.queryset
        profile_status = request.query_params.get('status', None)
        if profile_status:
            queryset = queryset.filter(status=profile_status)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
   
    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(status='APPROVED')
    
        page = self.paginate_queryset(queryset)
        serializer_class = self.get_serializer_class()
        if page is not None:
            serializer = serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
     
    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(id=kwargs['id']).first()
        if not obj:
            return Response({'message': 'Profile does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@extend_schema(tags=['Client Profile'])
class ClientProfileViewSet(ModelViewSet):
    model_class = ClientProfileModel
    serializer_class = ClientProfileListSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return ClientProfileCreateSerializer
        elif self.action =='update_status':
            return ClientProfileUpdateSerializer
        return self.serializer_class

    @extend_schema(
        examples=[
            OpenApiExample(
                "Create Client Profile",
                value={
                    "description": "string",
                    "goals": "string",
                    "emergency_contact": "string",
                },
                request_only=True,
            )
        ]
    )
    @transaction.atomic()
    @allowed_users(allowed_roles=['CLIENT'])
    def create(self, request, *args, **kwargs):
        
        instance = UserModel.objects.filter(id=request.user.id, user_role='CLIENT').first()
        if not instance:
            return Response({'message': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)
        request.data['user'] = instance.id

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            profile_obj = serializer.save()
            subject = 'Mental Well'
            message = f"Your profile has been created! It is now {profile_obj.status}."
            send_email(None, subject, message, request.user.id)
            return Response({'message': 'Profile created succesfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Client Profile",
                value={
                    "description": "string",
                    "goals": "string",
                    "emergency_contact": "string",
                },
                request_only=True,
            )
        ],
    )
    @transaction.atomic()
    @allowed_users(allowed_roles=['CLIENT'])
    def update(self, request, *args, **kwargs):
      
        instance = self.queryset.filter(id=kwargs['id']).first()

        if not instance:
            return Response({'message': 'Client profile does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        request.data['status'] = 'PENDING'

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            profile_obj = serializer.save()
            subject = 'Mental Well'
            message = f"Your profile has been updated! It is now {profile_obj.status}."
            send_email(None, subject, message, request.user.id)
            return Response({'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Client Profile Status",
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
            return Response({'message': 'Client profile does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            profile_obj = serializer.save()
            subject = 'Mental Well'
            message = f"Your profile was {profile_obj.status}. Please contact our authorities for any queries."
            send_email(profile_obj.user.id, subject, message, None)
            return Response({'message': 'Profile status updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @allowed_users(allowed_roles=['ADMIN'])
    def list(self, request, *args, **kwargs):
        queryset = self.queryset
    
        page = self.paginate_queryset(queryset)
        serializer_class = self.get_serializer_class()
        if page is not None:
            serializer = serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(id=kwargs['id']).first()
        if not obj:
            return Response({'message': 'Profile does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @allowed_users(allowed_roles=['ADMIN'])                         # For Bar Chart on Admin Dashboard.
    def get_profile_data(self, request, *args, **kwargs):
        counselor_qs = CounselorProfileModel.objects.filter(status='APPROVED')
        client_qs = self.queryset.objects.filter(status='APPROVED')
        profile_data = {
            'counselor_count': counselor_qs.count(),
            'client_count': client_qs.count(),
        }
        return Response(profile_data, status=status.HTTP_200_OK)
    


@extend_schema(tags=['Founder Profile'])
class FounderProfileViewSet(ModelViewSet):
    model_class = FounderProfileModel
    serializer_class = FounderProfileListSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action in  ['create', 'update']:
            return FounderProfileCreateSerializer
        else:
            return self.serializer_class

    @extend_schema(
        examples=[
            OpenApiExample(
                "Create Founder Profile",
                value={
                    "user": "string",
                    "description": "string",
                    "website": "string",
                    "linked_in": "string",
                },
                request_only=True,
            )
        ]
    )
    @transaction.atomic()
    @allowed_users(allowed_roles=[])
    def create(self, request, *args, **kwargs):
        
        user_instance = UserModel.objects.filter(id=request.data['user']).first()
        if not user_instance:
            return Response({'message': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            profile_obj = serializer.save()
            subject = 'Mental Well'
            message = f"Your profile has been created as a Founder!"
            send_email(profile_obj.user.id, subject, message, None)
            return Response({'message': 'Profile created succesfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Founder Profile",
                value={
                    "description": "string",
                    "website": "string",
                    "linked_in": "string",
                },
                request_only=True,
            )
        ],
    )
    @transaction.atomic()
    def update(self, request, *args, **kwargs):
      
        instance = self.queryset.filter(user__id=request.user.id).first()

        if not instance:
            return Response({'message': 'Founder profile does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            profile_obj = serializer.save()
            subject = 'Mental Well'
            message = f"Your profile has been updated!"
            send_email(None, subject, message, request.user.id)
            return Response({'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def list(self, request, *args, **kwargs):
        queryset = self.queryset
    
        page = self.paginate_queryset(queryset)
        serializer_class = self.get_serializer_class()
        if page is not None:
            serializer = serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
     
    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(id=kwargs['id']).first()
        if not obj:
            return Response({'message': 'Profile does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=['Achievements'])
class AchievementsViewSet(ModelViewSet):
    model_class = CounselorAchievements
    serializer_class = CounselorAchievementsSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    @extend_schema(
        examples=[
            OpenApiExample(
                "Create Achievements",
                value={
                    "title": "string",
                    "awarded_by": "string",
                    "date": "string",
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
        else:
            data['counselor']=request.user.id

        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            achievement_obj = serializer.save()
            subject = 'Mental Well'
            message = f"Your profile has been created! It is now {achievement_obj.status}."
            send_email(None, subject, message, request.user.id)
            return Response({'message': 'Achievement added succesfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Achievement",
                value={
                    "title": "string",
                    "awarded_by": "string",
                    "date": "string",
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
            return Response({'message': 'Achievement does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        request.data['status']='PENDING'

        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            achievement_obj = serializer.save()
            subject = 'Mental Well'
            message = f"Your profile has been updated! It is now {achievement_obj.status}."
            send_email(None, subject, message, request.user.id)
            return Response({'message': 'Achievement updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Achievement Status",
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
            return Response({'message': 'Achievement does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            achievement_obj = serializer.save()
            subject = 'Mental Well'
            message = f"Your achievement was {achievement_obj.status}. Please contact our authorities for any queries."
            send_email(achievement_obj.counselor.user.id, subject, message, None)
            return Response({'message': 'Achievement status updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @extend_schema(parameters=set_query_params('list', [
        {"name": 'counselor_id', "description": 'Filter by counselor_id'},
    ]))
    def list(self, request, *args, **kwargs):
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
    

    @extend_schema(parameters=set_query_params('list', [
        {"name": 'counselor_id', "description": 'Filter by counselor_id'},
        {"name": 'status', "description": 'Filter by achievement status'},
    ]))
    @allowed_users(allowed_roles=['ADMIN'])
    def get_achievement_list(self, request, *args, **kwargs):
        queryset = self.queryset
        counselor_id = request.query_params.get('counselor_id', None)
        achievement_status = request.query_params.get('status', None)
        if counselor_id:
            queryset = queryset.filter(counselor=counselor_id)
        if achievement_status:
            queryset = queryset.filter(counselor=achievement_status)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(id=kwargs['id']).first()
        if not obj:
            return Response({'message': 'Achievement does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


