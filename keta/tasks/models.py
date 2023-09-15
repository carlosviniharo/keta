from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models
from tickets.models import Jproblemas, Jprioridades
from users.models import Jusuarios

indicators = (
    ("P", "Padre"),
    ("A", "Ayuda")
)


class Jestados(models.Model):
    idestado = models.AutoField(primary_key=True)
    codigoestado = models.BigIntegerField(blank=True, null=True)
    descripcionestado = models.CharField(max_length=250, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'jestados'

    objects = models.Manager()

    def __str__(self):
        return self.descripcionestado


# TODO tests a example of store several base64 strings in archivo
class Jtareasticket(models.Model):
    idtarea = models.AutoField(primary_key=True)
    descripciontarea = models.CharField(max_length=500, blank=True, null=True)
    indicador = models.CharField(max_length=2, choices=[value for value in indicators], blank=True, null=True)
    fechaasignacion = models.DateTimeField(auto_now=True, null=True)
    fechaentrega = models.DateTimeField(blank=True, null=True)
    archivo = models.TextField(blank=True, null=True)
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

    objects = models.Manager()

    def __str__(self):
        return f"{self.idtarea} - {self.indicador} - {self.idusuarioasignado}"


class Jestadotareas(models.Model):
    idestadotarea = models.AutoField(primary_key=True)
    tiempooptimo = models.DateTimeField(blank=True, null=True)
    tiemporequerido = models.DateTimeField(blank=True, null=True)
    tiempoiniciocolor = models.DateTimeField(blank=True, null=True)
    tiempocolor = models.DateTimeField(blank=True, null=True)
    color = models.CharField(max_length=100, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)
    idtarea = models.ForeignKey(Jtareasticket, models.DO_NOTHING, db_column='idtarea', blank=True, null=True)

    class Meta:
        db_table = 'jestadotareas'

    objects = models.Manager()

    def __str__(self):
        return self.color


# Views models
class Vtareaestadocolor(models.Model):
    tarea = models.IntegerField(primary_key=True)
    no_ticket = models.CharField()
    color = models.CharField(max_length=100)
    tiempo_inicial_del_color = models.DateTimeField()
    tiempo_final_del_color = models.DateTimeField()
    fechaasignacion = models.DateTimeField()
    tiempooptimo = models.DateTimeField()
    tiemporequerido = models.DateTimeField()
    idproblema = models.IntegerField()
    id_asignador = models.IntegerField()
    usuario_asignador = models.EmailField()
    id_asignado = models.IntegerField()
    usuario_asignado = models.EmailField()
    titulo_ticket = models.CharField()
    agencia = models.CharField()
    client = models.CharField()
    descripcionasunto = models.CharField()
    descripcionprioridad = models.CharField(max_length=50)
    descripciontipoticket = models.CharField()
    descripciontipocomentario = models.DateTimeField()
    descripcionestado = models.CharField(max_length=250)
    now_state = models.BooleanField()

    class Meta:
        managed = False
        db_table = "vtareaestadocolor"

    objects = models.Manager()


class Vtareas(models.Model):
    tarea = models.IntegerField(primary_key=True)
    ticket_no = models.CharField()
    fecha_asignacion = models.DateTimeField()
    sucursal = models.CharField()
    nombre_cliente = models.CharField()
    apellido_cliente = models.CharField()
    nombres_tecnico = models.CharField()
    apellidos_tecnico = models.CharField()
    cargo = models.CharField()
    departamento_usuario_asignado = models.CharField()
    sucursal_usuario_asignado = models.CharField()
    tipo_reclamo = models.CharField()
    tipo_comentario = models.CharField()
    prioridad = models.CharField()
    estado = models.CharField()
    fechaentrega = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "vtareas"

    objects = models.Manager()
