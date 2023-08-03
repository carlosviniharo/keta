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


class JcargosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jcargos
        fields = '__all__'


class JcorporacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jcorporaciones
        fields = '__all__'


class JdepartamentosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jdepartamentos
        fields = '__all__'


class JgenerosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jgeneros
        fields = '__all__'


class JgeografiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jgeografia
        fields = '__all__'


class JpersonasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jpersonas
        fields = '__all__'


class JrolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jroles
        fields = '__all__'


class JsucursalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jsucursales
        fields = '__all__'


class JtipoidentificacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jtiposidentificaciones
        fields = '__all__'


class JtipopersonasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jtipospersonas
        fields = '__all__'


class JpersonasUsuariosSerializer(serializers.Serializer):
    persona = JpersonasSerializer()
    usuario = JusuariosSerializer()

