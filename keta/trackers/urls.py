from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    JseguimientostareasSetView,
    JseguimientotareasListView,
    JnotificacionesUpdatelListView,
    JnotificacionesSetView,
)

router = DefaultRouter()
router.register("seguimientostareas", JseguimientostareasSetView)
router.register("notificaciones", JnotificacionesSetView)

urlpatterns = [
    path("api/", include(router.urls)),
    path(
        "seguimientotareaslist/",
        JseguimientotareasListView.as_view(),
        name="seguimientotareas-list",
    ),
    path(
        "notificacioneslist/",
        JnotificacionesUpdatelListView.as_view(),
        name="notifications-list"
    )
]
