from rest_framework import serializers
from .models import *
from users.models import *
from users.serializers import model_serializers


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


@model_serializers(Jproblemas)
class JproblemasSerializer(serializers.HyperlinkedModelSerializer):
    pass

