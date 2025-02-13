from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from contributors.serializers import ContributorSerializer
from .models import Project
from authentication.models import User
from issues.serializers import IssueSerializer


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
