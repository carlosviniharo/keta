from django.db import transaction
from django.utils import timezone
from rest_framework import status
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
        jtipoidentificaciones = Jtiposidentificaciones.objects.all()
        serializer = JtipoidentificacionesSerializer(jtipoidentificaciones, many=True)
        return Response(serializer.data)


class JtipopersonasListView(APIView):
    def get(self, request):
        jtipopersonas = Jtipospersonas.objects.all()
        serializer = JtipopersonasSerializer(jtipopersonas, many=True)
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
