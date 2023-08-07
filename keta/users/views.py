import sys
import logging

from django.apps import apps
from django.db import transaction
from django.http import Http404
from django.template.response import ContentNotRenderedError
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response

from .serializers import *
from .utils import helper


# view for registering users and persons
class JusuariosRegisterView(APIView):

    def get(self, request):
        jusuarios = Jusuarios.objects.all()
        serializer = JusuariosSerializer(jusuarios, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = JpersonasUsuariosSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract the data from the serializer
        persona_data = serializer.validated_data.get('persona', {})
        user_data = serializer.validated_data.get('usuario', {})

        # Use a database transaction to ensure atomicity
        with transaction.atomic():
            # Create the user instance
            user_data['idpersona'] = None
            user_data['last_name'] = persona_data.get('apellido')
            user_data['first_name'] = persona_data.get('nombre')
            user_data['direccionmac'] = helper.get_mac_address()
            user_data['ipcreacion'] = helper.get_public_ip_address()
            user_data['date_joined'] = timezone.now()
            user = Jusuarios.objects.create_user(**user_data)

            # Create the persona instance and associate it with the user
            persona_data['idpersona'] = user.idpersona
            persona = Jpersonas.objects.create(**persona_data)
            user.idpersona = persona
            user.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class JususarioRegisterView(RetrieveAPIView):
    queryset = Jusuarios.objects.all()
    serializer_class = JusuariosSerializer
    lookup_field = 'email'



class JpersonasRegisterView(APIView):

    def get(self, request):
        jpersonas = Jpersonas.objects.all()
        serializer = JpersonasSerializer(jpersonas, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = JpersonasSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# View from retrieving all static tables.
# TODO: Restrict the access to the services with IsAuthenticated.
# Base class for classe which retrieves allways all the fields of the tables
class BaseListView(ListAPIView):
    queryset = None
    serializer_class = None


# Metaclass to customize the initialization of the classes
class ListViewMeta(type):
    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, name, bases, attrs)

        model_name = name[:-8]  # Remove "ListView" from the class name
        model = apps.get_model('users', model_name)

        new_class.queryset = model.objects.all()

        serializer_name = f"{model_name}Serializer"
        serializer_class = getattr(sys.modules[__name__], serializer_name)
        new_class.serializer_class = serializer_class

        return new_class


class JcargosListView(BaseListView, metaclass=ListViewMeta):
    pass


class JdepartamentosListView(BaseListView, metaclass=ListViewMeta):
    pass


class JcorporacionesListView(BaseListView, metaclass=ListViewMeta):
    pass


class JgenerosListView(BaseListView, metaclass=ListViewMeta):
    pass


class JgeografiaListView(BaseListView, metaclass=ListViewMeta):
    pass


class JrolesListView(BaseListView, metaclass=ListViewMeta):
    pass


class JsucursalesListView(BaseListView, metaclass=ListViewMeta):
    pass


class JtiposidentificacionesListView(BaseListView, metaclass=ListViewMeta):
    pass


class JtipospersonasListView(BaseListView, metaclass=ListViewMeta):
    pass


# Retrieve only the departamentos of each sucursal.
class JsucursalJdepartamentosListView(ListAPIView):
    serializer_class = JdepartamentosSerializer

    def get_queryset(self):
        idsucursal = self.request.query_params.get('idsucursal', None)
        return Jdepartamentos.objects.filter(idsucursal=idsucursal)


# View from login and logout.
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            # Update the last_login field for the user upon successful login
            user = Jusuarios.objects.get(email=request.data['email'])
            user.last_login = timezone.now()
            user.save()

        return response


# TODO: Implement token pruning mechanism to clean up the blacklist. Tokens
#  from logged-out users are added to the blacklist, which can grow large
#  over time.To prevent performance issues and optimize database usage,
#  periodically remove expired tokens.Use a scheduled task to run at
#  regular intervals for this cleanup.
class CustomLogoutView(APIView):
    """
    An endpoint to logout users.
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(e)
            return Response({"error": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)
