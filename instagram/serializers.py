from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Comment, Like, Profile


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(source='profile.avatar', default='', read_only=True)
    birth_date = serializers.DateField(source='profile.birth_date', default='', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'avatar', 'birth_date', 'last_login', 'is_superuser', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user)
        return user


class PostSerializer(serializers.ModelSerializer):
    author_avatar = serializers.ImageField(source='author.profile.avatar', read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_id = serializers.IntegerField(source='author.id', required=True)

    class Meta:
        model = Post
        fields = ('id', 'author_avatar', 'author_username', 'image', 'author_id', 'created_at')
        extra_kwargs = {'author': {'read_only': True}}

    def create(self, validated_data):
        print(validated_data)
        author = User.objects.get(pk=validated_data['author']['id'])
        image = validated_data['image']
        post = Post.objects.create(
            author=author,
            image=image
        )
        return post



class CommentSerializer(serializers.ModelSerializer):
    author_avatar = serializers.ImageField(source='author.profile.avatar', read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_id = serializers.IntegerField(source='author.id', required=True)

    class Meta:
        model = Comment
        fields = ('id', 'post', 'author_avatar', 'author_username', 'author_id', 'text', 'created_at')
        extra_kwargs = {'author': {'read_only': True}}

    def create(self, validated_data):
        print(validated_data)
        author = User.objects.get(pk=validated_data['author']['id'])
        comment = Comment.objects.create(
            author=author,
            post=validated_data['post'],
            text=validated_data['text'],
        )
        return comment


class LikeSerializer(serializers.ModelSerializer):
    author_avatar = serializers.ImageField(source='author.profile.avatar')
    author_username = serializers.CharField(source='author.username')
    author_id = serializers.IntegerField(source='author.id', read_only=True)

    class Meta:
        model = Like
        fields = ('id', 'post', 'author_avatar', 'author_username', 'author_id', 'created_at')
