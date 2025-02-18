import uuid
from django.db import models
from authentication.models import User
from projects.models import Project


class Contributor(models.Model):
    """ Modèle de contributeur

    Un utilisateur (User) contribue à un ou plusieurs projets

    """
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
        )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="contributions", null=False
        )

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE,
        related_name='contributors', null=False
        )
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'project']

    def __str__(self):
        return f"{self.user.username} - Contributor"
