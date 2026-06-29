
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *



router=DefaultRouter()

router.register('signup', ReqisterViewSet, basename='signup' )
router.register('login', LoginViewSet, basename='login')
router.register('user', UserViewSet, basename='user')


urlpatterns =router.urls
