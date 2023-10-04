from django.db import models
from encrypted_field import EncryptedField


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


class Vreportecobrosindebidos(models.Model):
    ticket = models.IntegerField(primary_key=True)
    nombredepartamento = models.CharField()
    nombre = models.CharField()
    apellido = models.CharField()
    identificacion = models.CharField()
    emailcliente = models.EmailField()
    date = models.DateTimeField()
    descripcionasunto = models.CharField()
    first_name = models.CharField()
    last_name = models.CharField()
    
    class Meta:
        managed = False
        db_table = 'vreportecobrosindebidos'
        
    objects = models.Manager()
    
    def __str__(self):
        return self.ticket


class Vreportereclamostarjeta(models.Model):
    ticket = models.IntegerField(primary_key=True)
    name = models.CharField()
    lastname = models.CharField()
    cardnumber = EncryptedField(hide_algorithm=True)
    detail = models.CharField()
    user = models.CharField()
    agency = models.CharField()
    identification = models.CharField()
    address = models.CharField()
    phone = models.CharField()
    date = models.DateTimeField()
    
    class Meta:
        
        managed = False
        db_table = "vreportereclamostarjeta"
        
    objects = models.Manager()
    
    def __str__(self):
        return self.ticket


class Vreportereclamosgenerales(models.Model):
    ticket = models.IntegerField(primary_key=True)
    comentario = models.CharField()
    agencia = models.CharField()
    departamento = models.CharField()
    usuario = models.CharField()
    servicio = models.CharField()
    detail = models.CharField()
    name = models.CharField()
    phone = models.CharField()
    email = models.EmailField()
    identification = models.CharField()
    date = models.DateTimeField()
    
    class Meta:
        managed = False
        db_table = "vreportereclamosgenerales"
    
    objects = models.Manager()
    
    def __str__(self):
        return self.ticket
