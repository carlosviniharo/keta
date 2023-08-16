import sys

from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
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
            persona = Jpersonas.objects.create(**persona_data)
            user = Jusuarios.objects.create_user(**user_data)
            user.idpersona = persona

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class JpersonasRegisterView(APIView):

    def get(self, request):
        jpersonas = Jpersonas.objects.all()
        serializer = JpersonasSerializer(jpersonas, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = JpersonasSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        identificacion = serializer.validated_data.get('identificacion')
        try:
            Jpersonas.objects.get(identificacion=identificacion)
        except ObjectDoesNotExist:
            serializer.save()
        else:
            return Response(
                {"detail": f"The person with this ID {identificacion} already exists"},
                status=status.HTTP_208_ALREADY_REPORTED
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# View from retrieving all static tables.
# TODO: Restrict the access to the services with IsAuthenticated.
# Base class for classe which retrieves  all the fields of the tables
class BaseListView(ListAPIView):
    queryset = None
    serializer_class = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        model_name = self.__class__.__name__[:-8]  # Remove "ListView" from the class name
        model = apps.get_model('users', model_name)

        self.queryset = model.objects.all()

        serializer_name = f"{model_name}Serializer"
        serializer_class = getattr(sys.modules[__name__], serializer_name)
        self.serializer_class = serializer_class


class JcargosListView(BaseListView):
    pass


class JdepartamentosListView(BaseListView):
    pass


class JcorporacionesListView(BaseListView):
    pass


class JgenerosListView(BaseListView):
    pass


class JgeografiaListView(BaseListView):
    pass


class JrolesListView(BaseListView):
    pass


class JsucursalesListView(BaseListView):
    pass


class JtiposidentificacionesListView(BaseListView):
    pass


class JtipospersonasListView(BaseListView):
    pass


# Retrieve the user using the column email.
class JusuarioRegisterView(RetrieveAPIView):
    queryset = Jusuarios.objects.all()
    serializer_class = JusuariosSerializer
    lookup_field = 'email'


# Retrieve the user static tables using id of each table.
class JcargoRegisterView(RetrieveAPIView):
    queryset = Jcargos.objects.all()
    serializer_class = JcargosSerializer
    lookup_field = 'idcargo'


class JroleRegisterView(RetrieveAPIView):
    queryset = Jroles.objects.all()
    serializer_class = JrolesSerializer
    lookup_field = 'idrol'


class JsucursalRegisterView(RetrieveAPIView):
    queryset = Jsucursales.objects.all()
    serializer_class = JsucursalesSerializer
    lookup_field = 'idsucursal'


class JpersonaRegisterView(RetrieveAPIView):
    queryset = Jpersonas.objects.all()
    serializer_class = JpersonasSerializer
    lookup_field = 'idpersona'


class JdepartamentoRegisterView(RetrieveAPIView):
    queryset = Jdepartamentos.objects.all()
    serializer_class = JdepartamentosSerializer
    lookup_field = 'iddepartamento'


class JtipospersonaRegisterView(RetrieveAPIView):
    queryset = Jtipospersonas.objects.all()
    serializer_class = JtipospersonasSerializer
    lookup_field = 'idtipopersona'


# Retrieve all the departamentos of each sucursal.
class JsucursalJdepartamentosListView(ListAPIView):

    serializer_class = JdepartamentosSerializer

    def get_queryset(self):
        idsucursal = self.request.query_params.get('idsucursal', None)
        return Jdepartamentos.objects.filter(idsucursal=idsucursal)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not queryset.exists():
            return Response(
                {f"detail": "idsucursal " + request.query_params.get('idsucursal')
                            + " was not found in the records"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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
