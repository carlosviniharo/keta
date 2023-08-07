from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', CustomLogoutView.as_view(), name='logout_user'),
    path('user_register/', JusuariosRegisterView.as_view(), name="sign_up"),
    path('user_profile/<str:email>/', JususarioRegisterView.as_view(), name="profile"),
    path('cargos/', JcargosListView.as_view(), name="cargos_list"),
    path('corporaciones/', JcorporacionesListView.as_view(), name='corporaciones_list'),
    path('departamentos/', JdepartamentosListView.as_view(), name='departamentos_list'),
    path('generos/', JgenerosListView.as_view(), name='generos_list'),
    path('geografia/', JgeografiaListView.as_view(), name='geografia_list'),
    path('roles/', JrolesListView.as_view(), name='roles_list'),
    path('sucursales/', JsucursalesListView.as_view(), name='sucursales_list'),
    path('tiposidentificaciones/', JtiposidentificacionesListView.as_view(), name='tipoidentificaciones_list'),
    path('tipospersonas/', JtipospersonasListView.as_view(), name='tipopersonas_list'),
    path('person_register/', JpersonasRegisterView.as_view(), name='jpersonas_create'),
    path('sucursaldepartamentos/', JsucursalJdepartamentosListView.as_view(), name='sucursaldepartamentos_list'),
]