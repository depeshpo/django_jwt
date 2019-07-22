from rest_framework.serializers import ModelSerializer
from .models import User, Profile


class UserSerializer(ModelSerializer):
    class Meta:
        fields = ('email', 'password')
        model = User
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class ProfileReadSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        fields = '__all__'
        model = Profile


class ProfileWriteSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Profile

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        return response
