from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .serializers import *
from users.serializers import *


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
class JpersonasListView(viewsets.ModelViewSet):
    queryset = Jpersonas.objects.all()
    serializer_class = JpersonasSerializer
    lookup_field = "identificacion"


class JtiposproductosJconceptosListView(ListAPIView):
    serializer_class = JconceptosSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.idtipoproducto = None

    def get_queryset(self):
        self.idtipoproducto = self.kwargs.get("idtipoproducto")
        return Jconceptos.objects.filter(idtipoproducto=self.idtipoproducto)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

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


# TODO: The valitadion if there is not repeated tickets should be improved
#  as for now it only invalidated tickets that have the same user, tipo ticket
#  and canal de recepcion.Also, include the number of ticket that is repeating.


class JproblemasViewSet(viewsets.ModelViewSet):
    queryset = Jproblemas.objects.all()
    serializer_class = JproblemasSerializer

    def create(self, request):
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
        canal_recepcion = problemas_serializer.validated_data["idcanalrecepcion"]
        monto = problemas_serializer.validated_data["monto"]
        idtipocomentario = problemas_serializer.validated_data["idtipocomentario"]

        data_ticket = problemas_serializer.validated_data

        if tipo_ticket.idtipoticket == 2:
            try:
                tarjeta_serializer.is_valid(raise_exception=True)
            except serializers.ValidationError:
                custom_response = {
                    "Validation failed:": "Ticket type 'Reclamos Tarjetas',  "
                                          "please include tarjeta in the request"
                }
                raise ValidationError(custom_response)

            tarjeta, created_tarjeta = self.create_tarjeta(
                tarjeta_serializer.validated_data
            )
            data_ticket["idtarjeta"] = tarjeta
        else:
            print("Please make sure you are sending the right tipoticket")
            created_tarjeta = False

        with transaction.atomic():
            persona, created_persona = self.create_persona(
                personas_serializer.validated_data
            )

            similar_tickets_exist = self.queryset.filter(
                idpersona=persona,
                idtipoticket=tipo_ticket,
                idcanalrecepcion=canal_recepcion,
                monto=monto,
                idtipocomentario=idtipocomentario,
            )

            if similar_tickets_exist.exists():
                return Response(
                    {"detail": f"The ticket already exists and the "
                               f"number of this ticket is {similar_tickets_exist[0].numeroticket}"},
                    status=status.HTTP_208_ALREADY_REPORTED,
                )

            ticket = self.create_ticket(persona, data_ticket)
            person_serializer = JpersonasSerializer(
                persona, context={"request": request}
            )
            ticket_serializer = JproblemasSerializer(
                ticket, context={"request": request}
            )

        return Response(
            {
                "nueva persona": f"{created_persona}",
                "tarjeta": f"{created_tarjeta}",
                "persona": person_serializer.data,
                "ticket": ticket_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    def create_persona(self, data):
        persona, created = Jpersonas.objects.get_or_create(
            identificacion=data["identificacion"], defaults={"idpersona": None, **data}
        )
        if not created:
            for attr, value in data.items():
                setattr(persona, attr, value)
            persona.save()
        return persona, created

    def create_tarjeta(self, data):
        tarjeta, created = Jtarjetas.objects.get_or_create(
            idmarcatarjeta=data["idmarcatarjeta"],
            idtipotarjeta=data["idtipotarjeta"],
            idclasetarjeta=data["idclasetarjeta"],
            defaults=data,
        )
        return tarjeta, created

    def create_ticket(self, persona, data_ticket):
        ticket = Jproblemas.objects.create(idpersona=persona, **data_ticket)
        return ticket
