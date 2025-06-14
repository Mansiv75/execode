# auth_api/serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['id', 'email']  # You can allow email editing if needed
    # def update(self, instance, validated_data):
    #     # Update the user instance with validated data
    #     instance.username = validated_data.get('username', instance.username)
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.save()
    #     return instance
    # def create(self, validated_data):
    #     # Create a new user instance with validated data
    #     user = User(
    #         username=validated_data['username'],
    #         email=validated_data['email']
    #     )
    #     user.set_password(validated_data.get('password', None))
    #     user.save()
    #     return user