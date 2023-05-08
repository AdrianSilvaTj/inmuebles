from rest_framework.routers import DefaultRouter

from .viewsets import CompanyModelViewset

router = DefaultRouter()

router.register('company', CompanyModelViewset, basename='company') 