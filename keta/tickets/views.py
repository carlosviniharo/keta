from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response

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


class JpersonasListView(viewsets.ModelViewSet):
    queryset = Jpersonas.objects.all()
    serializer_class = JpersonasSerializer
    lookup_field = "identificacion"


# TODO: The valitadion if there is not repeated tickets should be improved
#  as for now it only invalidated tickets that have the same user, tipo ticket
#  and canal de recepcion.


class JproblemasViewSet(viewsets.ModelViewSet):
    queryset = Jproblemas.objects.all()
    serializer_class = JproblemasSerializer

    def create(self, request):
        personas_serializer = JpersonasSerializer(data=request.data.get("persona"), context={'request': request})
        tarjeta_serializer = JtarjetasSerializer(data=request.data.get('tarjeta'), context={'request': request})
        problemas_serializer = JproblemasSerializer(data=request.data.get('ticket'), context={'request': request})
        # Validating data
        personas_serializer.is_valid(raise_exception=True)
        problemas_serializer.is_valid(raise_exception=True)
        # Get field to check if it is a new ticket
        tipo_ticket = problemas_serializer.validated_data["idtipoticket"]
        canal_recepcion = problemas_serializer.validated_data["idcanalrecepcion"]
        identificacion = personas_serializer.validated_data["identificacion"]
        # Get the dictionary with the data to create the ticket
        data_ticket = problemas_serializer.validated_data
        # check if the ticket needs to a tarjeta
        if tipo_ticket == 2:
            tarjeta_serializer.is_valid(raise_exception=True)
            # Create or retrieve the Jtarjetas instance
            tarjeta, created = Jtarjetas.objects.get_or_create(
                idmarcatarjeta=tarjeta_serializer.validated_data["idmarcatarjeta"],
                idtipotarjeta=tarjeta_serializer.validated_data["idtipotarjeta"],
                idclasetarjeta=tarjeta_serializer.validated_data["idclasetarjeta"],
                defaults=tarjeta_serializer.validated_data
            )
            # Associate the ticket with the tarjeta
            data_ticket['idtarjeta'] = tarjeta

        with transaction.atomic():
            # Create or retrieve the persona instance
            existing_persona, created = Jpersonas.objects.get_or_create(
                identificacion=identificacion,
                defaults={"idpersona": None, **personas_serializer.validated_data}
            )

            # Update existing persona with new data
            if not created:
                for attr, value in personas_serializer.validated_data.items():
                    setattr(existing_persona, attr, value)
                existing_persona.save()

            # Associate ticket with persona
            data_ticket["idpersona"] = existing_persona

            # Check if a similar ticket already exists
            similar_tickets_exist = Jproblemas.objects.filter(
                idpersona=existing_persona,
                idtipoticket=tipo_ticket,
                idcanalrecepcion=canal_recepcion
            ).exists()

            if similar_tickets_exist:
                return Response(
                    {"detail": f"The ticket already exists"},
                    status=status.HTTP_208_ALREADY_REPORTED
                )

            # Create the ticket
            ticket = Jproblemas.objects.create(**data_ticket)
            person_serializer = JpersonasSerializer(existing_persona, context={"request": request})
            ticket_serializer = JproblemasSerializer(ticket, context={"request": request})

        return Response(
            {
                'Nueva persona': f'{created}',
                'persona': person_serializer.data,
                'ticket': ticket_serializer.data
            },
            status=status.HTTP_201_CREATED
        )

