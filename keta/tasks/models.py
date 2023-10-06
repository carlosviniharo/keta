from django.db import models
from tickets.models import Jproblemas, Jprioridades
from users.models import Jusuarios

indicators = (("P", "Padre"), ("A", "Ayuda"))


class Jestados(models.Model):
    idestado = models.AutoField(primary_key=True)
    codigoestado = models.BigIntegerField(blank=True, null=True)
    descripcionestado = models.CharField(max_length=250, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "jestados"

    objects = models.Manager()

    def __str__(self):
        return self.descripcionestado


class Jtareasticket(models.Model):
    idtarea = models.AutoField(primary_key=True)
    descripciontarea = models.CharField(max_length=500, blank=True, null=True)
    indicador = models.CharField(
        max_length=2, choices=[value for value in indicators], blank=True, null=True
    )
    fechaasignacion = models.DateTimeField(auto_now_add=True, null=True)
    fechaentrega = models.DateTimeField(blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)
    fkidtarea = models.ForeignKey(
        "self", models.DO_NOTHING, db_column="fkidtarea", blank=True, null=True
    )
    idestado = models.ForeignKey(
        Jestados, models.DO_NOTHING, db_column="idestado", blank=True, null=True
    )
    idprioridad = models.ForeignKey(
        Jprioridades, models.DO_NOTHING, db_column="idprioridad", blank=True, null=True
    )
    idproblema = models.ForeignKey(
        Jproblemas, models.DO_NOTHING, db_column="idproblema", blank=True, null=True
    )
    idusuarioasignado = models.ForeignKey(
        Jusuarios,
        models.DO_NOTHING,
        db_column="idusuarioasignado",
        blank=True,
        null=True,
    )
    idusuarioqasigno = models.ForeignKey(
        Jusuarios,
        models.DO_NOTHING,
        db_column="idusuarioqasigno",
        related_name="jtareasticket_idusuarioqasigno_set",
        blank=True,
        null=True,
    )
    tareaprincipal = models.ForeignKey(
        "self",
        models.DO_NOTHING,
        db_column="tareaprincipal",
        related_name="jtareasticket_tareaprincipal_set",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "jtareasticket"

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
    idtarea = models.ForeignKey(
        Jtareasticket, models.DO_NOTHING, db_column="idtarea", blank=True, null=True
    )

    class Meta:
        db_table = "jestadotareas"

    objects = models.Manager()

    def __str__(self):
        return self.color


# TODO: The 'contenidoarchivo' field only supports small-sized files.
#  A cloud solution should be implemented so that instead of saving the base64 string,
#  it can store a link to where the file is stored.
class Jarchivos(models.Model):
    idarchivo = models.AutoField(primary_key=True)
    idtarea = models.ForeignKey(
        Jtareasticket,
        models.DO_NOTHING,
        db_column="idtarea"
    )
    idsubtarea = models.ForeignKey(
        Jtareasticket,
        models.DO_NOTHING,
        db_column="idsubtarea",
        related_name="jarchivos_idsubtarea_set",
        null=True,
    )
        
    nombrearchivo = models.CharField(max_length=500, blank=True, null=True)
    fechacarga = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    fecharegistro = models.DateTimeField(auto_now=True, blank=True, null=True)
    descripcionarchivo = models.CharField(max_length=1000)
    contenidoarchivo = models.TextField(null=True)
    mimetypearchivo = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "jarchivos"
        unique_together = ("idtarea", "nombrearchivo", "mimetypearchivo")

    objects = models.Manager()

    def __str__(self):
        return self.nombrearchivo


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
    titulo_tarea = models.CharField()
    fecha_asignacion = models.DateTimeField()
    sucursal = models.CharField()
    idcreador = models.IntegerField()
    creador = models.CharField()
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
    indicador = models.CharField()
    tareaprincipal = models.IntegerField()

    class Meta:
        managed = False
        db_table = "vtareas"

    objects = models.Manager()
