from rest_framework.viewsets import ModelViewSet
from .models import Comment
from .serializers import CommentSerializer
from .permissions import CommentPermission
from rest_framework.response import Response
from rest_framework import status


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [CommentPermission]

    def get_queryset(self):
        """ Retourne uniquement les commentaires des issues
        de projets où l'utilisateur est contributeur. """
        user = self.request.user

        if not user.is_authenticated:
            return Comment.objects.none()

        return Comment.objects.filter(
            issue__project__contributors__user=user
        ).select_related('issue', 'issue__project').distinct()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Le commentaire a été supprimée avec succès."},
            status=status.HTTP_200_OK
        )
