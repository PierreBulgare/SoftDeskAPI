from rest_framework.viewsets import ModelViewSet
from .models import Comment
from .serializers import CommentSerializer
from .permissions import CommentPermission


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
            issue__project__contributors__user=user).distinct()
