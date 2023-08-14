import sys

from django.apps import apps
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from .serializers import *


class BaseListView(ListAPIView):
    queryset = None
    serializer_class = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        model_name = self.__class__.__name__[:-8]  # Remove "ListView" from the class name
        model = apps.get_model('tickets', model_name)
        self.queryset = model.objects.all()
        serializer_name = f"{model_name}Serializer"
        serializer_class = getattr(sys.modules[__name__], serializer_name)
        self.serializer_class = serializer_class


class JcanalesrecepcionesListView(BaseListView):
    pass


class JclasestarjetasListView(BaseListView):
    pass


class JtiposproductosListView(BaseListView):
    pass


class JconceptosListView(BaseListView):
    pass


class JmarcastarjetasListView(BaseListView):
    pass


class JprioridadesListView(BaseListView):
    pass


class JproblemaslistView(BaseListView):
    pass


class JtipostarjetasListView(BaseListView):
    pass


class JtarjetasListView(BaseListView):
    pass


class JtiposcomentariosListView(BaseListView):
    pass


class JtickettiposListView(BaseListView):
    pass


class JtipostransaccionesListView(BaseListView):
    pass


class JproblemasViewSet(viewsets.ModelViewSet):
    queryset = Jproblemas.objects.all()
    serializer_class = JproblemasSerializer
