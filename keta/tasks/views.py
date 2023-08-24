import re

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response

from .serializers import JtareasticketSerializer, JestadotareasSerializers, JestadosSerializer
from .models import Jtareasticket, Jestadotareas, Jestados


# TODO The class only handles parent tasks please include support tasks.
class JtareasticketViewSet(viewsets.ModelViewSet):
    queryset = Jtareasticket.objects.all()
    serializer_class = JtareasticketSerializer

    def create(self, request, *args, **kwargs):
        task_serializer = JtareasticketSerializer(
            data=request.data, context={"request": request}
        )
        task_serializer.is_valid(raise_exception=True)
        # Check if the problem is Parent
        check_indicator = task_serializer.validated_data["indicador"]
        ticket = task_serializer.validated_data["idproblema"]

        if check_indicator == "P":
            existing_task = Jtareasticket.objects.filter(idproblema=ticket).first()
            if existing_task:
                return Response(
                    {"error": "A task for this ticket already exists, "
                              f"the task ID is {existing_task.idtarea}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            priority = ticket.idprioridad
            max_days_resolution = int(self.get_time_priority(priority)[1])
            # TODO : check the type for the archivo as this  must be a list
            if task_serializer.validated_data.get("archivo", ""):
                task_serializer.validated_data["archivo"] += ticket.archivo
            else:
                task_serializer.validated_data["archivo"] = ticket.archivo

            task_serializer.validated_data["idprioridad"] = priority
            task_serializer.validated_data[
                "fechaentrega"
            ] = timezone.now() + timezone.timedelta(days=max_days_resolution)

            task = Jtareasticket.objects.create(**task_serializer.validated_data)
            task.tareaprincipal = task

            task_resp = JtareasticketSerializer(task, context={"request": request})

            return Response(task_resp.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"error": "Include indicator value"}, status=status.HTTP_400_BAD_REQUEST
            )

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
