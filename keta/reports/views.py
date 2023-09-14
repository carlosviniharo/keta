import re
from django.http import StreamingHttpResponse
from rest_framework.generics import ListAPIView

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


class VcobrosindebiosListView(ListAPIView):
    serializer_class = VcobrosindebiosSerilizer

    def get(self, request, *args, **kwargs):
        # Create the StreamingHttpResponse without the data generator
        response = StreamingHttpResponse(content_type="application/xml")
        response["Content-Disposition"] = 'attachment; filename="xml_report.xml"'

        fecha_inicio = self.request.query_params.get("fecha_inicio", None)
        fecha_final = self.request.query_params.get("fecha_final", None)

        # Validate the XML content
        if not self.validate_xml(self.create_xml_streaming_response(fecha_inicio, fecha_final)):
            raise APIException("Invalid XML document")

        response.streaming_content = self.create_xml_streaming_response(fecha_inicio, fecha_final)

        return response

    def create_xml_streaming_response(self, fecha_inicio, fecha_final):
        def data_generator():

            queryset = Vcobrosindebios.objects.filter(
                Q(fecharecepcion__range=(fecha_inicio, fecha_final)) &
                Q(fecharespuesta__range=(fecha_inicio, fecha_final))
            )

            serializer = self.get_serializer(queryset, many=True)
            DICTIONARY_HEADER_REPORT["numRegistro"] = len(serializer.data)
            DICTIONARY_HEADER_REPORT["fechaCorte"] = self.format_date(fecha_final)
            yield '<?xml version="1.0" encoding="UTF-8"?>\n'
            yield '<reclamosCI01 {}>\n'.format(" ".join([f'{k}="{v}"' for k, v in DICTIONARY_HEADER_REPORT.items()]))

            for report_dic in serializer.data:
                attributes = self.process_report_data(report_dic)
                yield f'  <elemento {attributes} />\n'

            yield "</reclamosCI01>"

        return data_generator()

    def process_report_data(self, report_dic):
        attributes = []
        for key, value in report_dic.items():
            if isinstance(value, (int, float)):
                value = "%.2f" % float(value)
            if key in ["fecharecepcion", "fecharespuesta"]:
                value = self.format_date(value)
            attributes.append(f'{DICTIONARY_NAMES_ENTRIES_REPORT[key]}="{value}"')
        return ' '.join(attributes)

    @staticmethod
    def format_date(date_str):
        pattern = r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})"
        match = re.search(pattern, date_str)
        if match:
            year, month, day = match.group("year", "month", "day")
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
                except etree.DocumentInvalid:
                    return False
        return True









