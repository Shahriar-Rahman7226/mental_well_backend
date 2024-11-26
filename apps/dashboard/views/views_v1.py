from django.db import transaction
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from external.pagination import CustomPagination
from external.swagger_query_params import set_query_params
from apps.dashboard.serializers.serializers_v1 import *
from ..models import *
from rest_framework import status
from external.permission_decorator import allowed_users


@extend_schema(tags=['Banner'])
class BannerViewSet(ModelViewSet):
    model_class = BannerModel
    serializer_class = BannerSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Banner",
                value={
                    "title": "string",
                    "image": "string",
                },
                request_only=True,
            )
        ],
    )
    @allowed_users(allowed_roles=['ADMIN'])
    def update(self, request, *args, **kwargs):
      
        instance = self.model_class.objects.filter(id=kwargs['id']).first()

        if not instance:
            return Response({'message': 'Banner does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Banner updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(id=kwargs['id']).first()
        if not obj:
            return Response({'message': 'Banner does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer_class = self.serializer_class
        serializer = serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@extend_schema(tags=['Motivation'])
class MotivationViewSet(ModelViewSet):
    model_class = MotivationModel
    serializer_class = MotivationSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    @extend_schema(
        examples=[
            OpenApiExample(
                "Create Motivational Quote",
                value={
                    "quote_text": "string",
                    "author": "string",
                },
                request_only=True,
            )
        ]
    )
    @transaction.atomic()
    @allowed_users(allowed_roles=['ADMIN'])
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Motivational quote created succesfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Motivational Quote",
                value={
                    "quote_text": "string",
                    "author": "string",
                },
                request_only=True,
            )
        ],
    )
    @allowed_users(allowed_roles=['ADMIN'])
    def update(self, request, *args, **kwargs):
      
        instance = self.queryset.filter(id=kwargs['id']).first()

        if not instance:
            return Response({'message': 'Motivational Quote does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Motivational Quote updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @allowed_users(allowed_roles=['ADMIN'])
    def list(self, request, *args, **kwargs):
        queryset = self.queryset
    
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
            return Response({'message': 'Motivational Quote does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


    

@extend_schema(tags=['Legal Document'])
class LegalDocumentViewSet(ModelViewSet):
    model_class = LegalDocument
    serializer_class = LegalDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Legal Document",
                value={
                    "details": "string",
                    "version": "string",
                    "licence_document": "string",
                },
                request_only=True,
            )
        ],
    )
    @allowed_users(allowed_roles=['ADMIN'])
    def update(self, request, *args, **kwargs):
      
        instance = self.model_class.objects.filter(id=kwargs['id']).first()

        if not instance:
            return Response({'message': 'Legal Document does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Legal Document updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(id=kwargs['id']).first()
        if not obj:
            return Response({'message': 'Legal Document does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer_class = self.serializer_class
        serializer = serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@extend_schema(tags=['Privacy Policy'])
class PrivacyPolicyViewSet(ModelViewSet):
    model_class = PrivacyPolicy
    serializer_class = PrivacyPolicySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Privacy Policy",
                value={
                    "details": "string",
                },
                request_only=True,
            )
        ],
    )
    @allowed_users(allowed_roles=['ADMIN'])
    def update(self, request, *args, **kwargs):
      
        instance = self.model_class.objects.filter(id=kwargs['id']).first()

        if not instance:
            return Response({'message': 'Privacy Policy does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Privacy Policy updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(id=kwargs['id']).first()
        if not obj:
            return Response({'message': 'Privacy Policy does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer_class = self.serializer_class
        serializer = serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@extend_schema(tags=['About Us'])
class AboutUsViewSet(ModelViewSet):
    model_class = AboutUs
    serializer_class = AboutUsSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    @extend_schema(
        examples=[
            OpenApiExample(
               "Update About Us",
                value={
                    "introduction": "string",
                    "mission": "string",
                    "vission": "string",
                    "details": "string",
                    "contact_email": "string",
                    "contact_number": "string",
                    "address": "string",
                    "facebook": "string",
                    "instagram": "string",
                    "youtube": "string",
                    "linkedin": "string",
                },
                request_only=True,
            )
        ],
    )
    @allowed_users(allowed_roles=['ADMIN'])
    def update(self, request, *args, **kwargs):
      
        instance = self.model_class.objects.filter(id=kwargs['id']).first()

        if not instance:
            return Response({'message': 'About Us does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'About Us updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(id=kwargs['id']).first()
        if not obj:
            return Response({'message': 'About Us does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer_class = self.serializer_class
        serializer = serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@extend_schema(tags=['Footer'])
class FooterViewSet(ModelViewSet):
    model_class = FooterModel
    serializer_class = FooterSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Footer",
                value={
                    "image": "string",
                    "details": "string",
                    "contact_email": "string",
                    "contact_number": "string",
                    "address": "string",
                    "emergency_support": "string",
                    "facebook": "string",
                    "instagram": "string",
                    "youtube": "string",
                    "linkedin": "string",
                },
                request_only=True,
            )
        ],
    )
    @allowed_users(allowed_roles=['ADMIN'])
    def update(self, request, *args, **kwargs):
      
        instance = self.model_class.objects.filter(id=kwargs['id']).first()

        if not instance:
            return Response({'message': 'Footer does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Footer updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(id=kwargs['id']).first()
        if not obj:
            return Response({'message': 'Footer does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer_class = self.serializer_class
        serializer = serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
