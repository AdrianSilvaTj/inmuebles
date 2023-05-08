from rest_framework import serializers
from applications.property.models import Property, Company, Comment

#####################################################################################
#   MODEL SERIALIZERS                                      
#####################################################################################

#####################   Comment serializers    #######################################

class CommentModelSerializer(serializers.ModelSerializer):
    comment_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['id']
        extra_kwargs = {
            'property': {'required': False},            
            'comment_user': {'required': False},            
        }     

#####################   Property serializers    #######################################
def value_length(value):
    """ Funcion para validar la longitud del valor enviado o recibido """
    if len(value)  < 5:
        raise serializers.ValidationError("El valor es muy corto")

class PropertyModelSerializer(serializers.ModelSerializer):
    address_length = serializers.SerializerMethodField()
    comments_list = CommentModelSerializer(many = True, read_only = True)
    class Meta:
        model = Property
        fields = '__all__'
        read_only_fields = ['id']
        extra_kwargs = {
            'address': {'required': True, 'validators': [value_length]},
            'country': {'required': True},            
        }      
    
    def get_address_length(self, object):
        return len(object.address)
    
    def validate(self, data):
        """ Validaciones entre campos """
        if data['address'] == data['country']:
            raise serializers.ValidationError("La direccion y el pais deben ser diferentes.")
        
        property_ver = Property.objects.filter(address=data['address'], country=data['country'])
        if property_ver:
            raise serializers.ValidationError("Esta direccion, en este país ya existe.")

        return data
    
    def validate_image(self, data):
        """ Validaciones entre imagenes """
        if len(data) < 3:
            raise serializers.ValidationError("Url de imagen invalida.")
        return data

class PropertyHyLinkSerializer(serializers.HyperlinkedModelSerializer):
    # .PrimaryKeyRelatedField, regresa el metodo pk del modelo
    #property_list = serializers.PrimaryKeyRelatedField(many = True, read_only = True)
    
    # .StringRelatedField, regresa el metodo __str__ del modelo
    #property_list = serializers.StringRelatedField(many = True)
    
    # .HyperlinkedRelatedField, regresa un enlace para cada detalle
    # comments_list = serializers.HyperlinkedRelatedField(
    #     many = True,
    #     read_only = True,
    #     view_name = 'property:comment-detail',
    #     lookup_field = 'pk'
    # )
    company = serializers.HyperlinkedRelatedField(
        read_only = True,
        view_name = 'property:company-detail',
        lookup_field = 'pk'
    )
    class Meta:
        model = Property
        fields = '__all__'        
        extra_kwargs = {
            'url': {'view_name' : 'property:detail', 'lookup_field': 'pk'}
        }

#####################   Company serializers    #######################################

class CompanyModelSerializer(serializers.ModelSerializer):
    property_list = PropertyModelSerializer(many = True, read_only = True)
    class Meta:
        model = Company
        fields = '__all__'
    
class CompanyHyLinkSerializer(serializers.HyperlinkedModelSerializer):
    # .PrimaryKeyRelatedField, regresa el metodo pk del modelo
    #property_list = serializers.PrimaryKeyRelatedField(many = True, read_only = True)
    
    # .StringRelatedField, regresa el metodo __str__ del modelo
    #property_list = serializers.StringRelatedField(many = True)
    
    # .HyperlinkedRelatedField, regresa un enlace para cada detalle
    property_list = serializers.HyperlinkedRelatedField(
        many = True,
        read_only = True,
        view_name = 'property:detail',
        lookup_field = 'pk'
    )  
        
    class Meta:
        model = Company
        fields = '__all__'        
        extra_kwargs = {
            'url': {'view_name' : 'property:company-detail', 'lookup_field': 'pk'}
        }