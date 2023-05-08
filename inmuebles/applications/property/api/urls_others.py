from django.urls import path
from . import views_others

# Haciendo los procesos pero de varias maneras
app_name = 'property'
urlpatterns = [
    path('function/',views_others.property_list, name='list'),
    path('function/<pk>/',views_others.property_detail, name='detail'),
    path('apiview_2/',views_others.PropertyList_2.as_view(), name='apiview_list2'),    
]