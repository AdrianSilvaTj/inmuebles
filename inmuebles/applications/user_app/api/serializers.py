from rest_framework import serializers
from django.contrib.auth.models import User

from ..models import Account

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password', 'write_only': True})
    
    class Meta:
        model = Account
        fields = (
            'username', 'email', 'password', 'password2',
            'first_name', 'last_name', 'phone_number'
        )        
        extra_kwargs = {
            'password': {'write_only': True},
            'password2': {'write_only': True},
                        
        }
    
    def validate (self, obj):
        if Account.objects.filter(email=obj['email']).exists():
            raise serializers.ValidationError({'error': 'El email ya existe'})
        password = obj['password']
        password2 = obj['password2']
        if password!= password2:
            raise serializers.ValidationError({'error': 'El password de confirmación no coincide'})        
        return obj
    
    def save(self):
    #     password = self.validated_data['password']
    #     password2 = self.validated_data['password2']
    #     if password!= password2:
    #         raise serializers.ValidationError({'error': 'El password de confirmación no coincide'})
    #     if User.objects.filter(email=self.validated_data['email']).exists():
    #         raise serializers.ValidationError({'error': 'El email ya existe'})
        account = Account.objects.create_user(
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            email=self.validated_data['email'],
            phone_number=self.validated_data['phone_number'],
            password=self.validated_data['password'],
        )
            
        #account.set_password(self.validated_data['password2'])
        account.save()
        return account
        