from django.db import models


class Jcanalesrecepciones(models.Model):
    idcanalrecepcion = models.AutoField(primary_key=True)
    codigocanalrecepcion = models.CharField(max_length=2, blank=True, null=True)
    descripcioncanalrecepcion = models.CharField(max_length=250)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jcanalesrecepciones'