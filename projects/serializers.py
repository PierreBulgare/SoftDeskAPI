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

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Exclure l'id du projet de la liste des contributeurs
        representation['contributors'] = ContributorSerializer(
            instance.contributors.all(),
            many=True,
            context={**self.context, 'exclude_project': True}
        ).data

        # Ajouter les issues dans la vue détaillée du projet
        request = self.context.get('request', None)
        if (request
            and request.parser_context
            and 'pk' in request.parser_context['kwargs']):
            representation['issues'] = IssueSerializer(
                instance.issues.all(),
                many=True,
                context={**self.context,
                         'exclude_comments': True,
                         'exclude_project': True
                         }
            ).data

        return representation

    def get_issues(self, obj):
        return IssueSerializer(obj.issues, many=True).data
