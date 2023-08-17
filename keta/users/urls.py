from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView
)
from .views import *

router = DefaultRouter()
router.register(r'cargos', JcargosViewSet)
router.register(r'departamentos', JdepartamentosViewSet)
router.register(r'corporaciones', JcorporacionesViewSet)
router.register(r'generos', JgenerosViewSet)
router.register(r'geografia', JgeografiaViewSet)
router.register(r'roles', JrolesListViewSet)
router.register(r'sucursales', JsucursalesViewSet)
router.register(r'tiposidentificaciones', JtiposidentificacionesViewSet)
router.register(r'tipospersonas', JtipospersonasViewSet)
router.register(r'persona', JpersonasViewSet)
router.register(r'usuario', JusuariosViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', CustomLogoutView.as_view(), name='logout_user'),
    ]