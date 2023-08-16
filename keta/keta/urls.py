"""
URL configuration for keta project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from tickets.views import *

router = DefaultRouter()
router.register(r'canalesrecepciones', JcanalesrecepcionesViewSet)
router.register(r'clasestarjetas', JclasestarjetasViewSet)
router.register(r'tiposproductos', JtiposproductosViewSet)
router.register(r'conceptos', JconceptosViewSet)
router.register(r'marcastarjetas', JmarcastarjetasViewSet)
router.register(r'prioridades', JprioridadesViewSet)
router.register(r'tipostarjetas', JtipostarjetasViewSet)
router.register(r'tarjetas', JtarjetasViewSet)
router.register(r'tiposcomentarios', JtiposcomentariosViewSet)
router.register(r'tickettipos', JtickettiposViewSet)
router.register(r'tipostransacciones', JtipostransaccionesViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('tickets/', include('tickets.urls')),
    path(r'api/tickets/', include(router.urls)),
]
