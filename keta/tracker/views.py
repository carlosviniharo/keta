from collections import OrderedDict

from rest_framework.generics import ListAPIView
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Jseguimientostareas
from .serializers import JseguimientostareasSerializer

from tasks.models import Jtareasticket

FATHER_TASK_INDICATOR = "P"
SUB_TASK_INDICATOR = "A"


class JseguimientostareasSetView(viewsets.ModelViewSet):
    serializer_class = JseguimientostareasSerializer
    queryset = Jseguimientostareas.objects.all()


class JseguimientotareasListView(ListAPIView):
    serializer_class = JseguimientostareasSerializer
    queryset = Jseguimientostareas.objects.all()
    
    def list(self, request, *args, **kwargs):
        idtarea = self.request.query_params.get("idtarea", None)

        main_track = Jseguimientostareas.objects.filter(
            idtarea=idtarea,
            idtarea__indicador=FATHER_TASK_INDICATOR,
        )
        if main_track:
            serialized_track = self.get_serializer(main_track, many=True)
            
            track_sub = Jseguimientostareas.objects.filter(
                idtarea__tareaprincipal=idtarea,
                idtarea__indicador=SUB_TASK_INDICATOR)
            
            subtask_tracks = self.get_subtask_tracks(track_sub, request)

            return Response(
                {
                    "task": serialized_track.data,
                    "subtasks": subtask_tracks,
                },
                status=status.HTTP_200_OK
            )
        
        else:
            main_track = Jseguimientostareas.objects.filter(idtarea=idtarea)
            serialized_track = self.get_serializer(main_track, many=True)
            
            return Response(serialized_track.data, status=status.HTTP_200_OK)
        
    @staticmethod
    def get_subtask_tracks(track_sub, request):
        subtask_tracks = {}
        
        for task in track_sub:
            tarea_id = task.idtarea.idtarea
            if tarea_id not in subtask_tracks:
                subtask_tracks[tarea_id] = []
            
            subtask_tracks[tarea_id].append(
                OrderedDict(
                    JseguimientostareasSerializer(
                        task,
                        context={"request": request}
                    ).data
                )
            )
        return subtask_tracks
