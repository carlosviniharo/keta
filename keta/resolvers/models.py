from django.db import models

from users.models import Jusuarios
from tasks.models import Jtareasticket


# Create your models here.
class Jclasificacionesresoluciones(models.Model):
    idclasificacionresolucion = models.AutoField(primary_key=True)
    codigoclasificacionresolucion = models.CharField(
        max_length=4, blank=True, null=True
    )
    descripcionclasificacion = models.CharField(max_length=250, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "jclasificacionesresoluciones"
    
    objects = models.Manager()
    
    def __str__(self):
        return self.descripcionclasificacion


class Jtiporesoluciones(models.Model):
    idtiporesolucion = models.AutoField(primary_key=True)
    codigotiporesoulcion = models.CharField(max_length=4, blank=True, null=True)
    descripciontiporesolucion = models.CharField(max_length=250, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "jtiporesoluciones"

    objects = models.Manager()

    def __str__(self):
        return self.descripciontiporesolucion


class Jresoluciones(models.Model):
    idresolucion = models.AutoField(primary_key=True)
    numeroresolucion = models.CharField(max_length=100, blank=True, null=True)
    descripcionresolucion = models.TextField(blank=True, null=True)
    fecharesolucion = models.DateTimeField(auto_now_add=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)
    idclasificacionresolucion = models.ForeignKey(
        Jclasificacionesresoluciones,
        models.DO_NOTHING,
        db_column="idclasificacionresolucion",
        blank=True,
        null=True,
    )
    idtarea = models.ForeignKey(
        Jtareasticket, models.DO_NOTHING, db_column="idtarea", blank=True, null=True
    )
    idtiporesolucion = models.ForeignKey(
        Jtiporesoluciones,
        models.DO_NOTHING,
        db_column="idtiporesolucion",
        blank=True,
        null=True,
    )
    idusuariosolucion = models.ForeignKey(
        Jusuarios,
        models.DO_NOTHING,
        db_column="idusuariosolucion",
        null=False,
    )

    class Meta:
        db_table = "jresoluciones"
        unique_together = ("idtarea",)
    
    objects = models.Manager()

    def __str__(self):
        return self.descripcionresolucion


class Jvaloresresoluciones(models.Model):
    idvaloresresoluciones = models.AutoField(primary_key=True)
    monto = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    interesmonto = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True
    )
    totalmonto = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True
    )
    observacionmonto = models.CharField(max_length=500, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)
    idresolucion = models.ForeignKey(
        Jresoluciones,
        models.DO_NOTHING,
        db_column="idresolucion",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "jvaloresresoluciones"

    objects = models.Manager()

    def __str__(self):
        return self.totalmonto


class Vresoluciones(models.Model):
    idtarea = models.IntegerField(primary_key=True)
    idresolucion = models.IntegerField()
    fullname = models.CharField()
    emailcliente = models.CharField()
    agency = models.CharField()
    solver = models.CharField()
    descripciontiporesolucion = models.CharField()
    descripcionclasificacion = models.CharField()
    descripcionresolucion = models.CharField()
    tickettype = models.CharField()
    date = models.DateTimeField()
    
    class Meta:
        managed = False
        db_table = "vresoluciones"

    objects = models.Manager()
    
    def __str__(self):
        return self.idresolucion
    
    
    
    

