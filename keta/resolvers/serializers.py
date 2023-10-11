from users.serializers import model_serializers
from rest_framework import serializers
from .models import (
    Jclasificacionesresoluciones,
    Jresoluciones,
    Jtiporesoluciones,
    Jvaloresresoluciones,
    Vresoluciones,
)


@model_serializers(Jclasificacionesresoluciones)
class JclasificacionesresolucionesSerializer(serializers.HyperlinkedModelSerializer):
    pass


@model_serializers(Jresoluciones)
class JresolucionesSerializer(serializers.HyperlinkedModelSerializer):
    pass


@model_serializers(Jtiporesoluciones)
class JtiporesolucionesSerializer(serializers.HyperlinkedModelSerializer):
    pass


@model_serializers(Jvaloresresoluciones)
class JvaloresresolucionesSerializer(serializers.HyperlinkedModelSerializer):
    pass


# Serializers for the views of the database
class VresolucionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vresoluciones
        fields = "__all__"
        
