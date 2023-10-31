from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from rest_framework import serializers

from .serializers import (
    JcanalesrecepcionesSerializer,
    JclasestarjetasSerializer,
    JtiposproductosSerializer,
    JconceptosSerializer,
    JmarcastarjetasSerializer,
    JprioridadesSerializer,
    JtipostarjetasSerializer,
    JtarjetasSerializer,
    JtiposcomentariosSerializer,
    JtickettiposSerializer,
    JtipostransaccionesSerializer,
    JproblemasSerializer,
)
from .models import (
    Jcanalesrecepciones,
    Jclasestarjetas,
    Jtiposproductos,
    Jconceptos,
    Jmarcastarjetas,
    Jprioridades,
    Jtipostarjetas,
    Jtarjetas,
    Jtiposcomentarios,
    Jtickettipos,
    Jtipostransacciones,
    Jproblemas,
)

from users.models import Jpersonas
from users.serializers import JpersonasSerializer

CARD_TICKET_TYPE = 2


class JcanalesrecepcionesViewSet(viewsets.ModelViewSet):
    queryset = Jcanalesrecepciones.objects.all()
    serializer_class = JcanalesrecepcionesSerializer


class JclasestarjetasViewSet(viewsets.ModelViewSet):
    queryset = Jclasestarjetas.objects.all()
    serializer_class = JclasestarjetasSerializer


class JtiposproductosViewSet(viewsets.ModelViewSet):
    queryset = Jtiposproductos.objects.all()
    serializer_class = JtiposproductosSerializer


class JconceptosViewSet(viewsets.ModelViewSet):
    queryset = Jconceptos.objects.all()
    serializer_class = JconceptosSerializer


class JmarcastarjetasViewSet(viewsets.ModelViewSet):
    queryset = Jmarcastarjetas.objects.all()
    serializer_class = JmarcastarjetasSerializer


class JprioridadesViewSet(viewsets.ModelViewSet):
    queryset = Jprioridades.objects.all()
    serializer_class = JprioridadesSerializer


class JtipostarjetasViewSet(viewsets.ModelViewSet):
    queryset = Jtipostarjetas.objects.all()
    serializer_class = JtipostarjetasSerializer


class JtarjetasViewSet(viewsets.ModelViewSet):
    queryset = Jtarjetas.objects.all()
    serializer_class = JtarjetasSerializer


class JtiposcomentariosViewSet(viewsets.ModelViewSet):
    queryset = Jtiposcomentarios.objects.all()
    serializer_class = JtiposcomentariosSerializer


class JtickettiposViewSet(viewsets.ModelViewSet):
    queryset = Jtickettipos.objects.all()
    serializer_class = JtickettiposSerializer


class JtipostransaccionesViewSet(viewsets.ModelViewSet):
    queryset = Jtipostransacciones.objects.all()
    serializer_class = JtipostransaccionesSerializer


# Customize methods to get certain types of field in the tables.
class JtiposproductosJconceptosListView(ListAPIView):
    queryset = Jconceptos.objects.all()
    serializer_class = JconceptosSerializer

    def list(self, request, *args, **kwargs):
        queryset = Jconceptos.objects.filter(
            idtipoproducto=self.kwargs.get("idtipoproducto")
        )
        if not queryset.exists():
            return Response(
                {
                    "detail": "idtipoproducto "
                    + f"{self.idtipoproducto}"
                    + " was not found in the records"
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class JproblemasViewSet(viewsets.ModelViewSet):
    queryset = Jproblemas.objects.all()
    serializer_class = JproblemasSerializer

    def create(self, request, *args, **kwargs):
        personas_serializer = JpersonasSerializer(
            data=request.data.get("persona"), context={"request": request}
        )
        tarjeta_serializer = JtarjetasSerializer(
            data=request.data.get("tarjeta"), context={"request": request}
        )
        problemas_serializer = JproblemasSerializer(
            data=request.data.get("ticket"), context={"request": request}
        )

        personas_serializer.is_valid(raise_exception=True)
        problemas_serializer.is_valid(raise_exception=True)

        tipo_ticket = problemas_serializer.validated_data["idtipoticket"]
        data_ticket = problemas_serializer.validated_data

        if tipo_ticket.idtipoticket == CARD_TICKET_TYPE:
            try:
                tarjeta_serializer.is_valid(raise_exception=True)
            except serializers.ValidationError as er:
                return Response(
                    {
                        "detail": f" Validation failed, please include tarjeta in the request, verbose {er}"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            tarjeta, created = self.create_tarjeta(tarjeta_serializer.validated_data)
            data_ticket["idtarjeta"] = tarjeta
            tarjeta = JtarjetasSerializer(
                tarjeta, context={"request": request}
            ).data
            
        else:
            tarjeta = {}
            created = False

        with transaction.atomic():
            persona, created_persona = self.create_persona(
                personas_serializer.validated_data
            )

            data_ticket["idpersona"] = persona

            try:
                ticket = Jproblemas.objects.create(**data_ticket)
            except ValidationError as e:
                return Response({"detail": e}, status=status.HTTP_403_FORBIDDEN)

            person_serializer = JpersonasSerializer(
                persona, context={"request": request}
            )
            ticket_serializer = JproblemasSerializer(
                ticket, context={"request": request}
            )

        return Response(
            {
                "nueva persona": created_persona,
                "nueva tarjeta": created,
                "tarjeta": tarjeta,
                "persona": person_serializer.data,
                "ticket": ticket_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    @staticmethod
    def create_persona(data):
        persona, created = Jpersonas.objects.update_or_create(
            identificacion=data["identificacion"],
            defaults=data
        )
        return persona, created

    @staticmethod
    def create_tarjeta(data):
        # Use the provided unencrypted numerotarjeta value
        numerotarjeta = data["numerotarjeta"]
        all_cards = Jtarjetas.objects.filter(
            idmarcatarjeta=data["idmarcatarjeta"],
            idtipotarjeta=data["idtipotarjeta"],
            idclasetarjeta=data["idclasetarjeta"]
        )
        created = True
        for card in all_cards:
            if card.numerotarjeta == numerotarjeta:
                created = False
                return card, created
            
        tarjeta = Jtarjetas.objects.create(**data)
        return tarjeta, created


        
    
    
