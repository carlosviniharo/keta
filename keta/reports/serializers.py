from rest_framework import serializers

from .models import Vcobrosindebios


class VcobrosindebiosSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Vcobrosindebios
        fields = "__all__"
