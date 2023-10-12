from rest_framework import serializers

from .models import Jseguimientostareas, Jnotificaciones
from users.serializers import model_serializers


@model_serializers(Jseguimientostareas)
class JseguimientostareasSerializer(serializers.HyperlinkedModelSerializer):
    pass


@model_serializers(Jnotificaciones)
class JnotificacionesSerilaizer(serializers.HyperlinkedModelSerializer):
    pass
