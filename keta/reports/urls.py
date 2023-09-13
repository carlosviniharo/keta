from django.urls import path, include

from .views import VcobrosindebiosListView

urlpatterns = [
    path('cobrosindebidos/', VcobrosindebiosListView.as_view(), name='cobrosindebidos-list')
]