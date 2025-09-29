from django.urls import path, include 
from rest_framework.routers import DefaultRouter 
from . import views 
 
router = DefaultRouter() 
router.register(r'is-ilanlari', views.IsIlanlariViewSet) 
router.register(r'adaylar', views.AdayViewSet) 
router.register(r'aday-akis', views.AdayAkisViewSet) 
 
urlpatterns = [ 
    path('', include(router.urls)), 
] 
