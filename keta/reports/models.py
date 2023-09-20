from django.db import models


# Create your models here.
class Vcobrosindebios(models.Model):
    tipoidentificacionsujeto = models.CharField()
    identificacionsujeto = models.CharField(primary_key=True)
    nomapellidonomrazonsocial = models.CharField()
    canalrecepcion = models.CharField()
    fecharecepcion = models.DateTimeField()
    tipotransaccion = models.CharField()
    concepto = models.CharField()
    estadoreclamo = models.CharField()
    fecharespuesta = models.DateTimeField()
    tiporesolucion = models.CharField()
    montorestituido = models.FloatField()
    interesmonto = models.FloatField()
    totalrestituido = models.FloatField()

    class Meta:
        managed = False
        db_table = "vcobrosindebios"

    objects = models.Manager()
