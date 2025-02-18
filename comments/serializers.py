from rest_framework.serializers import (
    ModelSerializer, SerializerMethodField, PrimaryKeyRelatedField
)
from rest_framework.serializers import ValidationError
from .models import Comment
from contributors.models import Contributor
from issues.models import Issue


class CommentSerializer(ModelSerializer):
    author = SerializerMethodField()  # Récupère l'auteur dynamiquement
    issue = PrimaryKeyRelatedField(queryset=Issue.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'description', 'issue', 'author', 'created_time']
        extra_kwargs = {'created_time': {'read_only': True}}

    def get_author(self, obj):
        """ Renvoie l'ID du contributeur associé à l'auteur du commentaire """
        return obj.author.id if obj.author else None

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if self.context.get('exclude_issue', False):
            representation.pop('issue', None)

        return representation

    def create(self, validated_data):
        """ Associe automatiquement le contributeur
        correspondant à l'utilisateur """
        request = self.context.get("request")

        if not request or not request.user:
            raise ValidationError("Utilisateur non authentifié.")

        issue = validated_data.get("issue")
        user = request.user

        # Récupérer le projet via l'issue
        project = issue.project

        try:
            contributor = Contributor.objects.get(user=user, project=project)
        except Contributor.DoesNotExist:
            raise ValidationError(
                "L'utilisateur n'est pas un contributeur de ce projet."
            )

        validated_data["author"] = contributor  # Associer le bon contributeur
        return super().create(validated_data)
