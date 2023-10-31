from rest_framework import serializers

from users.serializers import model_serializers

from .models import Jseguimientostareas, Jnotificaciones



@model_serializers(Jseguimientostareas)
class JseguimientostareasSerializer(serializers.HyperlinkedModelSerializer):
    pass


@model_serializers(Jnotificaciones)
class JnotificacionesSerilaizer(serializers.HyperlinkedModelSerializer):
    pass
