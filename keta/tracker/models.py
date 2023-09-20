from django.db import models

from tasks.models import Jtareasticket


class Jseguimientostareas(models.Model):
    idseguimientotarea = models.AutoField(primary_key=True)
    detalleresolucion = models.CharField(max_length=500, blank=True, null=True)
    status = models.BooleanField(blank=True, null=True)
    fechacreacion = models.DateTimeField(auto_now_add=True, null=True)
    fechamodificacion = models.DateTimeField(blank=True, null=True)
    archivo = models.CharField(max_length=500, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)
    idtarea = models.ForeignKey(
        Jtareasticket, models.DO_NOTHING, db_column="idtarea", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "jseguimientostareas"

    objects = models.Manager()
