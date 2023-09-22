from django.shortcuts import render
from rest_framework import viewsets

from .models import (
    Jclasificacionesresoluciones,
    Jtiporesoluciones,
    Jresoluciones,
    Jvaloresresoluciones,
)
from .serializers import (
    JclasificacionesresolucionesSerializer,
    JtiporesolucionesSerializer,
    JresolucionesSerializer,
    JvaloresresolucionesSerializer,
)


class JclasificacionesresolucionesViewSet(viewsets.ModelViewSet):
    queryset = Jclasificacionesresoluciones.objects.all()
    serializer_class = JclasificacionesresolucionesSerializer

    
class JtiporesolucionesViewSet(viewsets.ModelViewSet):
    queryset = Jtiporesoluciones.objects.all()
    serializer_class = JtiporesolucionesSerializer


class JresolucionesViewSet(viewsets.ModelViewSet):
    queryset = Jresoluciones.objects.all()
    serializer_class = JresolucionesSerializer


class JvaloresresolucionesViewSet(viewsets.ModelViewSet):
    queryset = Jvaloresresoluciones.objects.all()
    serializer_class = JvaloresresolucionesSerializer
