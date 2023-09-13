from rest_framework import serializers

from users.serializers import model_serializers
from .models import (
    Jtareasticket,
    Jestadotareas,
    Jestados,
    Vtareaestadocolor,
    Vtareas,
)


@model_serializers(Jestadotareas)
class JestadotareasSerializer(serializers.HyperlinkedModelSerializer):
    pass


@model_serializers(Jestados)
class JestadosSerializer(serializers.HyperlinkedModelSerializer):
    pass


@model_serializers(Jtareasticket)
class JtareasticketSerializer(serializers.HyperlinkedModelSerializer):
    pass


# As the model is not managed by Django it can not be implemented Hyperlinked ModelSerializers
class VtareaestadocolorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vtareaestadocolor
        fields = "__all__"


class VtareasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vtareas
        fields = "__all__"


class EmailNotificationSerializer(serializers.Serializer):
    subject = serializers.CharField()
    message = serializers.CharField()
    recipient = serializers.ListField(child=serializers.EmailField())
