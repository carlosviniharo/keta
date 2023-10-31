from rest_framework import serializers

from .models import (
    Vcobrosindebios,
    Vreportecobrosindebidos,
    Vreportereclamostarjeta,
    Vreportereclamosgenerales,
)


class VcobrosindebiosSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Vcobrosindebios
        fields = "__all__"


class VreportecobrosindebidosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vreportecobrosindebidos
        fields = "__all__"


class VreportereclamostarjetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vreportereclamostarjeta
        fields = "__all__"


class VreportereclamosgeneralesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vreportereclamosgenerales
        fields = "__all__"
