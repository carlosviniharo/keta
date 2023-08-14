from django.db import IntegrityError
from rest_framework import serializers
from .models import *


class JusuariosSerializer(serializers.ModelSerializer):

    class Meta:
        model = Jusuarios
        fields = '__all__'

    def create(self, validate_data):
        try:
            user = Jusuarios.objects.create(
                email=validate_data['email'],
                username=validate_data['username'],
                idrol=validate_data['idrol'],
                iddepartamento=validate_data['iddepartamento'],
                idcargo=validate_data['idcargo']
            )
            user.set_password(validate_data['password'])
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


# Decorator wrapper for the serializers.
def model_serializers(model_):
    def decorator(serializer_class):
        class ModelSerializer(serializer_class):
            class Meta:
                model = model_
                fields = '__all__'
        return ModelSerializer
    return decorator


@model_serializers(Jcargos)
class JcargosSerializer(serializers.ModelSerializer):
    pass


@model_serializers(Jcorporaciones)
class JcorporacionesSerializer(serializers.ModelSerializer):
    pass


@model_serializers(Jdepartamentos)
class JdepartamentosSerializer(serializers.ModelSerializer):
    pass


@model_serializers(Jgeneros)
class JgenerosSerializer(serializers.ModelSerializer):
    pass


@model_serializers(Jgeografia)
class JgeografiaSerializer(serializers.ModelSerializer):
    pass


@model_serializers(Jpersonas)
class JpersonasSerializer(serializers.ModelSerializer):
    pass


@model_serializers(Jroles)
class JrolesSerializer(serializers.ModelSerializer):
    pass


@model_serializers(Jsucursales)
class JsucursalesSerializer(serializers.ModelSerializer):
    pass


@model_serializers(Jtiposidentificaciones)
class JtiposidentificacionesSerializer(serializers.ModelSerializer):
    pass


@model_serializers(Jtipospersonas)
class JtipospersonasSerializer(serializers.ModelSerializer):
    pass


class JpersonasUsuariosSerializer(serializers.Serializer):
    persona = JpersonasSerializer()
    usuario = JusuariosSerializer()


