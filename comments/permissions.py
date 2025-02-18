from rest_framework.permissions import BasePermission, SAFE_METHODS


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

        if request.method == "DELETE":
            from .models import Comment
            comment_id = view.kwargs.get("pk")
            if comment_id:
                try:
                    comment = Comment.objects.get(id=comment_id)
                    issue_id = comment.issue.id
                except Comment.DoesNotExist:
                    print("Comment does not exist")
                    return False

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

        return request.user == obj.author.user
