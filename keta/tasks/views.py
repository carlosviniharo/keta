from django.shortcuts import render
from rest_framework import viewsets

from .serializers import *
from .models import Jtareasticket


class JtareasticketViewSet(viewsets.ModelViewSet):
    queryset = Jtareasticket.objects.all()
    serializer_class = JtareasticketSerializer


class JestadotareasViewSet(viewsets.ModelViewSet):
    queryset = Jestadotareas.objects.all()
    serializer_class = JestadotareasSerializers


class JestadosViewSet(viewsets.ModelViewSet):
    queryset = Jestados.objects.all()
    serializer_class = JestadosSerializer