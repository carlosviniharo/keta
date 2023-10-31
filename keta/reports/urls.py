from django.urls import path

from .views import (
    VcobrosindebiosReportView,
    VcobrosindebiosListView,
    GeneratePdfReport
)

urlpatterns = [
    path(
        "cobrosindebidos/",
        VcobrosindebiosReportView.as_view(),
        name="cobrosindebidos-list",
    ),
    path(
        "cobrosindebiostable/",
        VcobrosindebiosListView.as_view(),
        name="cobrosindebiostable-list",
    ),
    path(
        "generate_pdf/<int:pk>/",
        GeneratePdfReport.as_view(),
        name="generatePDF"
    ),
]
