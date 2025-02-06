
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import CreateAPIView
from .models import User, Contributor, Project, Issue, Comment
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    UserSerializer, ContributorSerializer,
    ProjectSerializer, IssueSerializer, CommentSerializer
)
from .permissions import ProjectPermission, IssuePermission, CommentPermission


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class ContributorViewSet(ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [ProjectPermission]


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

        return Issue.objects.filter(project__contributors__user=user).distinct()


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

        return Comment.objects.filter(issue__project__contributors__user=user).distinct()
