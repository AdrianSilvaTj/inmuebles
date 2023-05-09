from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from applications.property.models import Property, Company, Comment
from .serializers import (
    PropertyModelSerializer, PropertyHyLinkSerializer , CompanyModelSerializer,
    CompanyHyLinkSerializer, CommentModelSerializer
)
from .permissions import IsAdminOrReadOnly

class CompanyModelViewset(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    #serializer_class = CompanyModelSerializer
    # Se le aplica los permisos definidos en AdminOrReadOnlyPermission
    permission_classes = [IsAdminOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CompanyHyLinkSerializer        
        return CompanyModelSerializer
    
