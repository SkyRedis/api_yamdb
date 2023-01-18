from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from reviews.models import Comment, Review, Titles

from .serializers import CommentSerializer, ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = []
    pagination_class = PageNumberPagination

    def get_queryset(self):
        if self.action == 'list':
            title = get_object_or_404(Titles, id=self.kwargs.get('title_id'))
            queryset = title.reviews
        else:
            title = get_object_or_404(Titles, id=self.kwargs.get('title_id'))
            queryset = title.reviews.all().filter(
                id=self.kwargs.get('review_id')
            )
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = []
    pagination_class = PageNumberPagination

    def get_queryset(self):
        if self.action == 'list':
            title = get_object_or_404(Titles, id=self.kwargs.get('title_id'))
            review = title.reviews.all().filter(
                id=self.kwargs.get('review_id')
            )
            queryset = review.comments
        else:
            title = get_object_or_404(Titles, id=self.kwargs.get('title_id'))
            review = title.reviews.all().filter(
                id=self.kwargs.get('review_id')
            )
            queryset = review.comments.all().filter(
                id=self.kwargs.get('comment_id')
            )
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, id=self.kwargs.get('title_id'))
        review = title.reviews.all().filter(
                id=self.kwargs.get('review_id')
        )
        serializer.save(author=self.request.user, review=review)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)
