from rest_framework import serializers

from .models import Jseguimientostareas
from users.serializers import model_serializers


@model_serializers(Jseguimientostareas)
class JseguimientostareasSerializer(serializers.HyperlinkedModelSerializer):
    pass
