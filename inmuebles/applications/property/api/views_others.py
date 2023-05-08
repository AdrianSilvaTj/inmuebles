from django.shortcuts import get_object_or_404
 
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets

from applications.property.models import Property, Company, Comment
from .serializers import (
    PropertySerializer, PropertyModelSerializer, CompanySerializer,
    CompanyHyLinkSerializer,CommentModelSerializer, CompanyModelSerializer
)


#####################################################################################
#               FUNCTIONS VIEWS                                       #                    #
#####################################################################################

# decorador para indicar con que metodo ('GET', 'POST, 'PUT, etc) trabajara la función.
# por defecto es GET
@api_view(['GET', 'POST']) 
def property_list(request):
    if request.method == 'GET':
            properties = Property.objects.all()
            serializer = PropertySerializer(properties, many=True)
            return Response(serializer.data)
    elif request.method == 'POST':
        deserializer = PropertySerializer(data=request.data)
        if deserializer.is_valid():
            deserializer.save()
            return Response(deserializer.data, status=status.HTTP_201_CREATED)
        return Response(deserializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET','PUT','DELETE'])
def property_detail(request, pk):
    if request.method == 'GET':
        # get_object_or_404, retorna el mismo el error en caso de no encontrar el objeto
        property = get_object_or_404(Property, pk=pk)
        serializer = PropertySerializer(property)
        return Response(serializer.data)
    elif request.method == 'PUT':
        property = Property.objects.get(pk=pk)
        deserializer = PropertySerializer(property, data=request.data)
        if deserializer.is_valid():
            deserializer.save()
            return Response(deserializer.data)
        return Response(deserializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        property = get_object_or_404(Property, pk=pk)
        property.delete()
        response = {
            "result": "deleted"
        }
        return Response(response,status=status.HTTP_204_NO_CONTENT)

#####################################################################################
#               APIVIEWS                                       #                    #
#####################################################################################


class PropertyList_2(APIView):
    def get(self, request):
        properties = Property.objects.all()
        serializer = PropertyModelSerializer(properties, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PropertyModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CommentListApiView(APIView):
    """ Lista de Comentarios """
    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentModelSerializer(comments, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        deserializer = CommentModelSerializer(data=request.data)
        if deserializer.is_valid():
            deserializer.save()
            return Response(deserializer.data, status=status.HTTP_201_CREATED)
        return Response(deserializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CommentDetailApiView(APIView):
    """ Detalles de los comentarios """
    def get_object(self, pk):
        return get_object_or_404(Comment, pk=pk)
    
    def get(self, request, pk):
        comment = self.get_object(pk)
        serializer = CommentModelSerializer(comment, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request, pk):
        comment = self.get_object(pk)
        deserializer = CommentModelSerializer(comment, data=request.data)
        if deserializer.is_valid():
            deserializer.save()
            return Response(deserializer.data)
        return Response(deserializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        comment = self.get_object(pk)
        comment.delete()
        response = {
            "result": "deleted"
        }
        return Response(response,status=status.HTTP_204_NO_CONTENT)

#####################################################################################
#               VIEWSETS                                       #                    #
#####################################################################################
    
class CompanyApiView(viewsets.ViewSet):
    """ Company API view """
    
    def list(self, request):
        companies = Company.objects.all()
        # context = {'request': request}, para el HyperlinkedRelatedField
        serializer = CompanyHyLinkSerializer(companies, many=True, context={'request': request})
        return Response(serializer.data)
    
    def create(self, request):
        serializer = CompanyModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        company = get_object_or_404(Company, pk=pk)
        serializer = CompanyModelSerializer(company, context={'request': request})
        return Response(serializer.data)    
    
    def update(self, request, pk=None):
        company = get_object_or_404(Company, pk=pk)
        serializer = CompanyModelSerializer(company, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request):
        company = get_object_or_404(Company, pk=request.data['id'])
        company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#####################################################################################
#               Company Views                                 #                    #
#####################################################################################

class CompanyListApiView(APIView):
    """ Company List API view """
    
    def get(self, request):
        companies = Company.objects.all()
        # context = {'request': request}, para el HyperlinkedRelatedField
        serializer = CompanyHyLinkSerializer(companies, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        deserializer = CompanyModelSerializer(data=request.data)
        if deserializer.is_valid():
            deserializer.save()
            return Response(deserializer.data, status=status.HTTP_201_CREATED)
        return Response(deserializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CompanyDetailApiView(APIView):
    """ Company Detail API view """
    def get_object(self, pk):
        return get_object_or_404(Company, pk=pk)
    
    def get(self, request, pk):
        company = self.get_object(pk)
        serializer = CompanyModelSerializer(company, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request, pk):
        company = self.get_object(pk)
        deserializer = CompanyModelSerializer(company, data=request.data)
        if deserializer.is_valid():
            deserializer.save()
            return Response(deserializer.data)
        return Response(deserializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        company = self.get_object(pk)
        company.delete()
        response = {
            "result": "deleted"
        }
        return Response(response,status=status.HTTP_204_NO_CONTENT)