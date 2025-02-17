from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User
from rest_framework.exceptions import PermissionDenied
from .serializers import UserSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserViewSet(ModelViewSet):
    """
    ViewSet pour les utilisateurs.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filtre les utilisateurs visibles pour l'utilisateur connecté.
        - Permet de voir les utilisateurs partageant leurs données.
        - Ajoute les propres données de l'utilisateur connecté.
        """
        user = self.request.user
        return User.objects.filter(can_data_be_shared=True) | User.objects.filter(id=user.id)

    def update(self, request, *args, **kwargs):
            """
            Autorise uniquement la mise à jour des données de l'utilisateur connecté.
            """
            instance = self.get_object()

            # Vérifie que l'utilisateur connecté est bien celui qui modifie
            if instance != request.user:
                raise PermissionDenied(
                     "Vous ne pouvez modifier que vos propres informations."
                     )

            return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """
        Autorise uniquement la suppression de l'utilisateur connecté.
        """
        instance = self.get_object()

        # Vérifie que l'utilisateur connecté est bien celui qui supprime
        if instance != request.user:
            raise PermissionDenied(
                "Vous ne pouvez supprimer que votre propre compte."
                )

        super().destroy(request, *args, **kwargs)
    
        # Retourne un message de confirmation
        return Response(
            {"message": "Votre compte a bien été supprimé."},
            status=status.HTTP_200_OK
        )
