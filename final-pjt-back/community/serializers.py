from django.core.exceptions import TooManyFieldsSent
from rest_framework import serializers
from .models import Review, Comment

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['movie', 'user', 'created_at']

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('__all__')
        read_only_fields = ['review', 'user',]

