from rest_framework import serializers
from reviews.models import Comment, Review


class CommentSerializer(serializers.ModelSerializer):

    class Meta():
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):

    class Meta():
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
