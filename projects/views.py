from rest_framework.viewsets import ModelViewSet
from .models import Project
from .serializers import ProjectSerializer
from .permissions import ProjectPermission


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [ProjectPermission]

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
