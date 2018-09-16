from rest_framework import viewsets, filters
from rest_framework.pagination import CursorPagination

from .models import Snippet, Comment
from .serializers import SnippetSerializer, CommentSerializer


class SnippetPagination(CursorPagination):
    ordering = '-created_at'


class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    filter_backends = (filters.OrderingFilter,)
    pagination_class = SnippetPagination
    ordering_fields = ('id', 'created_at',)
    ordering = ('created_at',)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('commented_at',)
    ordering = ('commented_at',)
