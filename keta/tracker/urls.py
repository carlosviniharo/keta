from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import JseguimientostareasSetView, JseguimientotareasListView

router = DefaultRouter()
router.register('seguimientostareas', JseguimientostareasSetView)

urlpatterns = [
    path('api/', include(router.urls)),
    path('seguimientotareaslist/', JseguimientotareasListView.as_view(), name='seguimientotareas-list')
]