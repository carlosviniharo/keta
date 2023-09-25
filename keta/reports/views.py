import re

from django.db.models import Q
from django.http import StreamingHttpResponse
from django.utils import timezone
from rest_framework.exceptions import APIException
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import viewsets, status

from lxml import etree

from .models import Vcobrosindebios
from .serializers import VcobrosindebiosSerilizer

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
            DICTIONARY_HEADER_REPORT["fechaCorte"] = self.format_date(str(fecha_final))
            yield '<?xml version="1.0" encoding="UTF-8"?>\n'
            yield "<reclamosCI01 {}>\n".format(
                " ".join([f'{k}="{v}"' for k, v in DICTIONARY_HEADER_REPORT.items()])
            )

            for report_dic in serializer.data:
                attributes = self.process_report_data(report_dic)
                yield f"  <elemento {attributes} />\n"

            yield "</reclamosCI01>"

        return data_generator()

    def process_report_data(self, report_dic):
        # Create a copy of the report_dic to avoid modifying it during iteration.
        report_copy = report_dic.copy()
        attributes = []
        
        if report_copy.get("estadoreclamo") == "1":
            del report_copy["fecharespuesta"]
            del report_copy["fecharespuesta"]
            
        for key, value in report_copy.items():
            if isinstance(value, (int, float)):
                value = "%.2f" % float(value)

            if key in ["fecharecepcion", "fecharespuesta"]:
                # Ensure that self.format_date is defined and works correctly.
                value = self.format_date(value, report_dic.get("ticket"))

            # Ensure that DICTIONARY_NAMES_ENTRIES_REPORT contains necessary mappings.
            attribute_name = DICTIONARY_NAMES_ENTRIES_REPORT.get(key, key)
            if key == "ticket":
                pass
            else:
                attributes.append(f'{attribute_name}="{value}"')
        return " ".join(attributes)

    @staticmethod
    def format_date(date_str, ticket=None):
        pattern = r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})"
        match = re.search(pattern, date_str)
        if match:
            year, month, day = match.group("year", "month", "day")
            if year == "0001":
                raise APIException(f"There could not be generated the record as ticket {ticket} state is closed "
                                   f", however not resolution record was found")
            return f"{day}/{month}/{year}"

        else:
            raise ValueError("Invalid date format")

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
