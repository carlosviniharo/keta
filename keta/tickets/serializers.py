from rest_framework import serializers
from .models import *
from users.models import *


def model_serializers(model_):
    def decorator(serializer_class):
        class ModelSerializer(serializer_class):
            class Meta:
                model = model_
                fields = '__all__'
        return ModelSerializer
    return decorator


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


# class JproblemasSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Jproblemas
#         fields = '__all__'

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
    class Meta:
        model = Jproblemas
        fields = '__all__'


class JpersonasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jpersonas
        fields = '__all__'


class personaticketsSerializer(serializers.Serializer):
    persona = JpersonasSerializer()
    ticket = JproblemasSerializer()
