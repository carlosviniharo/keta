from rest_framework import serializers

from users.serializers import model_serializers

from .models import Jseguimientostareas, Jnotificaciones, Vseguimientotareas


@model_serializers(Jseguimientostareas)
class JseguimientostareasSerializer(serializers.HyperlinkedModelSerializer):
    pass


@model_serializers(Jnotificaciones)
class JnotificacionesSerilaizer(serializers.HyperlinkedModelSerializer):
    pass


# Serializers for database views
class VseguimientotareasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vseguimientotareas
        fields = '__all__'
