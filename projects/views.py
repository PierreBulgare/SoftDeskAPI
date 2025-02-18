from rest_framework.viewsets import ModelViewSet
from .models import Project
from .serializers import ProjectSerializer
from .permissions import ProjectPermission
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


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

        from contributors.models import Contributor
        from contributors.serializers import ContributorSerializer
        contributor, created = Contributor.objects.get_or_create(
            user=user, project=project)

        # Vérifier si l'utilisateur est déjà contributeur
        if not created:
            return Response(
                {"message": "Vous êtes déjà contributeur de ce projet."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Serializer le contributeur
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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Le projet a été supprimée avec succès."},
            status=status.HTTP_200_OK
        )
