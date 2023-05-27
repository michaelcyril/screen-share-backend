from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'phone',
            # 'type',
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        # print("hey iam reached")
        # first_name = self.validated_data['first_name']
        # last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        password = self.validated_data['password']
        username = self.validated_data['username']
        phone = self.validated_data['phone']
        # type = self.validated_data['type']
        user = User.objects.create_user(username=username, password=password, email=email,
                                        phone=phone)
        return user

