from django.urls import path, include

from .views import VcobrosindebiosReportView, VcobrosindebiosListView

urlpatterns = [
    path('cobrosindebidos/', VcobrosindebiosReportView.as_view(), name='cobrosindebidos-list'),
    path('cobrosindebiostable/', VcobrosindebiosListView.as_view(), name='cobrosindebiostable-list')
]