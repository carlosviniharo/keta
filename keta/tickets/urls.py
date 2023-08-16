from django.urls import path, include
from rest_framework.routers import DefaultRouter

from tickets.views import *

router = DefaultRouter()
router.register(r'canalesrecepciones', JcanalesrecepcionesViewSet)
router.register(r'clasestarjetas', JclasestarjetasViewSet)
router.register(r'tiposproductos', JtiposproductosViewSet)
router.register(r'conceptos', JconceptosViewSet)
router.register(r'marcastarjetas', JmarcastarjetasViewSet)
router.register(r'prioridades', JprioridadesViewSet)
router.register(r'tipostarjetas', JtipostarjetasViewSet)
router.register(r'tarjetas', JtarjetasViewSet)
router.register(r'tiposcomentarios', JtiposcomentariosViewSet)
router.register(r'tickettipos', JtickettiposViewSet)
router.register(r'tipostransacciones', JtipostransaccionesViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('create_tickets/', JproblemasCreateView.as_view(), name='create_ticket'),
]