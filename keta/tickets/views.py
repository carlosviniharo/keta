from django.db import transaction
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *


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


# TODO: The valitadion if there is not repeated tickets should be improved
#  as for now it only invalidated tickets that have the same user, tipo ticket
#  and canal de recepcion.
# class JproblemasViewSet(viewsets.ModelViewSet):
#     queryset = Jproblemas.objects.all()
#     serializer_class = JproblemasSerializer
#
#     def create(self, request, *args, **kwargs):
#         personas_serializer = JpersonasSerializer(data=request.data.get('persona'))
#         problemas_serializer = self.get_serializer(data=request.data.get('ticket'))
#
#         if personas_serializer.is_valid() and problemas_serializer.is_valid():
#             # Save the persona record
#             persona_instance = personas_serializer.save()
#
#             # Associate the persona with the ticket and save the ticket record
#             ticket_data = problemas_serializer.validated_data
#             ticket_data['idpersona'] = persona_instance.idpersona # Set the foreign key
#             ticket_instance = Jproblemas.objects.create(**ticket_data)
#
#             return Response(
#                 {
#                     'persona': personas_serializer.data,
#                     'ticket': problemas_serializer.data
#                 },
#                 status=status.HTTP_201_CREATED
#             )
#
#         return Response(
#             {
#                 'errors': {
#                     'persona': personas_serializer.errors,
#                     'ticket': problemas_serializer.errors
#                 }
#             },
#             status=status.HTTP_400_BAD_REQUEST
#         )

class JproblemasCreateView(APIView):
    def post(self, request):
        personas_serializer = JpersonasSerializer(data=request.data.get("persona"))
        problemas_serializer = JproblemasSerializer(data=request.data.get('ticket'))
        if personas_serializer.is_valid() and problemas_serializer.is_valid():
            data_ticket = problemas_serializer.validated_data
            data_persona = personas_serializer.validated_data
        # Fields in a ticket that help to control not create repeated tickets
            tipo_ticket = data_ticket.get("idtipoticket")
            canal_recepcion = data_ticket.get("idcanalrecepcion")

            with transaction.atomic():
                # Create or retrieve the persona instance
                identificacion = data_persona.get("identificacion")
                existing_persona, created = Jpersonas.objects.get_or_create(
                    identificacion=identificacion,
                    defaults={"idpersona": None, **data_persona}
                )
                # If persona was just created or retrieved, update data_ticket
                data_ticket["idpersona"] = existing_persona
                data_ticket["fechacreacion"] = timezone.now()

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
                Jproblemas.objects.create(**data_ticket)

            return Response(
                {
                    'persona': personas_serializer.data,
                    'ticket': problemas_serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'errors': {
                    'persona': personas_serializer.errors,
                    'ticket': problemas_serializer.errors
                }
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request):
        jproblemas = Jproblemas.objects.all()
        serializer = JproblemasSerializer(jproblemas, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
