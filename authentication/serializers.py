from rest_framework.serializers import (
    ModelSerializer, CharField,
    ValidationError, SerializerMethodField
)
from .models import User

AGE_LIMIT = 15


class UserSerializer(ModelSerializer):
    password = CharField(write_only=True)
    age = SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'birth_date', 'age',
                  'can_be_contacted', 'can_data_be_shared', 'created_time']
        extra_kwargs = {'created_time': {'read_only': True}}

    def get_age(self, obj):
        """Retourne l'âge."""
        return obj.age

    def validate_birth_date(self, value):
        """Valide que l'utilisateur a au moins 15 ans."""
        from datetime import date
        today = date.today()
        age = today.year - value.year
        if (today.month, today.day) < (value.month, value.day):
            age -= 1

        if age < AGE_LIMIT:
            raise ValidationError(
                "Vous devez avoir au moins 15 ans pour vous inscrire."
                )
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """
        Met à jour les champs autorisés.
        """
        # Gérer le mot de passe si présent
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)

        # Mettre à jour les autres champs
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
