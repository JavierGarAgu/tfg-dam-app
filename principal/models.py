from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# ------------------------
# 1. Usuario
# ------------------------

class UsuarioManager(BaseUserManager):
    def create_user(self, usuario, contraseña=None, **extra_fields):
        if not usuario:
            raise ValueError('El usuario debe tener un nombre')
        usuario = self.model(usuario=usuario, **extra_fields)
        if contraseña:
            usuario.set_password(contraseña)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, usuario, contraseña=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(usuario, contraseña, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    usuario = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    password = models.CharField(max_length=100)

    USERNAME_FIELD = 'usuario'
    REQUIRED_FIELDS = ['email']

    objects = UsuarioManager()

    class Meta:
        db_table = 'usuarios'

    def __str__(self):
        return f"Usuario(id={self.id}, usuario='{self.usuario}', email='{self.email}', staff={self.is_staff}, superuser={self.is_superuser}, activo={self.is_active})"

# ------------------------
# 2. Registro
# ------------------------

class Registro(models.Model):
    TIPO_CHOICES = [
        ('mantenimiento', 'Mantenimiento'),
        ('averia', 'Avería'),
        ('consumo', 'Consumo'),
    ]

    tipo_registro = models.CharField(max_length=20, choices=TIPO_CHOICES)
    kilometraje = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    detalles = models.TextField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='usuario_id')

    class Meta:
        db_table = 'datos'

    def __str__(self):
        return f"Registro(id={self.id}, tipo='{self.tipo_registro}', km={self.kilometraje}, usuario='{self.usuario.usuario}')"
