from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'estados', JestadosViewSet)
router.register(r'tareas', JtareasticketViewSet)
router.register(r'colours', JestadotareasViewSet)

urlpatterns = [
    path('api/', include(router.urls))
]