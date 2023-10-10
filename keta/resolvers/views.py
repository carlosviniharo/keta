from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .utils.helper import send_email
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

dictionary_example = {
    "emailcliente": "carlosviniharo@outlook.com",
    "fullname": "Vanessa",
    "apellido": "Cabascango",
    "date": "2023/10/10",
    "agencia": "Otavalo",
}




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
        email = send_email(dictionary_example)
        print(email)
        try:
            resolution_serializer.is_valid(raise_exception=True)
            values_serializer.is_valid(raise_exception=True)
        except ValidationError:
            raise APIException("There is already a resolution for this ticket")
    
        ticket = resolution_serializer
        
        with transaction.atomic():
            try:
                resolution = Jresoluciones.objects.create(**resolution_serializer.validated_data)
                values_serializer.validated_data["idresolucion"] = resolution
                values = Jvaloresresoluciones.objects.create(**values_serializer.validated_data)
            except Exception as e:
                raise APIException(e)
            
        resolution_res = JresolucionesSerializer(resolution, context={"request": request})
        values_res = JvaloresresolucionesSerializer(values, context={"request": request})
        
        return Response(
            {
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
