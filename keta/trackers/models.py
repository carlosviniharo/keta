from django.db import models

from users.models import Jusuarios
from tasks.models import Jtareasticket


class Jseguimientostareas(models.Model):
    idseguimientotarea = models.AutoField(primary_key=True)
    tituloseguimientotarea = models.CharField(max_length=500, blank=True, null=True)
    detalleresolucion = models.CharField(max_length=1000, blank=True, null=True)
    status = models.BooleanField(blank=True, null=True)
    fechacreacion = models.DateTimeField(auto_now_add=True, null=True)
    fechamodificacion = models.DateTimeField(blank=True, null=True)
    fecharegistro = models.DateTimeField(auto_now_add=True, null=True)
    idtarea = models.ForeignKey(
        Jtareasticket, models.DO_NOTHING, db_column="idtarea", blank=True, null=True
    )

    class Meta:
        db_table = "jseguimientostareas"

    objects = models.Manager()
    
    def __str__(self):
        return self.tituloseguimientotarea


class Jnotificaciones(models.Model):
    idnotificacion = models.AutoField(primary_key=True)
    idusuario = models.ForeignKey(Jusuarios, models.DO_NOTHING, db_column='idusuario', blank=True, null=True)
    idtarea = models.ForeignKey(Jtareasticket, models.DO_NOTHING, db_column='idtarea', blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    notification_type = models.CharField(max_length=200, blank=True, null=True)
    status = models.BooleanField(blank=True, null=True)

    class Meta:
        db_table = 'jnotificaciones'
        
    objects = models.Manager()

    def __str__(self):
        return f"{self.idtarea} - {self.notification_type} - {self.created_at}"
