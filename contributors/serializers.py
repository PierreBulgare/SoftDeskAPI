from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from .models import Contributor
from authentication.models import User
from projects.models import Project


class ContributorSerializer(ModelSerializer):
    user = PrimaryKeyRelatedField(queryset=User.objects.all())
    project = PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project', 'created_time']
        extra_kwargs = {'created_time': {'read_only': True}}
