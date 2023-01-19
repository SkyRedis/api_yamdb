from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from reviews.models import Category, Genre, Title, Comment, Review

from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    CommentSerializer,
    ReviewSerializer
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = (permissions.AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=category__name',)


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    permission_classes = (permissions.AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=genre__name',)


class TitleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'genre__slug', 'category__slug')


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = []
    pagination_class = PageNumberPagination

    def get_queryset(self):
        if self.action == 'list':
            title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
            queryset = title.reviews
        else:
            title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
            queryset = title.reviews.all().filter(
                id=self.kwargs.get('review_id')
            )
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
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
            title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
            review = title.reviews.all().filter(
                id=self.kwargs.get('review_id')
            )
            queryset = review.comments
        else:
            title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
            review = title.reviews.all().filter(
                id=self.kwargs.get('review_id')
            )
            queryset = review.comments.all().filter(
                id=self.kwargs.get('comment_id')
            )
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = title.reviews.all().filter(
                id=self.kwargs.get('review_id')
        )
        serializer.save(author=self.request.user, review=review)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)
