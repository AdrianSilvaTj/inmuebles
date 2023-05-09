from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle

from applications.property.models import Property, Company, Comment
from .serializers import (
    PropertyModelSerializer, PropertyHyLinkSerializer , CompanyModelSerializer,
    CompanyHyLinkSerializer, CommentModelSerializer,
)
from .permissions import IsAdminOrReadOnly, IsCommentUserOrReadOnly
from .throttlings import CommentCreateThrottle, CommentListThrottle
from .pagination import PropertyPagination, PropertyLimitOffsetPag

#####################################################################################
#               Property Views                                 #                    #
#####################################################################################
class PropertyList(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request):
        properties = Property.objects.all()
        serializer = PropertyHyLinkSerializer(properties, many=True, context={'request': request})
        # Actualizando los datos ya existentes en la BD al momento de agregar los campos: calification_count y calification_count 
        #
        # arrproperty = []
        # for property in properties:
        #     coments_pro = Comment.objects.filter(property=property)
        #     property.calification_count = coments_pro.count()
        #     if coments_pro.exists():
        #         result = coments_pro.aggregate(
        #             cal_avg = Avg('calification'),
        #             cal_sum = Sum('calification')
        #             )
        #         print (result['cal_avg'])
        #         property.calification_sum = result['cal_sum']
        #         property.calification_avg = round(result['cal_avg'],1)
        #     arrproperty.append(property)
        # Property.objects.bulk_update(arrproperty, ['calification_count', 'calification_avg', 'calification_sum'])
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PropertyModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PropertyDetail(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get_object(self, pk):
        return get_object_or_404(Property, pk=pk)
    
    def get(self, request, pk):
        property = self.get_object(pk)
        serializer = PropertyModelSerializer(property)
        return Response(serializer.data)
    
    def put(self, request, pk):
        property = self.get_object(pk)
        serializer = PropertyModelSerializer(property, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        property = self.get_object(pk)
        property.delete()
        response = {
            "result": "deleted"
        }
        return Response(response,status=status.HTTP_204_NO_CONTENT)
    
class PropertyFilterList(ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyModelSerializer
    # Realizar busquedas con partes de la palabra
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['address', 'company__name', 'country']
    pagination_class = PropertyPagination
    #pagination_class = PropertyLimitOffsetPag
    
#####################################################################################
#               Company Views                                 #                    #
#####################################################################################

# En viewset.py
    
#####################################################################################
#               Comment Views                                 #                    #
#####################################################################################

class CommentListCreateApiView(ListCreateAPIView):
    """ Lista y Crea Comentarios de un propiedad """
    serializer_class = CommentModelSerializer
    # permission_classes = [IsAuthenticated]
    # Se utiliza para restringir el acceso a los usuarios segun la cantidad de peticiones por dia
    #throttle_classes = [UserRateThrottle, AnonRateThrottle]
    throttle_classes = [CommentListThrottle, AnonRateThrottle]
    # hacer peticiones con filtros automatizados, sin tener que redefinir el queryset
    # solo colocando en la petición: ?comment_user__username=adrian o ?active=True
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['comment_user__username', 'active'] 
        
    def get_queryset(self):
        """ Filtra los comentarios por la propiedad """       
        property_sel = (get_object_or_404(Property, pk=self.kwargs['pk']))
        return Comment.objects.filter(property = property_sel.id)
    
    def perform_create(self, serializer):
        """ Crea un comentario para la propiedad enviada """
        pk = self.kwargs.get('pk')
        # verifica que exista la propiedad
        property_sel = get_object_or_404(Property, pk=pk)
        # Validar que el usuario solo pueda hacer un comentario por propiedad
        user = self.request.user
        comment_qry = Comment.objects.filter(
            property = property_sel,
            comment_user = user
        )
        if comment_qry.exists():
            raise ValidationError("Ya existe un comentario de este usuario para esta propiedad")
        
        property_sel.calification_count = property_sel.calification_count + 1
        property_sel.calification_sum = property_sel.calification_sum + serializer.validated_data['calification']                
        property_sel.calification_avg = round(property_sel.calification_sum / property_sel.calification_count, 1)        
        property_sel.save()

        # setea el valor property con property_sel, para el nuevo registro a crear        
        serializer.save(property = property_sel, comment_user = user)
    
    
class CommentDetailApiView(RetrieveUpdateDestroyAPIView):
    """ Detalle de un comentario """
    serializer_class = CommentModelSerializer
    permission_classes = [IsCommentUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'comment-detail'
    
    def get_queryset(self):
        """ Filtra el comentarios por la propiedad """        
        return Comment.objects.filter(property = self.kwargs['id_prop'])
    
class UserCommentList(ListAPIView):
    serializer_class = CommentModelSerializer
    
    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Comment.objects.filter(comment_user = username)
    
    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        return Comment.objects.filter(comment_user__username = username)
    