from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response


# view for registering users
class JusuariosRegisterView(APIView):
    def post(self, request):
        serializer = JusuariosSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# View from retrieving all cargos.
class JcargosListView(APIView):
    def get(self, request):
        jcargos = Jcargos.objects.all()
        serializer = JcargosSerializer(jcargos, many=True)
        return Response(serializer.data)


class JdepartamentosListView(APIView):

    def get(self, request):
        jdepartamentos = Jdepartamentos.objects.all()
        serializer = JdepartamentosSerializer(jdepartamentos, many=True)
        return Response(serializer.data)


class JcorporacionesListView(APIView):

    def get(self, request):
        jcorporaciones = Jcorporaciones.objects.all()
        serializer = JcorporacionesSerializer(jcorporaciones, many=True)
        return Response(serializer.data)


class JgenerosListView(APIView):
    def get(self,request):
        jgeneros = Jgeneros.objects.all()
        serializer = JgenerosSerializer(jgeneros, many=True)
        return Response(serializer.data)


class JgeografiaListView(APIView):
    def get(self, request):
        jgeografia = Jgeografia.objects.all()
        serializer = JgeografiaSerializer(jgeografia, many=True)
        return Response(serializer.data)


class JrolesListView(APIView):
    def get(self, request):
        jroles = Jroles.objects.all()
        serializer = JrolesSerializer(jroles, many=True)
        return Response(serializer.data)


class JsucursalesListView(APIView):
    def get(self, request):
        jsucursales = Jsucursales.objects.all()
        serializer = JsucursalesSerializer(jsucursales, many=True)
        return Response(serializer.data)


class JtipoidentificacionesListView(APIView):
    def get(self, request):
        jtipoidentificaciones = Jtipoidentificaciones.objects.all()
        serializer = JtipoidentificacionesSerializer(jtipoidentificaciones, many=True)
        return Response(serializer.data)


class JtipopersonasListView(APIView):
    def get(self, request):
        jtipopersonas = Jtipopersonas.objects.all()
        serializer = JtipopersonasSerializer(jtipopersonas, many=True)
        return Response(serializer.data)


class JpersonasRegisterView(APIView):

    def get(self,request):
        jpersonas = Jpersonas.objects.all()
        serializer = JpersonasSerializer(jpersonas, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = JpersonasSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
