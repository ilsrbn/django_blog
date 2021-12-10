from rest_framework import viewsets
from .serializers import UserSerializer, PostSerializer, CommentSerializer, LikeSerializer
from .models import User, Post, Comment, Like
from django_filters import rest_framework as filters
from rest_framework.permissions import AllowAny, IsAuthenticated


class ActionBasedPermission(AllowAny):
    """
    Grant or deny access to a view, based on a mapping in view.action_permissions
    """
    def has_permission(self, request, view):
        for klass, actions in getattr(view, 'action_permissions', {}).items():
            if view.action in actions:
                return klass().has_permission(request, view)
        return False


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.order_by('created_at').reverse()
    serializer_class = PostSerializer

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('author_id',)
    ordering_fields = '__all__'

    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        IsAuthenticated: ['update', 'partial_update', 'destroy'],
        AllowAny: ['retrieve', 'list', 'create', 'update']
    }


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('author_id', 'post',)

    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        IsAuthenticated: ['update', 'partial_update', 'destroy'],
        AllowAny: ['retrieve', 'list', 'create', 'update']
    }


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('author_id', 'post',)