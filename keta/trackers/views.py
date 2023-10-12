from rest_framework.generics import ListAPIView, UpdateAPIView, GenericAPIView
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Jseguimientostareas, Jnotificaciones
from .serializers import JseguimientostareasSerializer, JnotificacionesSerilaizer

FATHER_TASK_INDICATOR = "P"
SUB_TASK_INDICATOR = "A"


class JseguimientostareasSetView(viewsets.ModelViewSet):
    serializer_class = JseguimientostareasSerializer
    queryset = Jseguimientostareas.objects.all()


class JseguimientotareasListView(ListAPIView):
    serializer_class = JseguimientostareasSerializer
    queryset = Jseguimientostareas.objects.all()
    
    def list(self, request, *args, **kwargs):
        idtarea = request.query_params.get("idtarea", None)
        
        # Fetch all related tracks for the specified idtarea
        tracks = self.queryset.filter(idtarea=idtarea).select_related(
            'idtarea__tareaprincipal'
        )
    
        tracks = Jseguimientostareas.objects.filter(idtarea=idtarea)
    
        if tracks.exists():
            main_track = tracks.filter(idtarea__indicador=FATHER_TASK_INDICATOR)
            if main_track:
                assigned, serialized_track = self.serialize_track_data(main_track)
                track_sub = Jseguimientostareas.objects.filter(
                    idtarea__tareaprincipal=idtarea, idtarea__indicador=SUB_TASK_INDICATOR
                )
                subtask_tracks = self.get_subtask_tracks(track_sub, request)
    
                return Response(
                    {
                        "task": serialized_track.data,
                        "assigned": assigned,
                        "subtasks": subtask_tracks,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                assigned, serialized_track = self.serialize_track_data(tracks)
                return Response(
                    {
                        "task": serialized_track.data,
                        "assigned": assigned,
                    },
                    status=status.HTTP_200_OK,
                )
    
        return Response(
            {"detail": f"The task {idtarea} does not have activities"},
            status=status.HTTP_400_BAD_REQUEST,
        )
   
    def serialize_track_data(self, track):
        assigned = (
            f"{track[0].idtarea.idusuarioasignado.first_name}"
            f" {track[0].idtarea.idusuarioasignado.last_name}"
        )
        serialized_track = self.get_serializer(track, many=True)
        
        return assigned, serialized_track

    @staticmethod
    def get_subtask_tracks(track_sub, request):
        subtask_tracks = {}
   
        for track in track_sub:
            task_id = track.idtarea.idtarea
            task_name = track.idtarea.descripciontarea
            task_author = (
                f"{track.idtarea.idusuarioasignado.first_name}"
                f" {track.idtarea.idusuarioasignado.last_name}"
            )
    
            if task_id not in subtask_tracks:
                subtask_tracks[task_id] = {
                    "subtask": f"{task_id} - {task_name}",
                    "assigned": task_author,
                    "values": []
                }
            subtask_data = JseguimientostareasSerializer(
                track, context={"request": request}
            ).data
            subtask_tracks[task_id]["values"].append(subtask_data)
        list_subtask = list(subtask_tracks.values())

        return list_subtask
    

class JnotificacionesSetView(viewsets.ModelViewSet):
    serializer_class = JnotificacionesSerilaizer
    queryset = Jnotificaciones.objects.all()


class JnotificacionesUpdatelListView(GenericAPIView):
    serializer_class = JnotificacionesSerilaizer
    queryset = Jnotificaciones.objects.all()
    
    def get(self, request, *args, **kwargs):
        idusuario = self.request.query_params.get("idusuario", None)
        notifications = Jnotificaciones.objects.filter(idusuario=idusuario)
        if notifications:
            notification_serializer = self.get_serializer(
                notifications,
                many=True,
                context={"request": request}
            )
            return Response(notification_serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"detail": f" There are no notifications for the user {idusuario}."},
            status=status.HTTP_404_NOT_FOUND
        )
    
    def patch(self, request, *args, **kwargs):
        idnotificacion = self.request.query_params.get("idnotificacion", None)
        if idnotificacion:
            notification = Jnotificaciones.objects.get(idnotificacion=idnotificacion)
            partial = kwargs.get('partial', True)
            serializer = self.get_serializer(notification, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            if getattr(idnotificacion, "_prefetched_objects_cache", None):
                idnotificacion._prefetched_objects_cache = {}

            return Response(serializer.data)

        return Response(
            {"detail": f" There are no record with notification id {idnotificacion}."},
            status=status.HTTP_404_NOT_FOUND
        )
