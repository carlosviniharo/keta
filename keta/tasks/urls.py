from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    JestadosViewSet,
    JtareasticketViewSet,
    JestadotareasViewSet,
    FilteredTaskView,
    EmailNotificationView,
    VtareaestadocolorListView,
)
router = DefaultRouter()
router.register(r'estados', JestadosViewSet)
router.register(r'tareas', JtareasticketViewSet)
router.register(r'colours', JestadotareasViewSet)
# router.register(r'filtered_tickets', FilteredTaskView)

urlpatterns = [
    path('api/', include(router.urls)),
    # Not CRUD supported endpoints
    path('filtered_tickets/', FilteredTaskView.as_view(), name='filtered_tickets-list'),
    path('send_email/', EmailNotificationView.as_view(), name='emails'),
    path('tareaestadocolor/', VtareaestadocolorListView.as_view(), name='tareaestadocolor-list'),
]
