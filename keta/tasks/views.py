import re
from collections import OrderedDict

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import transaction, IntegrityError
from django.db.models import F
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.exceptions import APIException
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from tickets.models import Jproblemas
from trackers.utils.helper import create_notification, create_notification_new_claim
from resolvers.utils.helper import send_email
from reports.utils.helper import format_date

from .utils.helper import create_excel_file
from .serializers import (
    JtareasticketSerializer,
    JestadotareasSerializer,
    JestadosSerializer,
    VtareaestadocolorSerializer,
    VtareasSerializer,
    JarchivosSerializer,
    JarchivoListSerializer,
    VtareasemailSerializer,
    VtareasrechazadasSerializer,
)
from .models import (
    Jarchivos,
    Jtareasticket,
    Jestadotareas,
    Jestados,
    Vtareaestadocolor,
    Vtareas,
    Vtareasemail, Vtareasrechazadas,
)
from .utils import helper


FATHER_TASK_INDICATOR = "P"
SUB_TASK_INDICATOR = "A"
DATE_FORMAT = "%d-%m-%Y"


# TODO the store of archivos should be switched to a cloud as the files can grown with time.
class JarchivosViewSet(viewsets.ModelViewSet):
    queryset = Jarchivos.objects.all()
    serializer_class = JarchivosSerializer


