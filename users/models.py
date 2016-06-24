from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class UserManager(BaseUserManager, models.Manager):

    def _create_user(self, username, email, password, is_staff,
                     is_superuser, **extra_fields):

        email = self.normalize_email(email)
        #if not email:
        #   raise ValueError('El email debe ser obligatorio')
        user = self.model(username=username, email=email, is_active=True,is_staff= is_staff, is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        return self._create_user(username, email, password, False,
                                 False, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        return self._create_user(username, email, password, True,
                                 True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50,unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='users',default='images/avatar.png')
    status = models.BooleanField(default=False)
    no_expediente = models.CharField(max_length=50, unique=True)

    objects = UserManager()

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        permissions = (
            ("permissions_estudiante", "Permiso para los Estudiantes"), ("permissions_administrador", "Permiso para los Administradores"),("permissions_maestros", "Permiso para los Maestros"),("permissions_biblioteca", "Permiso para Biblioteca"),("permissions_centro_computo", "Permiso para Centro Computo"),("permissions_contabilidad", "Permiso para Contabilidad"),
        )

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        full_name=self.first_name+" "+self.last_name
        return full_name

    def save_imag(self, *args, **kwargs):
        if self.image_url:
            import urllib, os
            from urlparse import urlparse
            filename = urlparse(self.image_url).path.split('/')[-1]
            urllib.urlretrieve(self.image_url, os.path.join(file_save_dir, filename))
            self.image = os.path.join(upload_path, filename)
            self.image_url = ''
            super(Product, self).save()