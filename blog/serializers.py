from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Article, Event

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ContactSerializer(serializers.Serializer):
    email = serializers.EmailField()
    request_type = serializers.ChoiceField(choices=[('contact', 'Contact'), ('bug', 'Bug Report')])
    message = serializers.CharField(max_length=2000)

    def validate_message(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("The message must be at least 10 characters long.")
        return value
    
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'published_date', 'image']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'content', 'published_date', 'start_date', 'end_date', 'image']