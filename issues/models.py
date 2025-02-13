import uuid
from django.db import models
from contributors.models import Contributor
from projects.models import Project


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


class Issue(models.Model):
    """ Modèle de problème

    Un problème est créé par un contributeur (Contributor) dans un projet.

    Un problème peut être de priorité faible (LOW),
    moyenne (MEDIUM) ou élevée (HIGH).

    Un problème peut être un bug (BUG), une fonctionnalité (FEATURE)
    ou une tâche (TASK).

    Un problème peut être à faire, en cours ou terminé.

    Un problème peut avoir plusieurs commentaires.

    """

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
        )
    title = models.CharField(max_length=100)
    description = models.TextField()
    priority = models.CharField(max_length=15, choices=Priority.choices)
    balise = models.CharField(max_length=15, choices=Balise.choices)
    status = models.CharField(max_length=15, choices=Status.choices)
    author = models.ForeignKey(
        Contributor, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='issues'
        )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='issues'
        )
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
