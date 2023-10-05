import re
from collections import namedtuple
from django.db.models import Q
from django.http import StreamingHttpResponse, HttpResponse
from django.template.loader import get_template
from django.utils import timezone
from rest_framework.exceptions import APIException
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import viewsets, status

from lxml import etree
import pdfkit

from .utils.helper import format_date
from tasks.utils.helper import convert_pdf_to_b64
from tasks.models import Jarchivos
from .models import (
    Vcobrosindebios,
    Vreportecobrosindebidos,
    Vreportereclamostarjeta,
    Vreportereclamosgenerales,
)
from .serializers import (
    VcobrosindebiosSerilizer,
    VreportecobrosindebidosSerializer,
    VreportereclamostarjetaSerializer,
    VreportereclamosgeneralesSerializer
)

from tasks.models import Jtareasticket

DICTIONARY_HEADER_REPORT = {
    "xmlns": "http://www.seps.gob.ec/reclamoCI01",
    "estructura": "CI01",
    "rucEntidad": "1234567890001",
    "fechaCorte": "",
    "numRegistro": 0,
}

DICTIONARY_NAMES_ENTRIES_REPORT = {
    "tipoidentificacionsujeto": "tipoIdentificacionSujeto",
    "identificacionsujeto": "identificacionSujeto",
    "nomapellidonomrazonsocial": "nomApellidoNomRazonSocial",
    "canalrecepcion": "canalRecepcion",
    "fecharecepcion": "fechaRecepcion",
    "tipotransaccion": "tipoTransaccion",
    "concepto": "concepto",
    "estadoreclamo": "estadoReclamo",
    "fecharespuesta": "fechaRespuesta",
    "tiporesolucion": "tipoResolucion",
    "montorestituido": "montoRestituido",
    "interesmonto": "interesMonto",
    "totalrestituido": "totalRestituido",
}
DATE_FORMAT = "%Y-%m-%d"

DICTIONARY_ARCHIVO_REPORT = {
    "idtarea": 0,
    "nombrearchivo": "",
    "descripcionarchivo": "Reporte generado automaticamente al registrarse exitosamente el reclamo",
    "contenidoarchivo": "",
    "mimetypearchivo": "application/pdf",
}

# Tuple to map the serializer, model to the html depending on the type of report
Report = namedtuple("Report", "type model serializer html")
DIC_REPORTS = {
    1: Report(
        "Cobros Indebidos",
        Vreportecobrosindebidos,
        VreportecobrosindebidosSerializer,
        "html/cobrosIndebidos.html"
    ),
    2: Report(
        "Reclamos Tarjetas",
        Vreportereclamostarjeta,
        VreportereclamostarjetaSerializer,
        "html/reclamosTarjeta.html"
    ),
    3: Report(
        "Reclamos Generales",
        Vreportereclamosgenerales,
        VreportereclamosgeneralesSerializer,
        "html/reclamosGenerales.html",
    ),
}


class VcobrosindebiosReportView(ListAPIView):
    serializer_class = VcobrosindebiosSerilizer

    def get(self, request, *args, **kwargs):
        # Create the StreamingHttpResponse without the data generator
        response = StreamingHttpResponse(content_type="application/xml")
        response["Content-Disposition"] = 'attachment; filename="xml_report.xml"'

        fecha_inicio = self.request.query_params.get("fecha_inicio", None)
        fecha_final = self.request.query_params.get("fecha_final", None)

        if fecha_inicio and fecha_final:
            fecha_inicio = timezone.datetime.strptime(fecha_inicio, DATE_FORMAT)
            fecha_final = timezone.datetime.strptime(
                fecha_final, DATE_FORMAT
            ) + timezone.timedelta(hours=23, minutes=59)
        else:
            raise APIException("Please provide proper fecha_inicio and fecha_final")

        # Validate the XML conten
        self.validate_xml(self.create_xml_streaming_response(fecha_inicio, fecha_final))

        response.streaming_content = self.create_xml_streaming_response(
            fecha_inicio, fecha_final
        )

        return response

    def create_xml_streaming_response(self, fecha_inicio, fecha_final):
        def data_generator():
            queryset = Vcobrosindebios.objects.filter(
                Q(fecharecepcion__range=(fecha_inicio, fecha_final))
                | Q(fecharespuesta__range=(fecha_inicio, fecha_final))
            )

            serializer = self.get_serializer(queryset, many=True)
            DICTIONARY_HEADER_REPORT["numRegistro"] = len(serializer.data)
            DICTIONARY_HEADER_REPORT["fechaCorte"] = format_date(str(fecha_final))
            yield '<?xml version="1.0" encoding="UTF-8"?>\n'
            yield "<reclamosCI01 {}>\n".format(
                " ".join([f'{k}="{v}"' for k, v in DICTIONARY_HEADER_REPORT.items()])
            )

            for report_dic in serializer.data:
                attributes = self.process_report_data(report_dic)
                yield f"  <elemento {attributes} />\n"

            yield "</reclamosCI01>"

        return data_generator()
    
    @staticmethod
    def process_report_data(self, report_dic):
        # Create a copy of the report_dic to avoid modifying it during iteration.
        report_copy = report_dic.copy()
        attributes = []

        if report_copy.get("estadoreclamo") == "1":
            del report_copy["fecharespuesta"]
            del report_copy["tiporesolucion"]

        for key, value in report_copy.items():
            if isinstance(value, (int, float)):
                value = "%.2f" % float(value)

            if key in ["fecharecepcion", "fecharespuesta"]:
                # Ensure that self.format_date is defined and works correctly.
                value = format_date(value, report_dic.get("ticket"))

            # Ensure that DICTIONARY_NAMES_ENTRIES_REPORT contains necessary mappings.
            attribute_name = DICTIONARY_NAMES_ENTRIES_REPORT.get(key, key)
            if key == "ticket":
                pass
            else:
                attributes.append(f'{attribute_name}="{value}"')
        return " ".join(attributes)

    @staticmethod
    def validate_xml(streaming_content):
        xmlschema_doc = etree.parse(r"reports/templates/xsd/structure.xsd")
        xmlschema = etree.XMLSchema(xmlschema_doc)
        xml_content = ""

        for chunk in streaming_content:
            if re.findall(r"<\?xml.*?\?>", chunk):
                pass
            else:
                xml_content += chunk
                try:
                    xmlschema.assertValid(etree.fromstring(xml_content))
                except etree.XMLSyntaxError:
                    continue
                except etree.DocumentInvalid as er:
                    raise er
        return True


