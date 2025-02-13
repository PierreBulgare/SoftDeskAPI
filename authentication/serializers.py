from rest_framework.serializers import ModelSerializer, CharField
from .models import User

class UserSerializer(ModelSerializer):
    password = CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'age',
                  'can_be_contacted', 'can_data_be_shared', 'created_time']
        extra_kwargs = {'created_time': {'read_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)