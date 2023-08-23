from rest_framework import serializers
from users.serializers import model_serializers
from .models import *


@model_serializers(Jtareasticket)
class JtareasticketSerializer(serializers.HyperlinkedModelSerializer):
    pass


@model_serializers(Jestadotareas)
class JestadotareasSerializers(serializers.HyperlinkedModelSerializer):
    pass


@model_serializers(Jestados)
class JestadosSerializer(serializers.HyperlinkedModelSerializer):
    pass
