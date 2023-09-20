from django.db import IntegrityError
from rest_framework import serializers

from .models import (
    Jusuarios,
    Jpersonas,
    Jcargos,
    Jdepartamentos,
    Jcorporaciones,
    Jgeneros,
    Jgeografia,
    Jroles,
    Jsucursales,
    Jtiposidentificaciones,
    Jtipospersonas,
    Vusuarios,
)


# Decorator wrapper for the serializers.
def model_serializers(model_):
    def decorator(serializer_class):
        class ModelSerializer(serializer_class):
            class Meta:
                model = model_
                fields = tuple(f.name for f in model_._meta.fields) + ("url",)

        return ModelSerializer

    return decorator


@model_serializers(Jcargos)
class JcargosSerializer(serializers.HyperlinkedModelSerializer):
    pass


@model_serializers(Jcorporaciones)
class JcorporacionesSerializer(serializers.HyperlinkedModelSerializer):
    pass


@model_serializers(Jdepartamentos)
class JdepartamentosSerializer(serializers.HyperlinkedModelSerializer):
    pass


@model_serializers(Jgeneros)
class JgenerosSerializer(serializers.HyperlinkedModelSerializer):
    pass


@model_serializers(Jgeografia)
class JgeografiaSerializer(serializers.HyperlinkedModelSerializer):
    pass


@model_serializers(Jpersonas)
class JpersonasSerializer(serializers.HyperlinkedModelSerializer):
    pass


@model_serializers(Jroles)
class JrolesSerializer(serializers.HyperlinkedModelSerializer):
    pass


@model_serializers(Jsucursales)
class JsucursalesSerializer(serializers.HyperlinkedModelSerializer):
    pass


@model_serializers(Jtiposidentificaciones)
class JtiposidentificacionesSerializer(serializers.HyperlinkedModelSerializer):
    pass


@model_serializers(Jtipospersonas)
class JtipospersonasSerializer(serializers.HyperlinkedModelSerializer):
    pass


@model_serializers(Jusuarios)
class JusuariosSerializer(serializers.HyperlinkedModelSerializer):
    def create(self, validated_data):
        try:
            user = Jusuarios.objects.create(
                email=validated_data["email"],
                username=validated_data["username"],
                idrol=validated_data["idrol"],
                iddepartamento=validated_data["iddepartamento"],
                idcargo=validated_data["idcargo"],
            )
            user.set_password(validated_data["password"])
            user.save()
            return user
        except IntegrityError as e:
            # Handle the exception if the user creation fails due to integrity error
            # For example, you can log the error or take appropriate action
            print("Error:", e)
            return None
        except KeyError as e:
            # Handle the exception if a required key is missing in validate_data
            # For example, you can log the error or raise a custom exception
            print("Error: Required key is missing:", e)
            return None


class VusuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vusuarios
        fields = "__all__"
