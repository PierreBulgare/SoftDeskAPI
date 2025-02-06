from rest_framework.serializers import (
    ModelSerializer, SerializerMethodField,
    CharField, PrimaryKeyRelatedField, ValidationError
)
from .models import User, Contributor, Project, Issue, Comment


class UserSerializer(ModelSerializer):
    password = CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'age',
                  'can_be_contacted', 'can_data_be_shared', 'created_time']
        extra_kwargs = {'created_time': {'read_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ContributorSerializer(ModelSerializer):
    user = PrimaryKeyRelatedField(queryset=User.objects.all())
    project = PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project', 'created_time']
        extra_kwargs = {'created_time': {'read_only': True}}


class ProjectSerializer(ModelSerializer):
    author = PrimaryKeyRelatedField(queryset=User.objects.all())
    contributors = ContributorSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'project_type',
                  'author', 'contributors', 'created_time']
        extra_kwargs = {'created_time': {'read_only': True}}

    def get_issues(self, obj):
        return IssueSerializer(obj.issues, many=True).data


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
