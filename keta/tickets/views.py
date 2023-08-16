import sys

from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *


class BaseListView(ListAPIView):
    queryset = None
    serializer_class = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        model_name = self.__class__.__name__[
            :-8
        ]  # Remove "ListView" from the class name
        model = apps.get_model("tickets", model_name)
        self.queryset = model.objects.all()
        serializer_name = f"{model_name}Serializer"
        serializer_class = getattr(sys.modules[__name__], serializer_name)
        self.serializer_class = serializer_class


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
class JproblemasViewSet(viewsets.ModelViewSet):
    queryset = Jproblemas.objects.all()
    serializer_class = JproblemasSerializer
    # def post(self, request):
    #     serializer = personaticketsSerializer(data=request.data, context={"request": request})
    #     serializer.is_valid(raise_exception=True)
    #     data_persona = serializer.validated_data.get("persona", {})
    #     data_ticket = serializer.validated_data.get("ticket", {})
    #
    #     # Fields in a ticket that help to control not create repeated tickets
    #     tipo_ticket = data_ticket.get("idtipoticket")
    #     canal_recepcion = data_ticket.get("idcanalrecepcion")
    #
    #     with transaction.atomic():
    #         # Create or retrieve the persona instance
    #         identificacion = data_persona.get("identificacion")
    #         existing_persona, created = Jpersonas.objects.get_or_create(
    #             identificacion=identificacion,
    #             defaults={"idpersona": None, **data_persona}
    #         )
    #
    #         # If persona was just created or retrieved, update data_ticket
    #         if created:
    #             data_ticket["idpersona"] = existing_persona
    #             data_ticket["fechacreacion"] = timezone.now()
    #
    #             # Check if a similar ticket already exists
    #             similar_tickets_exist = Jproblemas.objects.filter(
    #                 idpersona=existing_persona,
    #                 idtipoticket=tipo_ticket,
    #                 idcanalrecepcion=canal_recepcion
    #             ).exists()
    #
    #             if similar_tickets_exist:
    #                 return Response(
    #                     {"detail": f"The ticket already exists"},
    #                     status=status.HTTP_208_ALREADY_REPORTED
    #                 )
    #
    #             # Create the ticket
    #             Jproblemas.objects.create(**data_ticket)
    #
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    #
    # def get(self, request):
    #     jproblemas = Jproblemas.objects.all()
    #     serializer = JproblemasSerializer(jproblemas, many=True, context={'request': request})
    #     return Response(serializer.data, status=status.HTTP_200_OK)
