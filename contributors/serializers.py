from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from .models import Contributor
from authentication.models import User


class ContributorSerializer(ModelSerializer):
    user = PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project', 'created_time']
        extra_kwargs = {'created_time': {'read_only': True}}

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if self.context.get('exclude_project', False):
            representation.pop('project', None)
        return representation
