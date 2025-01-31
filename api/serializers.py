from rest_framework.serializers import (
    ModelSerializer, SerializerMethodField,
    CharField, PrimaryKeyRelatedField
)

from .models import User, Contributor, Project, Issue, Comment


class UserSerializer(ModelSerializer):
    password = CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'age', 'can_be_contacted', 'can_data_be_shared', 'created_time']
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
        fields = ['id', 'name', 'description', 'project_type', 'author', 'contributors', 'created_time']
        extra_kwargs = {'created_time': {'read_only': True}}

    def get_issues(self, obj):
        return IssueSerializer(obj.issues, many=True).data


class IssueSerializer(ModelSerializer):
    project = PrimaryKeyRelatedField(queryset=Project.objects.all())
    author = PrimaryKeyRelatedField(queryset=Contributor.objects.all())
    comments = SerializerMethodField()

    class Meta:
        model = Issue
        fields =['id', 'title', 'description', 'priority', 'balise', 'status', 'project', 'author', 'comments', 'created_time']
        extra_kwargs = {'created_time': {'read_only': True}}

    def get_comments(self, obj):
        return CommentSerializer(obj.comments, many=True).data
    
class CommentSerializer(ModelSerializer):
    author = PrimaryKeyRelatedField(queryset=Contributor.objects.all())
    issue = PrimaryKeyRelatedField(queryset=Issue.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'description', 'issue', 'author', 'created_time']
        extra_kwargs = {'created_time': {'read_only': True}}