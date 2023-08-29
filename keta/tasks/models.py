from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models
from tickets.models import Jproblemas, Jprioridades
from users.models import Jusuarios

indicators = (
    ("P", "Padre"),
    ("A", "Ayuda")
)


class Jestados(models.Model):
    idestado = models.AutoField(primary_key=True)
    codigoestado = models.BigIntegerField(blank=True, null=True)
    descripcionestado = models.CharField(max_length=250, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'jestados'

    objects = models.Manager()

    def __str__(self):
        return self.descripcionestado


class Jestadotareas(models.Model):
    idestadotarea = models.AutoField(primary_key=True)
    tiempooptimo = models.DateTimeField(blank=True, null=True)
    tiemporequerido = models.DateTimeField(blank=True, null=True)
    tiempoinicial = models.DateTimeField(blank=True, null=True)
    tiempofinal = models.DateTimeField(blank=True, null=True)
    color = models.CharField(max_length=100, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)
    idtarea = models.ForeignKey('Jtareasticket', models.DO_NOTHING, db_column='idtarea', blank=True, null=True)

    class Meta:
        db_table = 'jestadotareas'

    objects = models.Manager()

    def __str__(self):
        return self.color


# TODO tests a example of store several base64 strings in archivo
class Jtareasticket(models.Model):
    idtarea = models.AutoField(primary_key=True)
    descripciontarea = models.CharField(max_length=500, blank=True, null=True)
    indicador = models.CharField(max_length=2, choices=[value for value in indicators], blank=True, null=True)
    fechaasignacion = models.DateTimeField(auto_now=True, null=True)
    fechaentrega = models.DateTimeField(blank=True, null=True)
    archivo = models.TextField(blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)
    fkidtarea = models.ForeignKey('self', models.DO_NOTHING, db_column='fkidtarea', blank=True, null=True)
    idestado = models.ForeignKey(Jestados, models.DO_NOTHING, db_column='idestado', blank=True, null=True)
    idprioridad = models.ForeignKey(Jprioridades, models.DO_NOTHING, db_column='idprioridad', blank=True, null=True)
    idproblema = models.ForeignKey(Jproblemas, models.DO_NOTHING, db_column='idproblema', blank=True, null=True)
    idusuarioasignado = models.ForeignKey(Jusuarios, models.DO_NOTHING, db_column='idusuarioasignado', blank=True, null=True)
    idusuarioqasigno = models.ForeignKey(Jusuarios, models.DO_NOTHING, db_column='idusuarioqasigno', related_name='jtareasticket_idusuarioqasigno_set', blank=True, null=True)
    tareaprincipal = models.ForeignKey('self', models.DO_NOTHING, db_column='tareaprincipal', related_name='jtareasticket_tareaprincipal_set', blank=True, null=True)

    class Meta:
        db_table = 'jtareasticket'
        ordering = ["-fechaasignacion"]

    objects = models.Manager()

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if isinstance(self.archivo, str):
    #         self.archivo = self._parse_archivo(self.archivo)
    #
    # def _parse_archivo(self, archivo_str):
    #     if archivo_str:
    #         return archivo_str[1:-1].split(',')
    #     return []

    def __str__(self):
        return f"{self.idtarea} - {self.indicador} - {self.idusuarioasignado}"
