from django.db import models
from tickets.models import Jproblemas, Jprioridades
from users.models import Jusuarios

indicators = {
    "Padre": "P",
    "Ayuda": "A"
}


class Jestados(models.Model):
    idestado = models.AutoField(primary_key=True)
    codigoestado = models.BigIntegerField(blank=True, null=True)
    descripcionestado = models.CharField(max_length=250, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'jestados'

    def __str__(self):
        return self.descripcionestado


class Jtareasticket(models.Model):
    idtarea = models.AutoField(primary_key=True)
    descripciontarea = models.CharField(max_length=500, blank=True, null=True)
    indicador = models.CharField(max_length=2, choices=[value for value in indicators.values()], blank=True, null=True)
    fechaasignacion = models.DateTimeField(auto_now=True, null=True)
    fechaentrega = models.DateTimeField(blank=True, null=True)
    archivo = models.CharField(max_length=500, blank=True, null=True)
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

    def __str__(self):
        return f"{self.idtarea} - {self.tareaprincipal} - {self.idusuarioasignado}"
