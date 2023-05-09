from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

app_name = 'user_app'
urlpatterns = [
    # se utiliza para enviar el token del usuario luego de recibir el usuario y la contraseña
    #path('login/',obtain_auth_token, name='login'),    
    path('login/',views.login, name='login'),    
    # registra un usuario
    path('register/',views.register, name='register'),
    path('logout/',views.logout, name='logout'), 
    # para trabajar con JWT  
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
]