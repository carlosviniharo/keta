

from django.db import models

from users.models import Jpersonas, Jusuarios, Jsucursales
from .utils.helper import generate_ticket_id


class Jcanalesrecepciones(models.Model):
    idcanalrecepcion = models.AutoField(primary_key=True)
    codigocanalrecepcion = models.CharField(max_length=2, blank=True, null=True)
    descripcioncanalrecepcion = models.CharField(max_length=250)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jcanalesrecepciones'


class Jclasestarjetas(models.Model):
    idclasetarjeta = models.AutoField(primary_key=True)
    codigoclasetarjeta = models.CharField(max_length=2, blank=True, null=True)
    descripcionclasetarjeta = models.CharField(max_length=100, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jclasestarjetas'


class Jtiposproductos(models.Model):
    idtipoproducto = models.AutoField(primary_key=True)
    codigotipoproducto = models.CharField(max_length=4, blank=True, null=True)
    descripciontipoproducto = models.CharField(max_length=250, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jtiposproductos'


class Jconceptos(models.Model):
    idconcepto = models.AutoField(primary_key=True)
    idtipoproducto = models.ForeignKey(Jtiposproductos, models.DO_NOTHING, db_column='idtipoproducto', blank=True, null=True)
    codigoconcepto = models.CharField(max_length=4, blank=True, null=True)
    descripcionconcepto = models.TextField(blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jconceptos'


class Jmarcastarjetas(models.Model):
    idmarcatarjeta = models.AutoField(primary_key=True)
    codigomarcatarjeta = models.CharField(max_length=2, blank=True, null=True)
    descripcionmarcatarjeta = models.CharField(max_length=100, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jmarcastarjetas'


class Jprioridades(models.Model):
    idprioridad = models.AutoField(primary_key=True)
    codigoprioridad = models.CharField(max_length=2, blank=True, null=True)
    descripcionprioridad = models.CharField(max_length=50, blank=True, null=True)
    duracionprioridad = models.CharField(max_length=100, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jprioridades'


class Jtipostarjetas(models.Model):
    idtipotarjeta = models.AutoField(primary_key=True)
    codigotipotarjeta = models.CharField(max_length=4, blank=True, null=True)
    descripciontipotarjeta = models.CharField(max_length=100, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jtipostarjetas'


class Jtarjetas(models.Model):
    idtarjeta = models.AutoField(primary_key=True)
    idmarcatarjeta = models.ForeignKey(Jmarcastarjetas, models.DO_NOTHING, db_column='idmarcatarjeta', blank=True, null=True)
    idtipotarjeta = models.ForeignKey(Jtipostarjetas, models.DO_NOTHING, db_column='idtipotarjeta', blank=True, null=True)
    idclasetarjeta = models.ForeignKey(Jclasestarjetas, models.DO_NOTHING, db_column='idclasetarjeta', blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jtarjetas'


class Jtiposcomentarios(models.Model):
    idtipocomentario = models.AutoField(primary_key=True)
    codigotipocomentario = models.CharField(max_length=3, blank=True, null=True)
    descripciontipocomentario = models.CharField(max_length=250, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jtiposcomentarios'


class Jtickettipos(models.Model):
    idtipoticket = models.AutoField(primary_key=True)
    descripciontipoticket = models.CharField(max_length=250, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jtickettipos'


class Jtipostransacciones(models.Model):
    idtipotransaccion = models.AutoField(primary_key=True)
    codigotipotransaccion = models.CharField(max_length=4, blank=True, null=True)
    descripciontipotransaccion = models.CharField(max_length=250, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jtipostransacciones'


class JproblemasManager(models.Manager):
    pass


class Jproblemas(models.Model):
    idproblema = models.AutoField(primary_key=True)
    idusuario = models.ForeignKey(Jusuarios, models.DO_NOTHING, db_column='idusuario', blank=True, null=True)
    fechacreacion = models.DateTimeField(blank=True, null=True)
    numeroticket = models.CharField(max_length=100, blank=True, null=True)
    idtipotransaccion = models.ForeignKey(Jtipostransacciones, models.DO_NOTHING, db_column='idtipotransaccion', blank=True, null=True)
    idtipocomentario = models.ForeignKey(Jtiposcomentarios, models.DO_NOTHING, db_column='idtipocomentario', blank=True, null=True)
    idcanalrecepcion = models.ForeignKey(Jcanalesrecepciones, models.DO_NOTHING, db_column='idcanalrecepcion', blank=True, null=True)
    idpersona = models.ForeignKey(Jpersonas, models.DO_NOTHING, db_column='idpersona', blank=True, null=True)
    idtipoticket = models.ForeignKey(Jtickettipos, models.DO_NOTHING, db_column='idtipoticket', blank=True, null=True)
    idconcepto = models.ForeignKey(Jconceptos, models.DO_NOTHING, db_column='idconcepto', blank=True, null=True)
    descripcionasunto = models.TextField(blank=True, null=True)
    monto = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    idtarjeta = models.ForeignKey(Jtarjetas, models.DO_NOTHING, db_column='idtarjeta', blank=True, null=True)
    idprioridad = models.ForeignKey(Jprioridades, models.DO_NOTHING, db_column='idprioridad', blank=True, null=True)
    idsucursal = models.ForeignKey(Jsucursales, models.DO_NOTHING, db_column='idsucursal', blank=True, null=True)
    archivo = models.CharField(max_length=500, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jproblemas'

    def save(self, *args, **kwargs):
        if len(self.numeroticket.strip(" ")) == 0:
            self.numeroticket = generate_ticket_id()

        super(Jproblemas, self).save(*args, **kwargs)

    def __str__(self):
        return self.numeroticket #"{} - {}".format(self.idtipoticket, self.numeroticket)

