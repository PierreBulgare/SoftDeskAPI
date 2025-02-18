from rest_framework.viewsets import ModelViewSet
from .models import Project
from .serializers import ProjectSerializer
from .permissions import ProjectPermission
from rest_framework.decorators import action
from rest_framework.response import Response


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [ProjectPermission]

    @action(detail=True, methods=['post'], url_path='subscribe')
    def subscribe(self, request, pk=None):
        """
        Permet à un utilisateur de souscrire
        à un projet en tant que contributeur.
        """
        project = self.get_object()
        user = request.user

        # Vérifier si l'utilisateur est déjà contributeur
        if project.contributors.filter(id=user.id).exists():
            return Response(
                {"message": "Vous êtes déjà contributeur de ce projet."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Ajouter l'utilisateur en tant que contributeur
        from contributors.models import Contributor
        from contributors.serializers import ContributorSerializer
        contributor = Contributor.objects.create(user=user, project=project)
        serializer = ContributorSerializer(contributor)

        return Response(
            {
                "message": "Vous avez été ajouté comme contributeur.",
                "contributor": serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
