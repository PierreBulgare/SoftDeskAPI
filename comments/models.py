import uuid
from django.db import models
from contributors.models import Contributor
from issues.models import Issue

class Comment(models.Model):
    """ Modèle de commentaire

    Un commentaire est créé par un contributeur (Contributor)
    sur un problème (Issue).

    """

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
        )
    description = models.TextField()
    issue = models.ForeignKey(
        Issue, on_delete=models.CASCADE, related_name='comments'
        )
    author = models.ForeignKey(
        Contributor, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='comments'
        )
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Par {self.author.user.username} sur {self.issue.title}"
