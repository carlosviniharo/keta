from rest_framework import serializers

from users.serializers import model_serializers
from .models import (
    Jtareasticket,
    Jestadotareas,
    Jestados,
    Jarchivos,
    Vtareaestadocolor,
    Vtareas,
    Vtareasemail,
)


@model_serializers(Jarchivos)
class JarchivosSerializer(serializers.HyperlinkedModelSerializer):
    pass


@model_serializers(Jestadotareas)
class JestadotareasSerializer(serializers.HyperlinkedModelSerializer):
    pass


@model_serializers(Jestados)
class JestadosSerializer(serializers.HyperlinkedModelSerializer):
    pass


@model_serializers(Jtareasticket)
class JtareasticketSerializer(serializers.HyperlinkedModelSerializer):
    pass


# Special Serializers
# As the views cannot be managed by Django it was not implemented Hyperlinked ModelSerializers
class VtareaestadocolorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vtareaestadocolor
        fields = "__all__"


class VtareasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vtareas
        fields = "__all__"


class VtareasemailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vtareasemail
        fields = "__all__"


class JarchivoListSeriliazer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Jarchivos
        exclude = ("contenidoarchivo",)


# class EmailNotificationSerializer(serializers.Serializer):
#     subject = serializers.CharField()
#     message = serializers.CharField()
#     recipient = serializers.ListField(child=serializers.EmailField())
