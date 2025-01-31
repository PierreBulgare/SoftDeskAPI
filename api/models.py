import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.core.validators import MinValueValidator


class Priority(models.TextChoices):
    LOW = 'LOW', 'LOW'
    MEDIUM = 'MEDIUM', 'MEDIUM'
    HIGH = 'HIGH', 'HIGH'


class Balise(models.TextChoices):
    BUG = 'BUG', 'BUG'
    FEATURE = 'FEATURE', 'FEATURE'
    TASK = 'TASK', 'TASK'


class Status(models.TextChoices):
    TO_DO = 'To Do', 'To Do'
    IN_PROGRESS = 'In Progress', 'In Progress'
    FINISHED = 'Finished', 'Finished'


class ProjectType(models.TextChoices):
    BACK_END = 'back-end', 'back-end'
    FRONT_END = 'front-end', 'front-end'
    IOS = 'iOS', 'iOS'
    ANDROID = 'Android', 'Android'


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
        extra_fields.setdefault("is_active", True)  # ✅ Assure-toi que le compte est actif

        return self.create_user(username, password, **extra_fields)



class User(AbstractBaseUser):
    """ Modèle d'utilisateur

    Un utilisateur peut être membre de plusieurs groupes et avoir plusieurs permissions.

    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=100, unique=True)
    age = models.PositiveIntegerField(null=False, blank=False, validators=[MinValueValidator(0)])
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)


    objects = UserManager()

    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username


class Contributor(models.Model):
    """ Modèle de contributeur

    Un utilisateur (User) contribue à un ou plusieurs projets
    
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contributions", null=False)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='contributors', null=False)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'project']

    def __str__(self):
        return f"{self.user.username} - Contributor"


class Project(models.Model):
    """ Modèle de projet

    Un projet peut être de type back-end, front-end, iOS ou Android.

    Un projet est créé par un utilisateur (User) qui devient automatiquement un contributeur (Contributor).

    Un projet peut avoir plusieurs contributeurs.
    
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    project_type = models.CharField(max_length=15, choices=ProjectType.choices)
    author = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_projects')
    created_time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.author and not Contributor.objects.filter(user=self.author, project=self).exists():
            Contributor.objects.create(user=self.author, project=self)

    def __str__(self):
        return self.name


class Issue(models.Model):
    """ Modèle de problème

    Un problème est créé par un contributeur (Contributor) dans un projet.

    Un problème peut être de priorité faible (LOW), moyenne (MEDIUM) ou élevée (HIGH).

    Un problème peut être un bug (BUG), une fonctionnalité (FEATURE) ou une tâche (TASK).

    Un problème peut être à faire, en cours ou terminé.

    Un problème peut avoir plusieurs commentaires.

    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    priority = models.CharField(max_length=15, choices=Priority.choices)
    balise = models.CharField(max_length=15, choices=Balise.choices)
    status = models.CharField(max_length=15, choices=Status.choices)
    author = models.ForeignKey('Contributor', on_delete=models.SET_NULL, null=True, blank=True, related_name='issues')
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='issues')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """ Modèle de commentaire

    Un commentaire est créé par un contributeur (Contributor) sur un problème (Issue).

    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    description = models.TextField()
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(Contributor, on_delete=models.SET_NULL, null=True, blank=True, related_name='comments')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Par {self.author.user.username} sur {self.issue.title}"
