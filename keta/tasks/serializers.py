from rest_framework import serializers
from users.serializers import model_serializers
from .models import *


class JtareasticketSerializer(serializers.HyperlinkedModelSerializer):
    archivo = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = Jtareasticket
        fields = tuple(f.name for f in Jtareasticket._meta.fields) + ("url",)


@model_serializers(Jestadotareas)
class JestadotareasSerializers(serializers.HyperlinkedModelSerializer):
    pass


@model_serializers(Jestados)
class JestadosSerializer(serializers.HyperlinkedModelSerializer):
    pass
