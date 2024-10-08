from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    JestadosViewSet,
    JtareasticketViewSet,
    JestadotareasViewSet,
    FilteredTaskView,
    VtareaestadocolorListView,
    VtareasListView,
    JarchivosListView,
    JarchivoRetrieveView,
    JarchivosCreateView,
    JarchivosViewSet,
    VtareasrechazadasListView,
    VtaskListView,
    GenerateExcelView,
)

router = DefaultRouter()
router.register(r"estados", JestadosViewSet)
router.register(r"tareas", JtareasticketViewSet)
router.register(r"colours", JestadotareasViewSet)
router.register(r"archivos", JarchivosViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    # Not CRUD supported endpoints
    path(
        "filtered_tickets/",
        FilteredTaskView.as_view(),
        name="filtered_tickets-list"
    ),
    path(
        "vtareaestadocolor/",
        VtareaestadocolorListView.as_view(),
        name="tareaestadocolor-list"
    ),
    path(
        "rejectedTasksByUser/",
        VtareasrechazadasListView.as_view(),
        name="rejectedtasksbyuser-list"
    ),
    path(
        "vtareas/",
        VtareasListView.as_view(),
        name="vtareas-list"
    ),
    path(
        "allTasks/",
        VtaskListView.as_view(),
        name="alltasks-list"
    ),
    path(
        "archivoslist/",
        JarchivosListView.as_view(),
        name="archivos-list"
    ),
    path(
        "getarchivos/<int:pk>/",
        JarchivoRetrieveView.as_view(),
        name="archivos-files"
    ),
    path(
        "createarchivos/",
        JarchivosCreateView.as_view(),
        name="archivos-create"
    ),
    path(
        "generateExcel/",
        GenerateExcelView.as_view(),
        name="generate-excel"
    ),
]
