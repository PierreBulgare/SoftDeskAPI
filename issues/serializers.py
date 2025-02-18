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
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request', None)

        # Supprime 'comments' dans la vue (liste) des issues
        if request and not request.parser_context.get("kwargs", {}).get("pk"):
            representation.pop('comments', None)

        if self.context.get('exclude_comments', False):
            representation.pop('comments', None)

        if self.context.get('exclude_project', False):
            representation.pop('project', None)

        # Ajouter les commentaires uniquement dans la vue détaillée de l'issue
        if (request
            and request.parser_context
            and 'pk' in request.parser_context['kwargs']):
            representation['comments'] = CommentSerializer(
                instance.comments.all(),
                many=True,
                context={**self.context, 'exclude_issue': True}
            ).data

        return representation

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
