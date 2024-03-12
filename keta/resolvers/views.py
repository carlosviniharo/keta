from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from reports.utils.helper import format_date
from .utils.helper import send_email
from .models import (
    Jclasificacionesresoluciones,
    Jtiporesoluciones,
    Jresoluciones,
    Jvaloresresoluciones,
    Vresoluciones,
)
from .serializers import (
    JclasificacionesresolucionesSerializer,
    JtiporesolucionesSerializer,
    JresolucionesSerializer,
    JvaloresresolucionesSerializer,
    VresolucionesSerializer,
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
    
    def create(self, request, *args, **kwargs):
        resolution_serializer = JresolucionesSerializer(
            data=request.data.get("resolution"), context={"request": request}
        )
        values_serializer = JvaloresresolucionesSerializer(
            data=request.data.get("values"), context={"request": request}
        )

        try:
            resolution_serializer.is_valid(raise_exception=True)
            values_serializer.is_valid(raise_exception=True)
        except ValidationError as exc:
            raise APIException("There is already a resolution for this "
                               "ticket or the request data is wrong") from exc
    
        idticket = resolution_serializer.validated_data["idtarea"].idtarea
        
        with transaction.atomic():
            try:
                resolution = Jresoluciones.objects.create(**resolution_serializer.validated_data)
                values_serializer.validated_data["idresolucion"] = resolution
                values = Jvaloresresoluciones.objects.create(**values_serializer.validated_data)
                # Mapping and sending the data in an email notification.
                data_resolution = Vresoluciones.objects.get(idtarea=idticket)
                resolution_view = VresolucionesSerializer(data_resolution)
                resolution_email = resolution_view.data
                resolution_email["date"] = format_date(resolution_email["date"])
                send = send_email(resolution_email, "ticket_data_resolutino")
            except Exception as exc:
                raise APIException(exc) from exc
            
        resolution_res = JresolucionesSerializer(resolution, context={"request": request})
        values_res = JvaloresresolucionesSerializer(values, context={"request": request})
        
        return Response(
            {
                # "email": send,
                "resolution": resolution_res.data,
                "values": values_res.data,
            },
            status=status.HTTP_201_CREATED,
        )


class JresolucionesListSet(ListAPIView):
    queryset = Jresoluciones.objects.all()
    serializer_class = JresolucionesSerializer


class JvaloresresolucionesViewSet(viewsets.ModelViewSet):
    queryset = Jvaloresresoluciones.objects.all()
    serializer_class = JvaloresresolucionesSerializer
