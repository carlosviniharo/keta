from rest_framework import serializers

from users.models import Jpersonas
from users.serializers import model_serializers
from .models import (
    Jcanalesrecepciones, Jclasestarjetas, Jtiposproductos,
    Jconceptos, Jmarcastarjetas, Jprioridades, Jtipostarjetas,
    Jtarjetas, Jtiposcomentarios, Jtickettipos, Jtipostransacciones,
    Jproblemas,
)


@model_serializers(Jcanalesrecepciones)
class JcanalesrecepcionesSerializer(serializers.HyperlinkedModelSerializer):
    pass


@model_serializers(Jclasestarjetas)
class JclasestarjetasSerializer(serializers.HyperlinkedModelSerializer):
    pass


@model_serializers(Jtiposproductos)
class JtiposproductosSerializer(serializers.HyperlinkedModelSerializer):
    pass


@model_serializers(Jconceptos)
class JconceptosSerializer(serializers.HyperlinkedModelSerializer):
    pass


@model_serializers(Jmarcastarjetas)
class JmarcastarjetasSerializer(serializers.HyperlinkedModelSerializer):
    pass


@model_serializers(Jpersonas)
class JpersonasSerializer(serializers.HyperlinkedModelSerializer):
    pass

@model_serializers(Jprioridades)
class JprioridadesSerializer(serializers.HyperlinkedModelSerializer):
    pass


@model_serializers(Jtipostarjetas)
class JtipostarjetasSerializer(serializers.HyperlinkedModelSerializer):
    pass


@model_serializers(Jtarjetas)
class JtarjetasSerializer(serializers.HyperlinkedModelSerializer):
    pass


@model_serializers(Jtiposcomentarios)
class JtiposcomentariosSerializer(serializers.HyperlinkedModelSerializer):
    pass


@model_serializers(Jtickettipos)
class JtickettiposSerializer(serializers.HyperlinkedModelSerializer):
    pass


@model_serializers(Jtipostransacciones)
class JtipostransaccionesSerializer(serializers.HyperlinkedModelSerializer):
    pass


class JproblemasSerializer(serializers.HyperlinkedModelSerializer):
    archivo = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = Jproblemas
        fields = tuple(f.name for f in Jproblemas._meta.fields) + ("url",)
