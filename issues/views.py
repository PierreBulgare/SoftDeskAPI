from rest_framework.viewsets import ModelViewSet
from .models import Issue
from .serializers import IssueSerializer
from .permissions import IssuePermission


class IssueViewSet(ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IssuePermission]

    def get_queryset(self):
        """ Retourne uniquement les issues
        des projets où l'utilisateur est contributeur. """
        user = self.request.user
        if not user.is_authenticated:
            return Issue.objects.none()

        return Issue.objects.filter(
            project__contributors__user=user).distinct()
