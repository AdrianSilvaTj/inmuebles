from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from ..models import Account
from .serializers import UserSerializer, User

@api_view(['POST'])
def logout(request):
    request.user.auth_token.delete()
    return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def login(request):
    data={}
    if request.method == 'POST':        
        email = request.data.get('email')
        password = request.data.get('password')
        account = authenticate(request, email=email, password=password)
        
        if account is not None:
            data['response'] = 'El Login fue exitoso'
            data['username'] = account.username
            data['email'] = account.email
            data['first_name'] = account.first_name
            data['last_name'] = account.last_name
            data['phone_number'] = account.phone_number
            refresh = RefreshToken.for_user(account)
            data['token'] = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data['error'] = 'Usuario o contraseña incorrectos'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    data ={}
    if serializer.is_valid(): 
        account = serializer.save()
        data['response'] = "Usuario Creado"
        data['username'] = account.username
        data['email'] = account.email       
        data['first_name'] = account.first_name
        data['last_name'] = account.last_name
        data['phone_number'] = account.phone_number
        
        # *************************************************************
        # Asignar token 
        # token = Token.objects.get(user=acount).key
        # data['token'] = token
        
        # Asignar token JWT
        refresh = RefreshToken.for_user(account)
        data['token'] = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return Response(data, status=status.HTTP_201_CREATED)
    else:
        data = serializer.errors       
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def session_view(request):
    if request.method == 'GET':
        user = request.user
        account = Account.objects.get(email=user)
        data= {}
        if account is not None:
            data['response'] = 'El usuario esta en sesión'
            data['username'] = account.username
            data['email'] = account.email
            data['first_name'] = account.first_name
            data['last_name'] = account.last_name
            data['phone_number'] = account.phone_number
            refresh = RefreshToken.for_user(account)
            data['token'] = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data['error'] = 'El Usuario no existe'
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
