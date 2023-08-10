from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class Jcargos(models.Model):
    idcargo = models.AutoField(primary_key=True)
    codigocargo = models.CharField(max_length=10, blank=True, null=True)
    descripcioncargo = models.CharField(max_length=200, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jcargos'


class Jclasificacionesresoluciones(models.Model):
    idclasificacionresolucion = models.AutoField(primary_key=True)
    codigoclasificacionresolucion = models.CharField(max_length=4, blank=True, null=True)
    descripcionclasificacion = models.CharField(max_length=250, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jclasificacionesresoluciones'


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





class Jtiporesoluciones(models.Model):
    idtiporesolucion = models.AutoField(primary_key=True)
    codigotiporesoulcion = models.CharField(max_length=4, blank=True, null=True)
    descripciontiporesolucion = models.CharField(max_length=250, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'jtiporesoluciones'


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
