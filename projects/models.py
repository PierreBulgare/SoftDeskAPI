import uuid
from django.db import models
from authentication.models import User


class ProjectType(models.TextChoices):
    BACK_END = 'back-end', 'back-end'
    FRONT_END = 'front-end', 'front-end'
    IOS = 'iOS', 'iOS'
    ANDROID = 'Android', 'Android'


class Project(models.Model):
    """ Modèle de projet

    Un projet peut être de type back-end, front-end, iOS ou Android.

    Un projet est créé par un utilisateur (User)
    qui devient automatiquement un contributeur (Contributor).

    Un projet peut avoir plusieurs contributeurs.

    """

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
        )
    name = models.CharField(max_length=100)
    description = models.TextField()
    project_type = models.CharField(
        max_length=15, choices=ProjectType.choices
        )
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='created_projects'
        )
    created_time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        from contributors.models import Contributor
        if (self.author
            and not Contributor.objects.filter(
                user=self.author, project=self).exists()):
            Contributor.objects.create(user=self.author, project=self)

    def __str__(self):
        return self.name
