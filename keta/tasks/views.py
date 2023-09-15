import re
from collections import OrderedDict

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import F
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.exceptions import APIException
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from tickets.models import Jproblemas
from .serializers import (
    JtareasticketSerializer,
    JestadotareasSerializer,
    JestadosSerializer,
    EmailNotificationSerializer,
    VtareaestadocolorSerializer,
    VtareasSerializer,
)
from .models import (
    Jtareasticket,
    Jestadotareas,
    Jestados,
    Vtareaestadocolor,
    Vtareas,
)


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

        is_father, ticket = self.validate_task_data(task_data)

        priority = ticket.idprioridad
        optimal_time, max_days_resolution = self.get_time_priority(priority)
        task_data["idprioridad"] = priority
        task_data["fechaentrega"] = timezone.now() + timezone.timedelta(
            days=int(optimal_time)
        )

        # task_data["archivo"] = task_data.get("archivo", []) + ticket.archivo

        try:
            with transaction.atomic():
                task = Jtareasticket.objects.create(**task_data)
                if is_father:
                    Jtareasticket.objects.filter(pk=task.pk).update(
                        tareaprincipal=F("pk")
                    )
                    Jproblemas.objects.filter(pk=ticket.pk).update(status=False)
        except ValidationError as e:
            return Response({"detail": e}, status=status.HTTP_403_FORBIDDEN)

        task_resp = JtareasticketSerializer(task, context={"request": request})

        return Response(task_resp.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def validate_task_data(task_data):
        check_indicator = task_data.get("indicador")
        
        if check_indicator == "P":
            ticket = task_data.get("idproblema")
            if not ticket:
                raise APIException(
                    detail="Missing idproblema",
                )
            if not ticket.status:
                raise APIException(
                    detail=f"A main task with the ticket index {ticket.idproblema} already exits",
                )
            return True, ticket

        elif check_indicator == "A":
            ticket = task_data.get("tareaprincipal")
            if not ticket:
                raise APIException(
                    detail="Missing tareaprincipal",
                )
            return False, ticket

        else:
            raise APIException(
                detail="Invalid indicador",
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
    serializer_class = JestadotareasSerializer

    def create(self, request, *args, **kwargs):
        state_serializer = JestadotareasSerializer(
            data=request.data, context={"request": request}
        )
        state_serializer.is_valid(raise_exception=True)

        task = state_serializer.validated_data.get("idtarea")
        fechaasignacion = task.fechaasignacion

        if task.indicador != "P":
            return Response(
                {"detail": "The ticket must be Parent"},
                status=status.HTTP_400_BAD_REQUEST)

        elif state_serializer.validated_data.get("tiemporequerido"):
            fechaentrega = state_serializer.validated_data["tiemporequerido"]
            state_serializer.validated_data["tiempooptimo"] = task.fechaentrega
        else:
            state_serializer.validated_data["tiempooptimo"] = fechaentrega = task.fechaentrega
        try:
            delta_time = (fechaentrega - fechaasignacion) / 3
        except TypeError:
            return Response({"detail": "The ticket is missing the date of fechaentrega"}, status=status.HTTP_400_BAD_REQUEST)

        prev_tiempoentrega = fechaasignacion
        created_objects = []

        for colour in ["green", "yellow", "red"]:
            state_colour = state_serializer.validated_data
            state_colour["color"] = colour
            state_colour["tiempoiniciocolor"] = prev_tiempoentrega
            state_colour["tiempocolor"] = prev_tiempoentrega + delta_time
            prev_tiempoentrega = state_colour["tiempocolor"]

            obj, create_new = Jestadotareas.objects.update_or_create(
                color=state_colour.get("color"),
                idtarea=state_colour.get("idtarea"),
                defaults=state_colour,
            )
            created_objects.append(obj)
            serialized_objects = JestadotareasSerializer(
                created_objects, many=True, context={"request": request}
            )
        return Response(
            {"new_colors": f"{create_new}", "colours": serialized_objects.data},
            status=status.HTTP_200_OK,
        )


class JestadosViewSet(viewsets.ModelViewSet):
    queryset = Jestados.objects.all()
    serializer_class = JestadosSerializer


class FilteredTaskView(ListAPIView):
    queryset = Jtareasticket.objects.all()
    serializer_class = JtareasticketSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["idusuarioasignado__idusuario", "idestado__idestado", "indicador"]


class VtareaestadocolorListView(ListAPIView):
    queryset = Vtareaestadocolor.objects.all()
    serializer_class = VtareaestadocolorSerializer

    def list(self, request, *args, **kwargs):
        idtarea = self.request.query_params.get("idtarea", None)
        id_asignado = self.request.query_params.get("id_asignado", None)

        queryset_main_task = Vtareaestadocolor.objects.all()

        if idtarea is not None:
            queryset_main_task = queryset_main_task.filter(idtarea=idtarea, now_state=True)

        if id_asignado is not None:
            queryset_main_task = queryset_main_task.filter(id_asignado=id_asignado, now_state=True)

        if not queryset_main_task.exists():
            return Response(
                {
                    "detail": "The task "
                              + f"The task {idtarea} or the user {id_asignado}"
                              + " was not found in the records"
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer_main = self.get_serializer(queryset_main_task, many=True)

        tarea_ids = {item["tarea"] for item in serializer_main.data}

        subtasks_dict = {}
        if tarea_ids:
            queryset_subtasks = Vtareas.objects.filter(
                tareaprincipal__in=tarea_ids, indicador="A"
            )
            for subtask in queryset_subtasks:
                tarea_id = subtask.tareaprincipal
                if tarea_id not in subtasks_dict:
                    subtasks_dict[tarea_id] = []
                subtasks_dict[tarea_id].append(
                    OrderedDict(
                        VtareasSerializer(subtask, context={"request": request}).data
                    )
                )

        for index, queryset in enumerate(serializer_main.data):
            tarea_id = queryset.get("tarea")
            serializer_main.data[index]["subtasks"] = subtasks_dict.get(tarea_id, [])

        result = serializer_main.data
        return Response(result, status=status.HTTP_200_OK)


class VtareasListView(ListAPIView):
    queryset = Vtareas.objects.all()
    serializer_class = VtareasSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["tarea", "indicador"]


class EmailNotificationView(APIView):
    def post(self, request, format=None):
        serializer = EmailNotificationSerializer(data=request.data)
        if serializer.is_valid():
            subject = serializer.validated_data["subject"]
            message = serializer.validated_data["message"]
            recipient = serializer.validated_data["recipient"]

            # Send the email
            send_mail(subject, message, "example@mail.com", recipient)

            return Response(
                {"message": "Email notification sent."}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
