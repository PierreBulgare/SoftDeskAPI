from rest_framework.permissions import BasePermission


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
