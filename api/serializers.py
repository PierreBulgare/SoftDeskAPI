from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import User, Contributor, Project, Issue, Comment

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ContributorSerializer(ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Contributor
        fields = '__all__'

class ProjectSerializer(ModelSerializer):
    author = ContributorSerializer()
    contributors = ContributorSerializer(many=True)
    class Meta:
        model = Project
        fields = '__all__'

class IssueSerializer(ModelSerializer):
    project = ProjectSerializer()
    author = ContributorSerializer()
    comments = SerializerMethodField()
    class Meta:
        model = Issue
        fields = '__all__'

    def get_comments(self, obj):
        return CommentSerializer(obj.comments, many=True).data
    
class CommentSerializer(ModelSerializer):
    author = ContributorSerializer()
    class Meta:
        model = Comment
        fields = '__all__'