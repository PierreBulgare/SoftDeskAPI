from rest_framework.permissions import BasePermission, SAFE_METHODS


class ProjectPermission(BasePermission):
    """
    Permissions personnalisées :
    - Tout utilisateur authentifié peut lire un projet.
    - Tout utilisateur authentifié peut créer un projet.
    - Seul l'auteur peut modifier ou supprimer un projet.
    """

    def has_permission(self, request, view):
        """ Gère les permissions générales (liste, création, lecture...) """

        if view.action in ["list", "retrieve", "create"]:
            return request.user.is_authenticated

        return True

    def has_object_permission(self, request, view, obj):
        """ Gère les permissions spécifiques à un objet """

        if view.action in ["retrieve", "list"]:
            return True

        return request.user == obj.author


class IssuePermission(BasePermission):
    """
    Permissions personnalisées :
    - Tout utilisateur contributeur à un projet peut lire ses problèmes.
    - Tout utilisateur contributeur à un projet peut créer des problèmes.
    - Seul l'auteur d'un problème peut le modifier ou le supprimer.
    """

    def has_permission(self, request, view):
        """ Gère les permissions générales (liste, création, lecture...) """

        if not request.user.is_authenticated:
            return False

        project_id = (
            view.kwargs.get("project_pk") or request.data.get("project")
        )
        if not project_id:
            return False

        from .models import Project
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return False

        is_contributor = project.contributors.filter(
            user=request.user).exists()

        if request.method in SAFE_METHODS or request.method == "POST":
            return is_contributor

        return True

    def has_object_permission(self, request, view, obj):
        """ Gère les permissions spécifiques à un objet `Issue` """

        is_contributor = obj.project.contributors.filter(
            user=request.user).exists()

        if request.method in SAFE_METHODS:
            return is_contributor

        return request.user == obj.author


class CommentPermission(BasePermission):
    """
    Permissions personnalisées :
    - Tout utilisateur contributeur à un projet peut lire ses commentaires.
    - Tout utilisateur contributeur à un projet peut créer des commentaires.
    - Seul l'auteur d'un commentaire peut le modifier ou le supprimer.
    """

    def has_permission(self, request, view):
        """ Gère les permissions générales (liste, création, lecture...) """

        if not request.user.is_authenticated:
            return False

        issue_id = (
            view.kwargs.get("project_pk") or request.data.get("project")
            )
        if not issue_id:
            return False

        from .models import Issue
        try:
            issue = Issue.objects.get(id=issue_id)
        except Issue.DoesNotExist:
            return False

        is_contributor = issue.project.contributors.filter(
            user=request.user).exists()

        if request.method in SAFE_METHODS or request.method == "POST":
            return is_contributor

        return True

    def has_object_permission(self, request, view, obj):
        """ Gère les permissions spécifiques à un objet `Comment` """

        is_contributor = obj.issue.project.contributors.filter(
            user=request.user).exists()

        if request.method in SAFE_METHODS:
            return is_contributor

        return request.user == obj.author
