import sys

from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response

from .serializers import *
from .utils import helper


# Views for registering users and persons
class JusuariosViewSet(viewsets.ModelViewSet):
    queryset = Jusuarios.objects.all()
    serializer_class = JusuariosSerializer

    # def create(self, request):
    #     persona_serializer = JpersonasSerializer(data=request.data["persona"])
    #     usuario_serializer = JusuariosSerializer(data=request.data["usuario"])
    #
    #     # Extract the data from the serializer
    #     persona_serializer.is_valid(raise_exception=True)
    #     usuario_serializer.is_valid(raise_exception=True)
    #
    #     # Use a database transaction to ensure atomicity
    #     with transaction.atomic():
    #         # Create the user instance
    #         persona = persona_serializer.save()
    #         usuario_data = usuario_serializer.validated_data
    #         usuario_data["idpersona"] = None
    #         usuario_data["last_name"] = persona.apellido
    #         usuario_data["first_name"] = persona.nombre
    #         usuario_data["direccionmac"] = helper.get_mac_address()
    #         usuario_data["ipcreacion"] = helper.get_public_ip_address()
    #         usuario_data["date_joined"] = timezone.now()
    #         user = Jusuarios.objects.create_user(**usuario_data)
    #         user.idpersona = persona
    #
    #     return Response(
    #         {
    #             "persona": persona_serializer.data,
    #             "usuario": usuario_serializer.data,
    #             "user_link": self.get_serializer_context().get('request').build_absolute_uri(user.get_absolute_url()),
    #         },
    #         status=status.HTTP_201_CREATED
    #     )


class JpersonasViewSet(viewsets.ModelViewSet):
    queryset = Jpersonas.objects.all()
    serializer_class = JpersonasSerializer

    def create(self, request, *args, **kwargs):
        identificacion = request.data.get("identificacion")

        if Jpersonas.objects.filter(identificacion=identificacion).exists():
            return Response(
                {"detail": f"The person with this ID {identificacion} already exists"},
                status=status.HTTP_409_CONFLICT,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


# View from retrieving all static tables.
# TODO: Restrict the access to the services with IsAuthenticated.
class JcargosViewSet(viewsets.ModelViewSet):
    queryset = Jcargos.objects.all()
    serializer_class = JcargosSerializer


class JdepartamentosViewSet(viewsets.ModelViewSet):
    queryset = Jdepartamentos.objects.all()
    serializer_class = JdepartamentosSerializer


class JcorporacionesViewSet(viewsets.ModelViewSet):
    queryset = Jcorporaciones.objects.all()
    serializer_class = JcorporacionesSerializer


class JgenerosViewSet(viewsets.ModelViewSet):
    queryset = Jgeneros.objects.all()
    serializer_class = JgenerosSerializer


class JgeografiaViewSet(viewsets.ModelViewSet):
    queryset = Jgeografia.objects.all()
    serializer_class = JgeografiaSerializer


class JrolesListViewSet(viewsets.ModelViewSet):
    queryset = Jroles.objects.all()
    serializer_class = JrolesSerializer


class JsucursalesViewSet(viewsets.ModelViewSet):
    queryset = Jsucursales.objects.all()
    serializer_class = JsucursalesSerializer


class JtiposidentificacionesViewSet(viewsets.ModelViewSet):
    queryset = Jtiposidentificaciones.objects.all()
    serializer_class = JtiposidentificacionesSerializer


class JtipospersonasViewSet(viewsets.ModelViewSet):
    queryset = Jtipospersonas.objects.all()
    serializer_class = JtipospersonasSerializer


# Retrieve the user using the column email.
class JusuarioRegisterView(RetrieveAPIView):
    queryset = Jusuarios.objects.all()
    serializer_class = JusuariosSerializer
    lookup_field = "email"


# Retrieve all the departamentos of each sucursal.
class JsucursalJdepartamentosListView(ListAPIView):
    serializer_class = JdepartamentosSerializer

    def get_queryset(self):
        idsucursal = self.request.query_params.get("idsucursal", None)
        return Jdepartamentos.objects.filter(idsucursal=idsucursal)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not queryset.exists():
            return Response(
                {
                    f"detail": "idsucursal "
                    + request.query_params.get("idsucursal")
                    + " was not found in the records"
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# View from login and logout.
class CustomTokenObtainPairView(TokenObtainPairView):
    """
    An endpoint to login users.
    """
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            # Update the last_login field for the user upon successful login
            user = Jusuarios.objects.get(email=request.data["email"])
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
            return Response(
                {"detail": "Successfully logged out."},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            print(e)
            return Response(
                {"error": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST
            )
