from django.db import transaction, IntegrityError
from django.utils import timezone

from rest_framework import status, viewsets
from rest_framework.exceptions import APIException
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response

from .utils.helper import BaseViewSet

from .serializers import (
    JusuariosSerializer,
    JpersonasSerializer,
    JcargosSerializer,
    JdepartamentosSerializer,
    JdiasfestivosSerializer,
    JcorporacionesSerializer,
    JgenerosSerializer,
    JgeografiaSerializer,
    JrolesSerializer,
    JsucursalesSerializer,
    JtiposidentificacionesSerializer,
    JtipospersonasSerializer,
    VusuariosSerializer,

)
from .models import (
    Jusuarios,
    Jpersonas,
    Jcargos,
    Jdepartamentos,
    Jdiasfestivos,
    Jcorporaciones,
    Jgeneros,
    Jgeografia,
    Jroles,
    Jsucursales,
    Jtiposidentificaciones,
    Jtipospersonas,
    Vusuarios,
)


# Views for registering users and persons
class JusuariosViewSet(BaseViewSet):
    queryset = Jusuarios.objects.all()
    serializer_class = JusuariosSerializer
    # permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        persona_serializer = JpersonasSerializer(
            data=request.data["persona"], context={"request": request}
        )
        usuario_serializer = JusuariosSerializer(
            data=request.data["usuario"], context={"request": request}
        )

        # Extract the data from the serializer
        persona_serializer.is_valid(raise_exception=True)
        usuario_serializer.is_valid(raise_exception=True)

        identificacion = persona_serializer.validated_data["identificacion"]

        # Use a database transaction to ensure atomicity
        with transaction.atomic():
            # Create the user instance
            existing_persona, created = Jpersonas.objects.update_or_create(
                identificacion=identificacion,
                defaults=persona_serializer.validated_data,
            )

            usuario_data = usuario_serializer.validated_data
            usuario_data["idpersona"] = existing_persona
            usuario_data["last_name"] = existing_persona.apellido
            usuario_data["first_name"] = existing_persona.nombre
            user = Jusuarios.objects.create_user(**usuario_data)
            user_serializer = JusuariosSerializer(user, context={"request": request})
            person_serializer = JpersonasSerializer(
                existing_persona, context={"request": request}
            )
        return Response(
            {
                "persona": person_serializer.data,
                "usuario": user_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        newpassword = serializer.validated_data.pop("password", None)

        if newpassword:
            instance.set_password(newpassword)
            instance.save()
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data, status=status.HTTP_200_OK)


class JpersonasViewSet(BaseViewSet):
    queryset = Jpersonas.objects.all()
    serializer_class = JpersonasSerializer
    # permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        persona, created = Jpersonas.objects.update_or_create(
            identificacion=serializer.validated_data["identificacion"],
            defaults=serializer.validated_data,
        )
        person_serializer = JpersonasSerializer(persona, context={"request": request})

        return Response(
            {"new person": f"{created}", "persona": person_serializer.data},
            status=status.HTTP_201_CREATED,
        )


# View from retrieving all static tables.
# TODO: Restrict the access to the services with IsAuthenticated.
class JcargosViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = Jcargos.objects.all()
    serializer_class = JcargosSerializer


class JdepartamentosViewSet(viewsets.ModelViewSet):
    queryset = Jdepartamentos.objects.all()
    serializer_class = JdepartamentosSerializer


class JdiasfestivosViewSet(BaseViewSet):
    queryset = Jdiasfestivos.objects.all()
    serializer_class = JdiasfestivosSerializer

    def create(self, request, *args, **kwargs):
        hollidays_data = request.data
        instances = []
        for index, date in enumerate(hollidays_data["fecha"]):
            if index == 0:
                index = ""
            instances.append(
                Jdiasfestivos(
                    descripciondiasfestivos=f"{hollidays_data['descripciondiasfestivos']} {index}",
                    fecha=date
                )
            )

        try:
            created_instances = Jdiasfestivos.objects.bulk_create(instances)
        except IntegrityError as e:
            # Handle the IntegrityError here
            raise APIException(f"Repeated record, details:{e}")

        return Response({"Number of records created": len(created_instances)})


class JdiasfestivosActiveView(ListAPIView):
    serializer_class = JdiasfestivosSerializer
    queryset = Jdiasfestivos.objects.filter(status=True)


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
class JusuarioListView(RetrieveUpdateAPIView):
    queryset = Jusuarios.objects.all()
    serializer_class = JusuariosSerializer
    lookup_field = "email"


class JpersonasListView(viewsets.ModelViewSet):
    queryset = Jpersonas.objects.all()
    serializer_class = JpersonasSerializer
    lookup_field = "identificacion"


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
                    "detail": "idsucursal "
                    + f"{request.query_params.get('idsucursal')}"
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


# TODO: Implement token pruning mechanism to clean up the blacklist.
class CustomLogoutView(APIView):
    """
    An endpoint to logout users.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"detail": "Successfully logged out."},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as exc:
            return Response(
                {"error": f"Invalid refresh token. verbose {exc}"}, status=status.HTTP_400_BAD_REQUEST
            )


# Views for reports
class VusuariosReportView(ListAPIView):
    queryset = Vusuarios.objects.all()
    serializer_class = VusuariosSerializer


class VusuariosActiveView(ListAPIView):
    serializer_class = VusuariosSerializer

    def get_queryset(self):
        return Vusuarios.objects.filter(is_active=True)


class VusuariosAsignationView(ListAPIView):
    serializer_class = VusuariosSerializer
    
    def get_queryset(self):
        return Vusuarios.objects.filter(rol__in=["Supervisor", "Tecnico"])
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response(
                {
                    "detail": "No users with role Supervisor or "
                              "Tecnico was not found in the records"
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        
    