class VcobrosindebiosListView(ListAPIView):
    serializer_class = VcobrosindebiosSerilizer
    queryset = Vcobrosindebios.objects.all()

    def list(self, request, *args, **kwargs):
        fecha_inicio = self.request.query_params.get("fecha_inicio", None)
        fecha_final = self.request.query_params.get("fecha_final", None)

        if fecha_inicio and fecha_final:
            fecha_inicio = timezone.datetime.strptime(fecha_inicio, DATE_FORMAT)
            fecha_final = timezone.datetime.strptime(
                fecha_final, DATE_FORMAT
            ) + timezone.timedelta(hours=23, minutes=59)
        else:
            raise APIException("Please provide proper fecha_inicio and fecha_final")

        queryset = Vcobrosindebios.objects.filter(
            Q(fecharecepcion__range=(fecha_inicio, fecha_final))
            | Q(fecharespuesta__range=(fecha_inicio, fecha_final))
        )
        if not queryset:
            return Response(
                {
                    "detail": "Not record was found in the database in that period of time"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# TODO Finish the generation of the report as the format is incorrect
#  and it does not contain the propre information.
class GeneratePdfReport(RetrieveAPIView):
    serializer_class = None
    report = None
    task = None
    
    def get_queryset(self):
        # Access kwargs from self.kwargs
        pk = self.kwargs.get("pk")
        self.task = Jtareasticket.objects.get(idtarea=pk)
        # Use pk to fetch ticket_type
        id_ticket_type = self.task.idproblema.idtipoticket.idtipoticket
        
        # Get the report based on ticket_type from DIC_REPORTS
        self.report = DIC_REPORTS.get(id_ticket_type, "")
        
        # Check if a report was found
        if self.report:
            # Set the serializer class based on the report
            self.serializer_class = self.report.serializer
            return self.report.model.objects.get(ticket=pk)
        else:
            # Handle the case where no report was found
            raise ValueError(f"Ticket type {ticket_type} does not support reports")

    def retrieve(self, request, *args, **kwargs):
        ticket = self.get_queryset()
        template = get_template(self.report.html)
        data_ticket = self.get_serializer(ticket)
        data_report = data_ticket.data
        data_report["date"] = format_date(data_ticket.data["date"])
        html_content = template.render(data_report)

        # Specify the options for PDF generation
        options = {
            "enable-local-file-access": "",
        }
        
        # Generate PDF from HTML using pdfkit
        pdf = pdfkit.from_string(html_content, False, options=options)
        # Populating the data for sending the file to the database
        DICTIONARY_ARCHIVO_REPORT["idtarea"] = self.task
        DICTIONARY_ARCHIVO_REPORT["nombrearchivo"] = f"{kwargs.get('pk')} {self.report.type}"
        DICTIONARY_ARCHIVO_REPORT["contenidoarchivo"] = convert_pdf_to_b64(pdf)
        
        Jarchivos.objects.update_or_create(**DICTIONARY_ARCHIVO_REPORT)
        
        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = 'filename="output.pdf"'
        return response
