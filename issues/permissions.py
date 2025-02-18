from rest_framework.permissions import BasePermission, SAFE_METHODS


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

        if request.method in ["PATCH", "DELETE"]:
            from .models import Issue
            issue_id = view.kwargs.get("pk")
            if issue_id:
                try:
                    issue = Issue.objects.get(id=issue_id)
                    project_id = issue.project.id
                except Issue.DoesNotExist:
                    print("Issue does not exist")
                    return False

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

        print(f"Utilisateur connecté : {request.user}")
        print(f"Auteur de l'issue : {obj.author.user}")

        if request.method in SAFE_METHODS:
            return Contributor.objects.filter(
                user=request.user, project=obj.project
            ).exists()

        # Seul l'auteur peut modifier ou supprimer l'issue
        return request.user == obj.author.user
