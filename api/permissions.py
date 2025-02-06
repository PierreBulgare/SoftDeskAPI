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
            print("User not authenticated")
            return False
        
        if request.method == "GET" and "project_pk" not in view.kwargs:
            return True

        project_id = (
            view.kwargs.get("project_pk") or request.data.get("project")
        )
        if not project_id:
            print("No project ID")
            return False

        from .models import Project, Contributor
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            print("Project does not exist")
            return False

        is_contributor = (
            Contributor.objects.filter(
                user=request.user, project=project).exists()
        )

        if request.method in SAFE_METHODS or request.method == "POST":
            print("Safe methods or POST")
            return is_contributor

        return True

    def has_object_permission(self, request, view, obj):
        """ Gère les permissions spécifiques à un objet `Issue` """

        from .models import Contributor

        is_contributor = (
            Contributor.objects.filter(
                user=request.user, project=obj.project).exists()
        )

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
            print("User not authenticated")
            return False
        
        if request.method == "GET" and "issue_pk" not in view.kwargs:
            print("GET request")
            return True

        issue_id = (
            view.kwargs.get("issue_pk") or request.data.get("issue")
            )
        if not issue_id:
            return False

        from .models import Issue, Contributor
        try:
            issue = Issue.objects.get(id=issue_id)
        except Issue.DoesNotExist:
            return False

        is_contributor = (
            Contributor.objects.filter(
                user=request.user, project=issue.project).exists()
        )

        if request.method in SAFE_METHODS or request.method == "POST":
            return is_contributor

        return True

    def has_object_permission(self, request, view, obj):
        """ Gère les permissions spécifiques à un objet `Comment` """

        from .models import Contributor

        is_contributor = (
            Contributor.objects.filter(
                user=request.user, project=obj.issue.project).exists()
        )

        if request.method in SAFE_METHODS:
            return is_contributor

        return request.user == obj.author
