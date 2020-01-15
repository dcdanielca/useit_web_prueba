from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from events.models import *


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(min_length=8)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')


class ResponseSerializer(serializers.ModelSerializer):
    creator_username = serializers.CharField(source='creator.username')

    class Meta:
        model = Comment
        exclude = ('responses',)


class CommentSerializer(serializers.ModelSerializer):
    responses = ResponseSerializer(required=False, read_only=True, many=True)
    creator_username = serializers.CharField(required = False, source='creator.username')

    class Meta:
        model = Comment
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):

    comments = CommentSerializer(required=False, read_only=True, many=True)

    class Meta:
        model = Event
        fields = '__all__'


class InteractionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interaction
        fields = '__all__'
  