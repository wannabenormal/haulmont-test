from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate


from .models import Note

UserModel = get_user_model()


class NoteSerializer(serializers.ModelSerializer):
    class Meta():
        model = Note
        fields = ('id', 'title', 'description', 'created_at', )
        read_only_fields = ('created_at', )


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    notes = NoteSerializer(many=True, read_only=True)

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

        return user

    class Meta:
        model = UserModel
        fields = ('id', 'username', 'password', 'notes', )


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        write_only=True,
        label='Username'
    )
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True,
        label='Password'
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(
                request=self.context.get('request'),
                username=username, password=password
            )

            if not user:
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs
