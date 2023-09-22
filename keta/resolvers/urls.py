from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    JclasificacionesresolucionesViewSet,
    JtiporesolucionesViewSet,
    JresolucionesViewSet,
    JvaloresresolucionesViewSet,
)

router = DefaultRouter()
router.register(r"clasificacionesresoluciones", JclasificacionesresolucionesViewSet)
router.register(r"tiporesoluciones", JtiporesolucionesViewSet)
router.register(r"resoluciones", JresolucionesViewSet)
router.register(r"valoresresoluciones", JvaloresresolucionesViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
]
