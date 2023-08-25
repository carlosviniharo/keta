import re

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response

from .serializers import JtareasticketSerializer, JestadotareasSerializers, JestadosSerializer
from .models import Jtareasticket, Jestadotareas, Jestados


# TODO Fix how the files should be appended. They should go to main Task.
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
        # Check if the problem is Parent
        check_indicator = task_data['indicador']
        if check_indicator == "P":
            ticket = task_data['idproblema']
        elif check_indicator == "A":
            main_task = task_data['tareaprincipal']
            ticket = main_task.idproblema
            is_father = False

        priority = ticket.idprioridad
        max_days_resolution = int(self.get_time_priority(priority)[1])
        task_data["idprioridad"] = priority
        task_data["fechaentrega"] = timezone.now() + timezone.timedelta(days=max_days_resolution)

        # TODO : check the type for the archivo as this  must be a list
        if task_data.get("archivo", ""):
            task_data["archivo"] += ticket.archivo
        else:
            task_data["archivo"] = ticket.archivo

        try:
            task = Jtareasticket.objects.create(**task_data)
        except ValidationError as e:
            return Response({"detail": e}, status=status.HTTP_403_FORBIDDEN)

        task.tareaprincipal = task

        if not is_father:
            task.tareaprincipal = main_task

        task.save()
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
