from django.urls import path, include
from . import views
from . import routers

# Haciendo los procesos pero de varias maneras
app_name = 'property'
urlpatterns = [
    path('property/',views.PropertyList.as_view(), name='list'),
    path('property/<pk>/',views.PropertyDetail.as_view(), name='detail'),
    path('property/<pk>/comment/',views.CommentListCreateApiView.as_view(), name='comment-list'),
    path('property/<id_prop>/comment/<pk>/',views.CommentDetailApiView.as_view(), name='comment-detail'),
    path('property_filter_list/',views.PropertyFilterList.as_view(), name='filter-list'),
    #path('user_comment/<username>/',views.UserCommentList.as_view(), name='user-comment-list'),
    path('user_comment/',views.UserCommentList.as_view(), name='user-comment-list'),
    path('', include(routers.router.urls)),
    # path('company/',views.CompanyListApiView.as_view(), name='company-list'),
    # path('company/<pk>/',views.CompanyDetailApiView.as_view(), name='company-detail'),
    
]