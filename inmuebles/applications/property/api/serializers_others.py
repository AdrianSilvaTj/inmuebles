from rest_framework import serializers
from applications.property.models import Property, Company, Comment

#####################################################################################
# serializers.Serializer                                      
#####################################################################################

def value_length(value):
    """ Funcion para validar la longitud del valor enviado o recibido """
    if len(value)  < 5:
        raise serializers.ValidationError("El valor es muy corto")

class PropertySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    # validators, indica funciones para validar ese atributo
    address = serializers.CharField(validators = [value_length])
    country = serializers.CharField(validators = [value_length])
    image = serializers.CharField()
    description = serializers.CharField(validators = [value_length])
    active = serializers.BooleanField()
    
    def create(self, validated_data):
        """ Crea un registro para Property """
        return Property.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """ Actualiza un registro de Property """
        instance.address = validated_data.get('address', instance.address)
        instance.country = validated_data.get('country', instance.country)
        instance.image = validated_data.get('image', instance.image)
        instance.description = validated_data.get('description', instance.description)
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance    
    
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
    