from rest_framework.serializers import (
    ModelSerializer, SerializerMethodField,
    PrimaryKeyRelatedField, ValidationError
)
from .models import Issue
from .models import Project
from comments.serializers import CommentSerializer
from contributors.models import Contributor


class IssueSerializer(ModelSerializer):
    project = PrimaryKeyRelatedField(queryset=Project.objects.all())
    author = SerializerMethodField()
    comments = SerializerMethodField()

    class Meta:
        model = Issue
        fields = [
            'id', 'title', 'description', 'priority',
            'balise', 'status', 'project', 'author',
            'comments', 'created_time']
        extra_kwargs = {'created_time': {'read_only': True}}

    def get_comments(self, obj):
        return CommentSerializer(obj.comments, many=True).data

    def get_author(self, obj):
        """ Renvoie l'ID du contributeur associé à l'auteur de l'issue """
        return obj.author.id if obj.author else None

    def create(self, validated_data):
        """ Associe automatiquement le contributeur
        correspondant à l'utilisateur """
        request = self.context.get("request")

        if not request or not request.user:
            raise ValidationError("Utilisateur non authentifié.")

        project = validated_data.get("project")
        user = request.user

        try:
            contributor = Contributor.objects.get(user=user, project=project)
        except Contributor.DoesNotExist:
            raise ValidationError(
                "L'utilisateur n'est pas un contributeur de ce projet.")

        validated_data["author"] = contributor
        return super().create(validated_data)
