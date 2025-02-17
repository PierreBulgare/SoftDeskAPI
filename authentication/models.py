from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinValueValidator
from datetime import date


class UserManager(BaseUserManager):
    """ Manager personnalisé pour le modèle User """

    def create_user(self, username, password=None, **extra_fields):
        """ Crée et retourne un utilisateur normal """
        if not username:
            raise ValueError("Le champ 'username' est obligatoire")

        if not password:
            raise ValueError("Le champ 'password' est obligatoire")

        user = self.model(username=username, **extra_fields)
        user.set_password(password)  # Hashage du mot de passe
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        """ Crée et retourne un superutilisateur """
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser):
    """ Modèle d'utilisateur

    Un utilisateur peut être membre de plusieurs groupes
    et avoir plusieurs permissions.

    """

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
        )
    username = models.CharField(max_length=100, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username
    
    @property
    def age(self):
        """ Retourne l'âge de l'utilisateur """
        if self.birth_date:
            return date.today().year - self.birth_date.year
        return None
