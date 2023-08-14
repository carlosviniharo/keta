from rest_framework import serializers
from .models import *


def model_serializers(model_):
    def decorator(serializer_class):
        class ModelSerializer(serializer_class):
            class Meta:
                model = model_
                fields = '__all__'
        return ModelSerializer
    return decorator


@model_serializers(Jcanalesrecepciones)
class JcanalesrecepcionesSerializer(serializers.ModelSerializer):
    pass


@model_serializers(Jclasestarjetas)
class JclasestarjetasSerializer(serializers.ModelSerializer):
    pass


@model_serializers(Jtiposproductos)
class JtiposproductosSerializer(serializers.ModelSerializer):
    pass


@model_serializers(Jconceptos)
class JconceptosSerializer(serializers.ModelSerializer):
    pass


@model_serializers(Jmarcastarjetas)
class JmarcastarjetasSerializer(serializers.ModelSerializer):
    pass


@model_serializers(Jprioridades)
class JprioridadesSerializer(serializers.ModelSerializer):
    pass


@model_serializers(Jproblemas)
class JproblemasSerializer(serializers.ModelSerializer):
    pass


@model_serializers(Jtipostarjetas)
class JtipostarjetasSerializer(serializers.ModelSerializer):
    pass


@model_serializers(Jtarjetas)
class JtarjetasSerializer(serializers.ModelSerializer):
    pass


@model_serializers(Jtiposcomentarios)
class JtiposcomentariosSerializer(serializers.ModelSerializer):
    pass


@model_serializers(Jtickettipos)
class JtickettiposSerializer(serializers.ModelSerializer):
    pass


@model_serializers(Jtipostransacciones)
class JtipostransaccionesSerializer(serializers.ModelSerializer):
    pass
