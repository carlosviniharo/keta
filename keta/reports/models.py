from django.db import models


# Create your models here.
class Vcobrosindebios(models.Model):
    ticket = models.IntegerField(primary_key=True)
    tipoidentificacionsujeto = models.CharField()
    identificacionsujeto = models.CharField()
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
    
    def __str__(self):
        return f"Ticket number {self.ticket}"
