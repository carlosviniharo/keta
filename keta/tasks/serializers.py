from rest_framework import serializers

from users.serializers import model_serializers
from .models import Jtareasticket, Jestadotareas, Jestados, Vtareaestadocolor


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


# As the model is not managed by Django it can not be implemented Hyperlinked ModelSerializers
class VtareaestadocolorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vtareaestadocolor
        fields = "__all__"


class EmailNotificationSerializer(serializers.Serializer):
    subject = serializers.CharField()
    message = serializers.CharField()
    recipient = serializers.ListField(child=serializers.EmailField())
