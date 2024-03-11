from django.db import models

from users.models import Jusuarios
from tasks.models import Jtareasticket


class Jseguimientostareas(models.Model):
    idseguimientotarea = models.AutoField(primary_key=True)
    tituloseguimientotarea = models.CharField(max_length=500, blank=True, null=True)
    detalleresolucion = models.CharField(max_length=1000, blank=True, null=True)
    status = models.BooleanField(default=True)
    fechacreacion = models.DateTimeField(auto_now_add=True, null=True)
    fechamodificacion = models.DateTimeField(auto_now=True, null=True)
    fecharegistro = models.DateTimeField(auto_now_add=True, null=True)
    idtarea = models.ForeignKey(
        Jtareasticket, models.DO_NOTHING, db_column="idtarea", blank=True, null=True
    )
    idusuario = models.ForeignKey(
        Jusuarios, models.DO_NOTHING, db_column='idusuario', blank=True, null=True
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
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=True, null=True)
    notification_type = models.CharField(max_length=200, blank=True, null=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'jnotificaciones'
        ordering = ['-created_at']
        
    objects = models.Manager()

    def __str__(self):
        return f"{self.idtarea} - {self.notification_type} - {self.created_at}"


# Database views  models for the app

class Vseguimientotareas(models.Model):
    idseguimientotarea = models.IntegerField(primary_key=True)
    tituloseguimientotarea = models.CharField()
    detalleresolucion = models.TextField()
    status = models.BooleanField()
    fechacreacion = models.DateTimeField()
    fechamodificacion = models.DateTimeField()
    fecharegistro = models.DateTimeField()
    idtarea = models.IntegerField()
    indicador = models.CharField()
    descripciontarea = models.CharField()
    tareaprincipal = models.IntegerField()
    idusuario = models.IntegerField()
    usuario = models.CharField()

    class Meta:
        managed = False
        db_table = 'vseguimientotareas'

    objects = models.Manager()