class JarchivosCreateView(CreateAPIView):
    queryset = Jarchivos.objects.all()
    serializer_class = JarchivosSerializer
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        file_serializer = JarchivosSerializer(
            data=request.data, context={"request": request}
        )
        file_serializer.is_valid(raise_exception=True)
        file = file_serializer.validated_data
        pdf_file = request.FILES.get("pdf_file")
        if pdf_file:
            base64_encoded_string = helper.convert_pdf_to_b64(pdf_file)
        else:
            return Response(
                {"detail": "No pdf file was provided or provided a corrupted one"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create a ContentFile from the binary data
        file["contenidoarchivo"] = base64_encoded_string

        task = file["idtarea"]
        if task.indicador == SUB_TASK_INDICATOR:
            file["idtarea"] = task.tareaprincipal

        try:
            with transaction.atomic():
                file_saved = Jarchivos.objects.create(**file)
        except IntegrityError:
            return Response(
                {
                    "detail": f"The file with the name '{file['nombrearchivo']}' already exists in this ticket"
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        file_resp = JarchivosSerializer(file_saved, context={"request": request})
        return Response(file_resp.data, status=status.HTTP_201_CREATED)


class JarchivosListView(ListAPIView):
    queryset = Jarchivos.objects.all()
    serializer_class = JarchivoListSerializer
    
    def list(self, request, *args, **kwargs):
        idtask = self.request.query_params.get("idtarea", None)
        is_ticket = Jtareasticket.objects.get(idtarea=idtask)
        
        if is_ticket.indicador == "P":
            queryset = Jarchivos.objects.only(
                "idarchivo",
                "idsubtarea",
                "idtarea",
                "nombrearchivo",
                "fechacarga",
                "fecharegistro",
                "descripcionarchivo",
                "mimetypearchivo",
            ).filter(idtarea=idtask)
        else:
            queryset = Jarchivos.objects.only(
                "idarchivo",
                "idsubtarea",
                "idtarea",
                "nombrearchivo",
                "fechacarga",
                "fecharegistro",
                "descripcionarchivo",
                "mimetypearchivo",
            ).filter(idsubtarea=idtask)
        
        if not queryset:
            raise APIException(f"There is not any file for task {idtask}")
        
        archivo_data = JarchivoListSerializer(queryset, many=True, context={"request": request})
        return Response(archivo_data.data, status=status.HTTP_201_CREATED)


class JarchivoRetrieveView(RetrieveAPIView):
    queryset = Jarchivos.objects.all()
    serializer_class = JarchivosSerializer
    
    def retrieve(self, request, *args, **kwargs):
        archivo = self.get_object()
        pdf_string = archivo.contenidoarchivo
        pdf_name = archivo.nombrearchivo
        pdf_mimetype = archivo.mimetypearchivo
        response = helper.convert_base64_to_pdf(pdf_string, pdf_name, pdf_mimetype)
        return response
    
    
# TODO Implement pagination as the number of registers in this model can grown rapidly.
class JtareasticketViewSet(viewsets.ModelViewSet):
    queryset = Jtareasticket.objects.all()
    serializer_class = JtareasticketSerializer

    def create(self, request, *args, **kwargs):

        subtareatime = request.data.get("subtareatime")

        task_serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        task_serializer.is_valid(raise_exception=True)
        task_data = task_serializer.validated_data

        is_father, ticket = self.validate_task_data(task_data)

        object_priority = ticket.idprioridad
        task_data["idprioridad"] = object_priority

        try:
            with transaction.atomic():
                
                if is_father:
                    create_date = timezone.now()
                    optimal_time, max_days_resolution = self.get_time_priority(object_priority)
                    optimal_date, extended_date = helper.calculate_weekends(create_date, optimal_time,
                                                                            max_days_resolution)
                    task_data["fechaentrega"] = optimal_date
                    task_data["fechaextension"] = extended_date
                    task = Jtareasticket.objects.create(**task_data)
                    Jtareasticket.objects.filter(pk=task.pk).update(
                        tareaprincipal=F("pk")
                    )
                    Jproblemas.objects.filter(pk=ticket.pk).update(status=False)
                    task_resp = JtareasticketSerializer(task, context={"request": request})

                    # Giving format to the data and sending the email after create a claim
                    tarea_email = Vtareasemail.objects.get(idtarea=task_resp.data.get("idtarea"))
                    tarea_email = VtareasemailSerializer(tarea_email)
                    tarea_email_data = tarea_email.data

                    if not tarea_email_data["date"]:
                        raise APIException("There is not date in the view for the email.")

                    tarea_email_data["date"] = format_date(tarea_email_data["date"])
                    try:
                        send_email(tarea_email_data, "create_ticket_email")
                    except Exception as e:
                        raise APIException(f"The following error occurred, {e}")

                    create_notification_new_claim(task_resp, request)
                else:
                    fechaentrega_subtarea = task_data["tareaprincipal"].fechaentrega - timezone.timedelta(days=1)

                    if fechaentrega_subtarea.weekday() > 4:
                        fechaentrega_subtarea += timezone.timedelta(7 - fechaentrega_subtarea.weekday())

                    task_data["fechaentrega"] = fechaentrega_subtarea

                    if subtareatime:
                        task_data["fechaentrega"] = subtareatime

                    task = Jtareasticket.objects.create(**task_data)
                    task_resp = JtareasticketSerializer(task, context={"request": request})

                    # Giving format to the data and sending the email after create a claim
                    tarea_email = Vtareas.objects.get(tarea=task_resp.data.get("idtarea"))

                    try:
                        send_email(tarea_email, "ticket_data_assigment")
                    except Exception as e:
                        raise APIException(f"The following error occurred, {e}")
                    
        except ValidationError as exc:
            return Response({"detail": exc}, status=status.HTTP_403_FORBIDDEN)

        return Response(task_resp.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        data_task = request.data
        update_assignment = int(data_task.get("idestado").split('/')[-2])
        indicator = instance.indicador
        object_priority = instance.idprioridad

        if update_assignment == 3 and indicator == FATHER_TASK_INDICATOR:
            create_date = timezone.now()
            optimal_time, max_days_resolution = self.get_time_priority(object_priority)
            optimal_date, extended_date = helper.calculate_weekends(create_date, optimal_time, max_days_resolution)
            data_task["fechaentrega"] = optimal_date
            data_task["fechaextension"] = extended_date

        serializer = self.get_serializer(instance, data=data_task, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        create_notification(serializer, request)

        return Response(serializer.data)

    @staticmethod
    def validate_task_data(task_data):
        check_indicator = task_data.get("indicador")

        if check_indicator == FATHER_TASK_INDICATOR:
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

        if check_indicator == SUB_TASK_INDICATOR:
            ticket = task_data.get("tareaprincipal")
            if not ticket:
                raise APIException(
                    detail="Missing tareaprincipal",
                )
            return False, ticket
        raise APIException("Invalid indicator")
    

    @staticmethod
    def get_time_priority(priority):
        try:
            time_values = re.findall(r"\d+", priority.duracionprioridad)
            if len(time_values) == 2:
                optimal_time = int(time_values[0]) - 1
                deadline = int(time_values[1]) - 1
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
        # Create a state serializer instance and validate data
        state_serializer = JestadotareasSerializer(
            data=request.data, context={"request": request}
        )
        state_serializer.is_valid(raise_exception=True)
        state = state_serializer.validated_data

        # Extract task  from validated data
        task = state.get("idtarea")

        # Check if the task is a parent task
        if task.indicador != FATHER_TASK_INDICATOR:
            return Response(
                {"detail": "The ticket must be Parent"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Setting the tiempo optimo to fecha de entrega
        fechaasignacion = task.fechaasignacion
        fechaentrega = state["tiempooptimo"] = task.fechaentrega

        if state.get("tiemporequerido"):
            fechaentrega = state["tiemporequerido"]

        try:
            delta_time = (fechaentrega - fechaasignacion) / 3
        except TypeError:
            return Response(
                {"detail": "The ticket is missing the date of fechaentrega"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Create states for "green," "yellow," and "red" colors
        create_new, created_objects = self._create_color_states(
            state, delta_time, fechaasignacion
        )

        # Serialize and return the created objects
        serialized_objects = JestadotareasSerializer(
            created_objects, many=True, context={"request": request}
        )
        return Response(
            {"new_colors": f"{create_new}", "colours": serialized_objects.data},
            status=status.HTTP_200_OK,
        )

    @staticmethod
    def _create_color_states(state, delta_time, fechaasignacion):
        prev_tiempoentrega = fechaasignacion
        indefinite_time = timezone.datetime(9999, 12, 31)
        created_objects = []

        for colour in ["green", "yellow", "red", "grey"]:
            state_colour = state.copy()
            state_colour["color"] = colour
            state_colour["tiempoiniciocolor"] = prev_tiempoentrega
            if colour == "grey":
                state_colour["tiempocolor"] = indefinite_time
            else:
                state_colour["tiempocolor"] = prev_tiempoentrega + delta_time
                prev_tiempoentrega = state_colour["tiempocolor"]

            obj, create_new = Jestadotareas.objects.update_or_create(
                color=state_colour.get("color"),
                idtarea=state_colour.get("idtarea"),
                defaults=state_colour,
            )
            created_objects.append(obj)

        return create_new, created_objects


class JestadosViewSet(viewsets.ModelViewSet):
    queryset = Jestados.objects.all()
    serializer_class = JestadosSerializer


class FilteredTaskView(ListAPIView):
    queryset = Jtareasticket.objects.all()
    serializer_class = JtareasticketSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "idusuarioasignado__idusuario",
        "idestado__idestado",
        "indicador",
    ]


class VtaskListView(ListAPIView):
    queryset = Vtareas.objects.all()
    serializer_class = VtareasSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "tarea",
        "cedula",
        "sucursal",
        "tipo_reclamo",
        "tipo_comentario",
        "fechaentrega",
        "prioridad",
        "estado",
    ]

    def get_queryset(self):
        queryset = Vtareas.objects.all()

        # Apply any filters specified in the request
        queryset = self.filter_queryset(queryset)

        # Apply custom date range filtering
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            start_date = timezone.datetime.strptime(start_date, DATE_FORMAT)
            end_date = timezone.datetime.strptime(end_date, DATE_FORMAT) + timezone.timedelta(hours=23, minutes=59)
            queryset = queryset.filter(fecha_asignacion__range=(start_date, end_date))
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class GenerateExcelView(VtaskListView):

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = queryset.filter(indicador=FATHER_TASK_INDICATOR)
        serializer = self.get_serializer(queryset, many=True)
        response = create_excel_file(serializer.data)
        return response


# Endpoints for the database views.
class VtareaestadocolorListView(ListAPIView):
    queryset = Vtareaestadocolor.objects.all()
    serializer_class = VtareaestadocolorSerializer

    def list(self, request, *args, **kwargs):
        idtarea = self.request.query_params.get("idtarea", None)
        id_asignado = self.request.query_params.get("id_asignado", None)

        queryset_main_task = Vtareaestadocolor.objects.filter(now_state=True)

        if idtarea is not None:
            queryset_main_task = queryset_main_task.filter(
                idtarea=idtarea
            )

        if id_asignado is not None:
            queryset_main_task = queryset_main_task.filter(
                id_asignado=id_asignado
            )

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
                tareaprincipal__in=tarea_ids, indicador=SUB_TASK_INDICATOR
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
    filterset_fields = ["tarea", "indicador", "estado", "idcreador", "sucursal", "idtecnico"]


class VtareasrechazadasListView(ListAPIView):
    queryset = Vtareasrechazadas.objects.all()
    serializer_class = VtareasrechazadasSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["idasignador"]

# class EmailNotificationView(APIView):
#     def post(self, request, format=None):
#         serializer = EmailNotificationSerializer(data=request.data)
#         if serializer.is_valid():
#             subject = serializer.validated_data["subject"]
#             message = serializer.validated_data["message"]
#             recipient = serializer.validated_data["recipient"]
#
#             # Send the email
#             send_mail(subject, message, "example@mail.com", recipient)
#
#             return Response(
#                 {"message": "Email notification sent."}, status=status.HTTP_200_OK
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
