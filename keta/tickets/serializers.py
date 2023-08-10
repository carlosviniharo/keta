from rest_framework import serializers
from .models import *


def model_serilaizers(model_class):
    def decorator(serializer_class):
        class ModelSerializer(serializer_class):
            class Meta(serializer_class.Meta):
                model= model_class
                fields = '__all__'
        return ModelSerializer
    return decorator


@model_serilaizers(Jcanalesrecepciones)
class JcanalesrecepcionesSerializer(serializers.ModelSerializer):
    pass


@model_serilaizers(Jclasestarjetas)
class JclasestarjetasSerializer(serializers.ModelSerializer):
    pass


@model_serilaizers(Jtiposproductos)
class JtiposproductosSerializer(serializers.ModelSerializer):
    pass


@model_serilaizers(Jconceptos)
class JconceptosSerializer(serializers.ModelSerializer):
    pass


@model_serilaizers(Jmarcastarjetas)
class JmarcastarjetasSerializer(serializers.ModelSerializer):
    pass


@model_serilaizers(Jprioridades)
class JprioridadesSerializer(serializers.ModelSerializer):
    pass


@model_serilaizers(Jtipostarjetas)
class JtipostarjetasSerializer(serializers.ModelSerializer):
    pass


@model_serilaizers(Jtarjetas)
class JtarjetasSerializer(serializers.ModelSerializer):
    pass


@model_serilaizers(Jtiposcomentarios)
class JtiposcomentariosSerializer(serializers.ModelSerializer):
    pass


@model_serilaizers(Jtickettipos)
class JtickettiposSerializer(serializers.ModelSerializer):
    pass


@model_serilaizers(Jtipostransacciones)
class JtipostransaccionesSerializer(serializers.ModelSerializer):
    pass