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
    
    masked_numerotarjeta = serializers.SerializerMethodField()
    
    class Meta:
        model = Vreportereclamostarjeta
        fields = '__all__'
    
    def get_masked_numerotarjeta(self, obj):
        # Implement your masking logic here
        # For example, you can replace all but the last 4 digits with asterisks
        masked_value = '*' * (len(str(obj.cardnumber)) - 4) + str(obj.cardnumber)[-4:]
        return masked_value


class VreportereclamosgeneralesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vreportereclamosgenerales
        fields = "__all__"
