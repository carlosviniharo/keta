import re

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import transaction
from django.db.models import F
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from tickets.models import Jproblemas
from .serializers import JtareasticketSerializer, JestadotareasSerializers, JestadosSerializer
from .models import Jtareasticket, Jestadotareas, Jestados


# TODO Fix the field archivo as this would be a table
class JtareasticketViewSet(viewsets.ModelViewSet):
    queryset = Jtareasticket.objects.all()
    serializer_class = JtareasticketSerializer

    def create(self, request, *args, **kwargs):
        task_serializer = JtareasticketSerializer(
            data=request.data, context={"request": request}
        )
        task_serializer.is_valid(raise_exception=True)
        task_data = task_serializer.validated_data
        is_father = True
        check_indicator = task_data.get('indicador')

        if check_indicator == "P":
            ticket = task_data.get('idproblema')
            if not ticket:
                return Response({"detail": "Missing idproblema"}, status=status.HTTP_400_BAD_REQUEST)
            if not ticket.status:
                return Response(
                    {"detail": f"A main task with the ticket index {ticket.idproblema} already exits"},
                    status=status.HTTP_409_CONFLICT,
                )
        elif check_indicator == "A":
            ticket = task_data.get('tareaprincipal')
            if not ticket:
                return Response({"detail": "Missing tareaprincipal"}, status=status.HTTP_400_BAD_REQUEST)
            is_father = False

        else:
            return Response({"detail": "Invalid indicador"}, status=status.HTTP_400_BAD_REQUEST)

        priority = ticket.idprioridad
        _, max_days_resolution = self.get_time_priority(priority)
        task_data["idprioridad"] = priority
        task_data["fechaentrega"] = timezone.now() + timezone.timedelta(days=int(max_days_resolution))

        # task_data["archivo"] = task_data.get("archivo", []) + ticket.archivo

        try:
            with transaction.atomic():
                task = Jtareasticket.objects.create(**task_data)
                if is_father:
                    Jtareasticket.objects.filter(pk=task.pk).update(tareaprincipal=F("pk"))
                    Jproblemas.objects.filter(pk=ticket.pk).update(status=False)
        except ValidationError as e:
            return Response({"detail": e}, status=status.HTTP_403_FORBIDDEN)

        task_resp = JtareasticketSerializer(task, context={"request": request})
        return Response(task_resp.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def get_time_priority(priority):
        try:
            time_values = re.findall(r"\d+", priority.duracionprioridad)
            if len(time_values) == 2:
                optimal_time = time_values[0]
                deadline = time_values[1]
            else:
                raise ValueError(
                    "Not enough time values extracted from duracionprioridad"
                )
        except (ObjectDoesNotExist, ValueError):
            return None, None
        return optimal_time, deadline


class JestadotareasViewSet(viewsets.ModelViewSet):
    queryset = Jestadotareas.objects.all()
    serializer_class = JestadotareasSerializers


class JestadosViewSet(viewsets.ModelViewSet):
    queryset = Jestados.objects.all()
    serializer_class = JestadosSerializer

    def create(self, request, *args, **kwargs):
        state_serializer = JestadosSerializer(
            data=request.data,
            context={"request": request})
        state_serializer.is_valid(raise_exception=True)
        task = state_serializer.validated_data['idtarea']
        fechaasignacion = task.get("fechaasignacion")
        fechaentrega = task.get("fechaasignacion")
        delta_time = (fechaentrega - fechaasignacion) / 3
        colours = {"green": 1, "yellow": 2, "red": 3}
        for colour, factor in colours:
            state_colour = state_serializer.validated_data
            state_colour["color"] = colour
            state_colour["tiempofinal"] = fechaasignacion + (factor * delta_time)
            Jestados.objects.create(**state_colour)
        return Response(status=status.HTTP_200_OK)


class StopLightViewSet(viewsets.ModelViewSet):
    pass


class FilteredTaskView(ListAPIView):
    queryset = Jtareasticket.objects.all()
    serializer_class = JtareasticketSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['idusuarioasignado__idusuario', 'idestado__idestado']
