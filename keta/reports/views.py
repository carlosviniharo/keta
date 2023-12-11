import re
from collections import namedtuple

from django.db import transaction, IntegrityError
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.http import StreamingHttpResponse, HttpResponse
from django.template.loader import get_template
from django.utils import timezone
from rest_framework.exceptions import APIException
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status

from lxml import etree
import pdfkit

from tasks.models import Jarchivos, Jtareasticket
from .utils.helper import format_date
from tasks.utils.helper import convert_pdf_to_b64

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
    "descripcionarchivo": "Reporte generado automaticamente al "
                          "registrarse exitosamente el reclamo",
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
        self.validate_xml(self.create_xml_streaming_response(
            fecha_inicio,
            fecha_final,
        ))

        response.streaming_content = self.create_xml_streaming_response(
            fecha_inicio,
            fecha_final
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
            yield "<reclamosCI01 {} />\n".format(
                " ".join([f'{k}="{v}"' for k, v in DICTIONARY_HEADER_REPORT.items()])
            )

            for report_dic in serializer.data:
                attributes = self.process_report_data(report_dic)
                yield f"  <elemento {attributes} />\n"

            yield "</reclamosCI01>"

        return data_generator()
    
    @staticmethod
    def process_report_data(report_dic):
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


class GeneratePdfReport(RetrieveAPIView):
    serializer_class = None
    report = None
    task = None
    
    def get_queryset(self):
        pk = self.kwargs.get("pk")
        self.get_task(pk)
        self.get_report()
        return self.get_ticket_object(pk)
    
    def get_task(self, pk):
        try:
            self.task = Jtareasticket.objects.get(idtarea=pk)
        except ObjectDoesNotExist as exc:
            raise APIException(f"The ticket number {pk} does not exist, verbose {exc}")
    
    def get_report(self):
        id_ticket_type = self.task.idproblema.idtipoticket.idtipoticket
        self.report = DIC_REPORTS.get(id_ticket_type, "")
        if not self.report:
            raise APIException(f"Ticket type {self.task.idproblema.idtipoticket} does not support reports")
    
    def get_ticket_object(self, pk):
        self.serializer_class = self.report.serializer
        try:
            ticket_object = self.report.model.objects.get(ticket=pk)
        except ObjectDoesNotExist:
            raise APIException(f"Ticket number {pk} is not a main task")
        return ticket_object
    
    def retrieve(self, request, *args, **kwargs):
        ticket = self.get_queryset()
        data_report = self.get_report_data(ticket)
        html_content = self.render_html(data_report)
        pdf = self.generate_pdf(html_content)
        self.save_pdf_to_database(pdf)
        return Response(
            {"detail": "File successfully crested and saved"},
            status=status.HTTP_201_CREATED
        )
    
    def get_report_data(self, ticket):
        data_ticket = self.get_serializer(ticket)
        data_report = data_ticket.data
        data_report["date"] = format_date(data_ticket.data["date"])
        return data_report
    
    def render_html(self, data_report):
        template = get_template(self.report.html)
        return template.render(data_report)
    
    def generate_pdf(self, html_content):
        options = {
            "enable-local-file-access": "",
        }
        return pdfkit.from_string(html_content, False, options=options)
    
    def save_pdf_to_database(self, pdf):
        DICTIONARY_ARCHIVO_REPORT["idtarea"] = self.task
        DICTIONARY_ARCHIVO_REPORT["nombrearchivo"] = f"{self.kwargs.get('pk')} {self.report.type}"
        DICTIONARY_ARCHIVO_REPORT["contenidoarchivo"] = convert_pdf_to_b64(pdf)
        try:
            with transaction.atomic():
                archivo = Jarchivos.objects.create(**DICTIONARY_ARCHIVO_REPORT)
        except IntegrityError:
            raise APIException(
                f"The file with the name '{DICTIONARY_ARCHIVO_REPORT['nombrearchivo']}' was not saved"
            )
