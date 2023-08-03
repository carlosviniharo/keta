from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class Jcanalesrecepciones(models.Model):
    idcanalrecepcion = models.AutoField(primary_key=True)
    codigocanalrecepcion = models.CharField(max_length=2, blank=True, null=True)
    descripcioncanalrecepcion = models.CharField(max_length=250)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jcanalesrecepciones'


class Jcargos(models.Model):
    idcargo = models.AutoField(primary_key=True)
    codigocargo = models.CharField(max_length=10, blank=True, null=True)
    descripcioncargo = models.CharField(max_length=200, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jcargos'


class Jclasestarjetas(models.Model):
    idclasetarjeta = models.AutoField(primary_key=True)
    codigoclasetarjeta = models.CharField(max_length=2, blank=True, null=True)
    descripcionclasetarjeta = models.CharField(max_length=100, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jclasestarjetas'


class Jclasificacionesresoluciones(models.Model):
    idclasificacionresolucion = models.AutoField(primary_key=True)
    codigoclasificacionresolucion = models.CharField(max_length=4, blank=True, null=True)
    descripcionclasificacion = models.CharField(max_length=250, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jclasificacionesresoluciones'


class Jconceptos(models.Model):
    idconcepto = models.AutoField(primary_key=True)
    idtipoproducto = models.ForeignKey('Jtiposproductos', models.DO_NOTHING, db_column='idtipoproducto', blank=True, null=True)
    codigoconcepto = models.CharField(max_length=4, blank=True, null=True)
    descripcionconcepto = models.TextField(blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jconceptos'


class Jcorporaciones(models.Model):
    idcorporacion = models.AutoField(primary_key=True)
    idpais = models.ForeignKey('Jgeografia', models.DO_NOTHING, db_column='idpais', blank=True, null=True)
    nombrecorporacion = models.CharField(max_length=200, blank=True, null=True)
    descripcioncorporacion = models.CharField(max_length=500, blank=True, null=True)
    representantelegal = models.CharField(max_length=200, blank=True, null=True)
    ruc = models.CharField(blank=True, null=True)
    direccioncorporacion = models.CharField(max_length=200, blank=True, null=True)
    telefonocorporacion = models.CharField(blank=True, null=True)
    status = models.BooleanField(blank=True, null=True)
    fechacreacion = models.DateTimeField(blank=True, null=True)
    fechamodificacion = models.DateTimeField(blank=True, null=True)
    ipcreacion = models.CharField(max_length=50, blank=True, null=True)
    ipmodificacion = models.CharField(max_length=50, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jcorporaciones'


class Jdepartamentos(models.Model):
    iddepartamento = models.AutoField(primary_key=True)
    idsucursal = models.ForeignKey('Jsucursales', models.DO_NOTHING, db_column='idsucursal', blank=True, null=True)
    codigodepartamento = models.CharField(max_length=2, blank=True, null=True)
    nombredepartamento = models.CharField(max_length=200, blank=True, null=True)
    status = models.BooleanField(blank=True, null=True)
    descripciondepartamento = models.CharField(max_length=500, blank=True, null=True)
    fechacreacion = models.DateTimeField(blank=True, null=True)
    fechamodificacion = models.DateTimeField(blank=True, null=True)
    ipcreacion = models.CharField(max_length=50, blank=True, null=True)
    ipmodificacion = models.CharField(max_length=50, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jdepartamentos'


class Jestados(models.Model):
    idestado = models.AutoField(primary_key=True)
    codigoestado = models.BigIntegerField(blank=True, null=True)
    descripcionestado = models.CharField(max_length=250, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jestados'


class Jestadotareas(models.Model):
    idestadotarea = models.AutoField(primary_key=True)
    idtarea = models.ForeignKey('Jtareasticket', models.DO_NOTHING, db_column='idtarea', blank=True, null=True)
    diaoptimo = models.BigIntegerField(blank=True, null=True)
    diarequerido = models.BigIntegerField(blank=True, null=True)
    color = models.CharField(max_length=100, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jestadotareas'


class Jgeneros(models.Model):
    idgenero = models.AutoField(primary_key=True)
    codigogenero = models.CharField(max_length=2, blank=True, null=True)
    descripciongenero = models.CharField(max_length=50, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jgeneros'


class Jgeografia(models.Model):
    idgeografia = models.AutoField(primary_key=True)
    fkidgeografia = models.ForeignKey('self', models.DO_NOTHING, db_column='fkidgeografia', blank=True, null=True)
    codigogeografia = models.CharField(max_length=2, blank=True, null=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    nivel = models.BigIntegerField(blank=True, null=True)
    status = models.BooleanField(blank=True, null=True)
    fechacreacion = models.DateTimeField(blank=True, null=True)
    fechamodificacion = models.DateTimeField(blank=True, null=True)
    ipcreacion = models.CharField(max_length=50, blank=True, null=True)
    ipmodificacion = models.CharField(max_length=50, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jgeografia'


class Jmarcastarjetas(models.Model):
    idmarcatarjeta = models.AutoField(primary_key=True)
    codigomarcatarjeta = models.CharField(max_length=2, blank=True, null=True)
    descripcionmarcatarjeta = models.CharField(max_length=100, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jmarcastarjetas'


class Jpersonas(models.Model):
    idpersona = models.AutoField(primary_key=True)
    idgenero = models.ForeignKey(Jgeneros, models.DO_NOTHING, db_column='idgenero', blank=True, null=True)
    idtipoidentificacion = models.ForeignKey('Jtiposidentificaciones', models.DO_NOTHING, db_column='idtipoidentificacion', blank=True, null=True)
    idtipopersona = models.ForeignKey('Jtipospersonas', models.DO_NOTHING, db_column='idtipopersona', blank=True, null=True)
    identificacion = models.CharField(max_length=10, blank=True, unique=True)
    nombre = models.CharField(max_length=250, blank=True, null=True)
    apellido = models.CharField(max_length=250, blank=True, null=True)
    emailcliente = models.CharField(max_length=100, blank=True, null=True)
    celular = models.CharField(max_length=10, blank=True, null=True)
    telefono = models.CharField(max_length=9, blank=True, null=True)
    direccion = models.CharField(max_length=500, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'jpersonas'


class Jprioridades(models.Model):
    idprioridad = models.AutoField(primary_key=True)
    codigoprioridad = models.CharField(max_length=2, blank=True, null=True)
    descripcionprioridad = models.CharField(max_length=50, blank=True, null=True)
    duracionprioridad = models.CharField(max_length=100, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jprioridades'


class Jproblemas(models.Model):
    idproblema = models.AutoField(primary_key=True)
    idusuario = models.ForeignKey('Jusuarios', models.DO_NOTHING, db_column='idusuario', blank=True, null=True)
    fechacreacion = models.DateTimeField(blank=True, null=True)
    numeroticket = models.CharField(max_length=100, blank=True, null=True)
    idtipotransaccion = models.ForeignKey('Jtipostransacciones', models.DO_NOTHING, db_column='idtipotransaccion', blank=True, null=True)
    idtipocomentario = models.ForeignKey('Jtiposcomentarios', models.DO_NOTHING, db_column='idtipocomentario', blank=True, null=True)
    idcanalrecepcion = models.ForeignKey(Jcanalesrecepciones, models.DO_NOTHING, db_column='idcanalrecepcion', blank=True, null=True)
    idpersona = models.ForeignKey(Jpersonas, models.DO_NOTHING, db_column='idpersona', blank=True, null=True)
    idtipoticket = models.ForeignKey('Jtickettipos', models.DO_NOTHING, db_column='idtipoticket', blank=True, null=True)
    idconcepto = models.ForeignKey(Jconceptos, models.DO_NOTHING, db_column='idconcepto', blank=True, null=True)
    descripcionasunto = models.TextField(blank=True, null=True)
    monto = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    idtarjeta = models.ForeignKey('Jtarjetas', models.DO_NOTHING, db_column='idtarjeta', blank=True, null=True)
    idprioridad = models.ForeignKey(Jprioridades, models.DO_NOTHING, db_column='idprioridad', blank=True, null=True)
    idsucursal = models.ForeignKey('Jsucursales', models.DO_NOTHING, db_column='idsucursal', blank=True, null=True)
    archivo = models.CharField(max_length=500, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jproblemas'


class Jresoluciones(models.Model):
    idresolucion = models.AutoField(primary_key=True)
    numeroresolucion = models.CharField(max_length=100, blank=True, null=True)
    idtarea = models.ForeignKey('Jtareasticket', models.DO_NOTHING, db_column='idtarea', blank=True, null=True)
    idtiporesolucion = models.ForeignKey('Jtiporesoluciones', models.DO_NOTHING, db_column='idtiporesolucion', blank=True, null=True)
    idclasificacionresolucion = models.ForeignKey(Jclasificacionesresoluciones, models.DO_NOTHING, db_column='idclasificacionresolucion', blank=True, null=True)
    descripcionresolucion = models.TextField(blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jresoluciones'


class Jroles(models.Model):
    idrol = models.AutoField(primary_key=True)
    nombrerol = models.CharField(max_length=100, blank=True, null=True)
    descripcionrol = models.CharField(max_length=100, blank=True, null=True)
    status = models.BooleanField(blank=True, null=True)
    fechacreacion = models.DateTimeField(blank=True, null=True)
    fechamodificacion = models.DateTimeField(blank=True, null=True)
    ipcreacion = models.CharField(max_length=50, blank=True, null=True)
    ipmodificacion = models.CharField(max_length=50, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jroles'


class Jseguimientostareas(models.Model):
    idseguimientotarea = models.AutoField(primary_key=True)
    idtarea = models.ForeignKey('Jtareasticket', models.DO_NOTHING, db_column='idtarea', blank=True, null=True)
    detalleresolucion = models.CharField(max_length=500, blank=True, null=True)
    status = models.BooleanField(blank=True, null=True)
    fechacreacion = models.DateTimeField(blank=True, null=True)
    fechamodificacion = models.DateTimeField(blank=True, null=True)
    archivo = models.CharField(max_length=500, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jseguimientostareas'


class Jsucursales(models.Model):
    idsucursal = models.AutoField(primary_key=True)
    idpais = models.ForeignKey(Jgeografia, models.DO_NOTHING, db_column='idpais', blank=True, null=True)
    idcorporacion = models.ForeignKey(Jcorporaciones, models.DO_NOTHING, db_column='idcorporacion', blank=True, null=True)
    codigosucursal = models.CharField(max_length=2, blank=True, null=True)
    nombresucursal = models.CharField(max_length=200, blank=True, null=True)
    descripcionsucursal = models.CharField(max_length=500, blank=True, null=True)
    direccionsucursal = models.CharField(max_length=200, blank=True, null=True)
    telefonosucursal = models.CharField(blank=True, null=True)
    status = models.BooleanField(blank=True, null=True)
    fechacreacion = models.DateTimeField(blank=True, null=True)
    fechamodificacion = models.DateTimeField(blank=True, null=True)
    ipcreacion = models.CharField(max_length=50, blank=True, null=True)
    ipmodificacion = models.CharField(max_length=50, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jsucursales'


class Jtareasticket(models.Model):
    idtarea = models.AutoField(primary_key=True)
    fkidtarea = models.ForeignKey('self', models.DO_NOTHING, db_column='fkidtarea', blank=True, null=True)
    idproblema = models.ForeignKey(Jproblemas, models.DO_NOTHING, db_column='idproblema', blank=True, null=True)
    idusuarioqasigno = models.ForeignKey('Jusuarios', models.DO_NOTHING, db_column='idusuarioqasigno', blank=True, null=True)
    idusuarioasignado = models.ForeignKey('Jusuarios', models.DO_NOTHING, db_column='idusuarioasignado', related_name='jtareasticket_idusuarioasignado_set', blank=True, null=True)
    descripciontarea = models.CharField(max_length=500, blank=True, null=True)
    tareaprincipal = models.ForeignKey('self', models.DO_NOTHING, db_column='tareaprincipal', related_name='jtareasticket_tareaprincipal_set', blank=True, null=True)
    indicador = models.CharField(max_length=2, blank=True, null=True)
    idprioridad = models.ForeignKey(Jprioridades, models.DO_NOTHING, db_column='idprioridad', blank=True, null=True)
    idestado = models.ForeignKey(Jestados, models.DO_NOTHING, db_column='idestado', blank=True, null=True)
    fechaasignacion = models.DateTimeField(blank=True, null=True)
    fechaentrega = models.DateTimeField(blank=True, null=True)
    archivo = models.CharField(max_length=500, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jtareasticket'


class Jtarjetas(models.Model):
    idtarjeta = models.AutoField(primary_key=True)
    idmarcatarjeta = models.ForeignKey(Jmarcastarjetas, models.DO_NOTHING, db_column='idmarcatarjeta', blank=True, null=True)
    idtipotarjeta = models.ForeignKey('Jtipostarjetas', models.DO_NOTHING, db_column='idtipotarjeta', blank=True, null=True)
    idclasetarjeta = models.ForeignKey(Jclasestarjetas, models.DO_NOTHING, db_column='idclasetarjeta', blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jtarjetas'


class Jtickettipos(models.Model):
    idtipoticket = models.AutoField(primary_key=True)
    descripciontipoticket = models.CharField(max_length=250, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jtickettipos'


class Jtiporesoluciones(models.Model):
    idtiporesolucion = models.AutoField(primary_key=True)
    codigotiporesoulcion = models.CharField(max_length=4, blank=True, null=True)
    descripciontiporesolucion = models.CharField(max_length=250, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jtiporesoluciones'


class Jtiposcomentarios(models.Model):
    idtipocomentario = models.AutoField(primary_key=True)
    codigotipocomentario = models.CharField(max_length=3, blank=True, null=True)
    descripciontipocomentario = models.CharField(max_length=250, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jtiposcomentarios'


class Jtiposidentificaciones(models.Model):
    idtipoidentificacion = models.AutoField(primary_key=True)
    codigotipoidentificacion = models.CharField(max_length=2, blank=True, null=True)
    descripciontipoidentificacion = models.CharField(max_length=50, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jtiposidentificaciones'


class Jtipospersonas(models.Model):
    idtipopersona = models.AutoField(primary_key=True)
    codigotipopersona = models.CharField(blank=True, null=True)
    descripciontipopersona = models.CharField(max_length=50, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jtipospersonas'


class Jtiposproductos(models.Model):
    idtipoproducto = models.AutoField(primary_key=True)
    codigotipoproducto = models.CharField(max_length=4, blank=True, null=True)
    descripciontipoproducto = models.CharField(max_length=250, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jtiposproductos'


class Jtipostarjetas(models.Model):
    idtipotarjeta = models.AutoField(primary_key=True)
    codigotipotarjeta = models.CharField(max_length=4, blank=True, null=True)
    descripciontipotarjeta = models.CharField(max_length=100, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jtipostarjetas'


class Jtipostransacciones(models.Model):
    idtipotransaccion = models.AutoField(primary_key=True)
    codigotipotransaccion = models.CharField(max_length=4, blank=True, null=True)
    descripciontipotransaccion = models.CharField(max_length=250, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jtipostransacciones'


class Jvaloresresoluciones(models.Model):
    idvaloresresoluciones = models.AutoField(primary_key=True)
    idresolucion = models.ForeignKey(Jresoluciones, models.DO_NOTHING, db_column='idresolucion', blank=True, null=True)
    monto = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    interesmonto = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    totalmonto = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    observacionmonto = models.CharField(max_length=500, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jvaloresresoluciones'


class JusuariosManager(BaseUserManager):
    use_in_migration = True

    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is Required')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, ** extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')

        return self._create_user(email, password, **extra_fields)


class Jusuarios(AbstractUser):
    idusuario = models.AutoField(primary_key=True)
    idrol = models.ForeignKey(Jroles, models.DO_NOTHING, db_column='idrol', blank=True, null=True)
    idpersona = models.ForeignKey(Jpersonas, models.DO_NOTHING, db_column='idpersona', blank=True, null=True)
    iddepartamento = models.ForeignKey(Jdepartamentos, models.DO_NOTHING, db_column='iddepartamento', blank=True, null=True)
    idcargo = models.ForeignKey(Jcargos, models.DO_NOTHING, db_column='idcargo', blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True, default=True)
    direccionmac = models.CharField(max_length=100, blank=True, null=True)
    date_joined = models.DateTimeField(blank=True, null=True)
    fechamodificacion = models.DateTimeField(blank=True, null=True)
    ipcreacion = models.CharField(max_length=50, blank=True, null=True)
    ipmodificacion = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, unique=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    is_staff = models.BooleanField(blank=True, null=True, default=True)
    is_superuser = models.BooleanField(blank=True, null=True, default=False)
    last_login = models.DateTimeField(blank=True, null=True)
    password = models.CharField(max_length=100)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    objects = JusuariosManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'jusuarios'

    def __str__(self):
        return self.username
