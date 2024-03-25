from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    JcargosViewSet,
    JdepartamentosViewSet,
    JcorporacionesViewSet,
    JgenerosViewSet,
    JgeografiaViewSet,
    JrolesListViewSet,
    JsucursalesViewSet,
    JtiposidentificacionesViewSet,
    JtipospersonasViewSet,
    JpersonasViewSet,
    JusuariosViewSet,
    CustomTokenObtainPairView,
    CustomLogoutView,
    JusuarioListView,
    JsucursalJdepartamentosListView,
    VusuariosReportView,
    JpersonasListView,
    VusuariosAsignationView,
    JdiasfestivosViewSet,
    JdiasfestivosActiveView,
    VusuariosActiveView,
)

router = DefaultRouter()
router.register(r"cargos", JcargosViewSet)
router.register(r"departamentos", JdepartamentosViewSet)
router.register(r"diasfestivos", JdiasfestivosViewSet)
router.register(r"corporaciones", JcorporacionesViewSet)
router.register(r"generos", JgenerosViewSet)
router.register(r"geografia", JgeografiaViewSet)
router.register(r"roles", JrolesListViewSet)
router.register(r"sucursales", JsucursalesViewSet)
router.register(r"tiposidentificaciones", JtiposidentificacionesViewSet)
router.register(r"tipospersonas", JtipospersonasViewSet)
router.register(r"personas", JpersonasViewSet)
router.register(r"personaidentificacion", JpersonasListView, basename="custom-personas")
router.register(r"usuarios", JusuariosViewSet)


urlpatterns = [
    path("api/", include(router.urls)),
    # Not CRUD supported endpoints
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", CustomLogoutView.as_view(), name="logout_user"),
    path("user_profile/<str:email>/", JusuarioListView.as_view(), name="profile"),
    path(
        "sucursaldepartamentos/",
        JsucursalJdepartamentosListView.as_view(),
        name="jsucursal_jdepartamentos",
    ),
    path(
        "usuarios_reporte/", VusuariosReportView.as_view(), name="usuariosreporte-list"
    ),
    path(
       "usuarios_asignacion/", VusuariosAsignationView.as_view(), name="usuariosasignacion-list"
    ),
    path(
        "activeUsers/", VusuariosActiveView.as_view(), name="activeusers-list"
    ),
    # Jdiasfestivos especial endpoints
    path(
        "activeDiasFestivos/", JdiasfestivosActiveView.as_view(), name="activediasfestivos-list"
    ),
]
