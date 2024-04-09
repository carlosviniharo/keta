from django.db import models
from django.db.models import Max, IntegerField, FloatField, ExpressionWrapper, F, Value, Func
from django.db.models.functions import Cast, Replace
from django.utils import timezone
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


class JtareasticketManager(models.Manager):

    use_in_migration = True

    def create(self, **kwargs):
        if kwargs.get('indicador') == "P":
            latest_main_ticket_code = self.filter(indicador="P").count()
            next_main_ticket_code = str(latest_main_ticket_code + 1) if latest_main_ticket_code else "1"
            kwargs['codigo'] = next_main_ticket_code
        else:
            main_task = kwargs.get('tareaprincipal')
            main_code = main_task.codigo
            latest_ticket_count = self.filter(indicador="A", tareaprincipal=main_task.idtarea).count()
            sub_ticket_number = latest_ticket_count + 1 if latest_ticket_count else 1
            kwargs['codigo'] = f"{main_code}.{sub_ticket_number}"

        # # Determine the value of the codigo field based on the indicador field
        # if kwargs.get('indicador') == "P":
        #     latest_main_ticket_code = (
        #         self.filter(indicador="P")
        #         .annotate(codigo_int=Cast('codigo', IntegerField()))
        #         .aggregate(Max('codigo_int'))['codigo_int__max']
        #     )
        #     next_main_ticket_code = str(int(latest_main_ticket_code) + 1) if latest_main_ticket_code else "1"
        #     kwargs['codigo'] = next_main_ticket_code
        # else:
        #     main_task = kwargs.get('tareaprincipal')
        #
        #     queryset = self.filter(indicador="A", tareaprincipal=main_task.idtarea)
        #     queryset = queryset.annotate(
        #         transformed_code=Cast(ExtractNumericPart('codigo'), IntegerField())
        #     )
        #
        #     # Filter to get the original value corresponding to the maximum transformed code
        #     latest_sub_ticket_code = queryset.filter(
        #         transformed_code=queryset.aggregate(Max('transformed_code'))['transformed_code__max']).values_list(
        #         'codigo', flat=True).first()
        #
        #     main_ticket_code = main_task.codigo if main_task else ""
        #     sub_ticket_number = int(latest_sub_ticket_code.split('.')[1]) + 1 if latest_sub_ticket_code else 1
        #     kwargs['codigo'] = f"{main_ticket_code}.{sub_ticket_number}"

        return super().create(**kwargs)


# class ExtractNumericPart(Func):
#     function = 'REGEXP_REPLACE'
#     template = r"%(function)s(%(expressions)s, '\.', '', 'g')"


class Jtareasticket(models.Model):
    idtarea = models.AutoField(primary_key=True)
    codigo = models.CharField(blank=True, null=True, unique=True)
    descripciontarea = models.CharField(max_length=500, blank=True, null=True)
    indicador = models.CharField(
        max_length=2, choices=[value for value in indicators], blank=True, null=True
    )
    fechaasignacion = models.DateTimeField(default=timezone.now)
    fechaentrega = models.DateTimeField(blank=True, null=True)
    fechaextension = models.DateTimeField(blank=True, null=True)
    fecharegistro = models.DateTimeField(auto_now_add=True, null=True)
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

    objects = JtareasticketManager()

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
        unique_together = ("idtarea", "descripcionarchivo", "mimetypearchivo")

    objects = models.Manager()

    def __str__(self):
        return self.nombrearchivo


# Views models
class Vtareaestadocolor(models.Model):
    tarea = models.IntegerField(primary_key=True)
    no_ticket = models.CharField()
    codigo = models.CharField()
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
    codigo = models.CharField()
    ticket_no = models.CharField()
    titulo_tarea = models.CharField()
    fecha_creacion = models.DateTimeField()
    fecha_asignacion = models.DateTimeField()
    fecha_extension = models.DateTimeField()
    sucursal = models.CharField()
    idcreador = models.IntegerField()
    creador = models.CharField()
    cedula = models.CharField()
    nombre_cliente = models.CharField()
    idtecnico = models.IntegerField()
    nombres_tecnico = models.CharField()
    cargo = models.CharField()
    departamento_usuario_asignado = models.CharField()
    sucursal_usuario_asignado = models.CharField()
    tipo_reclamo = models.CharField()
    tipo_comentario = models.CharField()
    prioridad = models.CharField()
    estado = models.CharField()
    fechaentrega = models.DateTimeField()
    fecharesolucion = models.DateTimeField()
    indicador = models.CharField()
    tareaprincipal = models.IntegerField()

    class Meta:
        managed = False
        db_table = "vtareas"

    objects = models.Manager()


class Vtareasemail(models.Model):
    idtarea = models.IntegerField(primary_key=True)
    codigo = models.CharField()
    fullname = models.CharField(max_length=255)
    emailcliente = models.EmailField()
    agency = models.CharField(max_length=255)
    tickettype = models.CharField(max_length=255)
    date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'vtareasemail'

    objects = models.Manager()


class Vemailnotificaciones(models.Model):
    tarea = models.IntegerField(primary_key=True)
    codigo = models.CharField()
    titulo_tarea = models.CharField()
    fecha_asignacion = models.DateTimeField()
    fechaentrega = models.DateTimeField()
    sucursal_ticket = models.CharField()
    idtecnico = models.IntegerField()
    nombres_tecnico = models.CharField()
    email_asignado = models.EmailField()
    cargo_asignado = models.CharField()
    departamento_usuario_asignado = models.CharField()
    sucursal_usuario_asignado = models.CharField()
    id_asignador = models.IntegerField()
    nombres_asignador = models.CharField()
    email_asignador = models.EmailField()
    cargo_asignador = models.CharField()
    tipo_reclamo = models.CharField()
    tipo_comentario = models.CharField()
    prioridad = models.CharField()
    estado = models.CharField()
    indicador = models.CharField(max_length=1)
    tareaprincipal = models.BooleanField()
    detalles_rechazo = models.CharField()
    max_fechacreacion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'vemailnotificaciones'

    objects = models.Manager()


class Vtareasrechazadas(models.Model):
    tarea = models.IntegerField(primary_key=True)
    codigo = models.CharField()
    ticket_no = models.CharField()
    titulo_tarea = models.CharField()
    fecha_asignacion = models.DateTimeField()
    fecha_entrega = models.DateTimeField()
    sucursal = models.CharField()
    cedula = models.CharField()
    nombre_cliente = models.CharField()
    idasignador = models.IntegerField()
    nombre_asignador = models.CharField()
    idasignado = models.IntegerField()
    nombre_asignado = models.CharField()
    cargo = models.CharField()
    departamento_usuario_asignado = models.CharField()
    sucursal_usuario_asignado = models.CharField()
    tipo_reclamo = models.CharField()
    tipo_comentario = models.CharField()
    prioridad = models.CharField()
    estado = models.CharField()
    indicador = models.CharField()
    tareaprincipal = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'vtareasrechazadas'

    objects = models.Manager()
