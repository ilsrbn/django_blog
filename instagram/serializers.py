from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Comment, Like, Profile, Image


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'avatar')


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(source='profile.avatar', default='', required=False)
    birth_date = serializers.DateField(source='profile.birth_date', default='', read_only=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'avatar', 'birth_date', 'last_login', 'password', 'is_superuser')
        extra_kwargs = {'last_login': {'read_only': True}, 'is_superuser': {'read_only': True}, 'password': {'write_only': True}}

    def create(self, validated_data):
        print(self)
        user = User.objects.create_user(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        Profile.objects.create(user=user)
        return user

    def update(self, instance, validated_data):
        profile = Profile.objects.get(user=instance)
        print(validated_data)
        profile.avatar = validated_data['profile']['avatar']
        profile.save(update_fields=['avatar'])
        instance.profile = profile
        instance.save()
        return instance


class ImageSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField(source='post.id', required=True)

    class Meta:
        model = Image
        fields = ('id', 'image', 'post_id')
        extra_kwargs = {'post': {'read_only': True}}

    def create(self, validated_data):
        post = Post.objects.get(pk=validated_data['post']['id'])
        return Image.objects.create(post=post, image=validated_data['image'])


class LikeSerializer(serializers.ModelSerializer):
    author_avatar = serializers.ImageField(source='author.profile.avatar', read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_id = serializers.IntegerField(source='author.id')
    post_id = serializers.IntegerField(source='post.id')

    class Meta:
        model = Like
        fields = ('id', 'post_id', 'author_avatar', 'author_username', 'author_id')

    def create(self, validated_data):
        post = Post.objects.get(pk=validated_data['post']['id'])
        author = User.objects.get(pk=validated_data['author']['id'])
        return Like.objects.create(post=post, author=author)


class PostSerializer(serializers.ModelSerializer):
    author_avatar = serializers.ImageField(source='author.profile.avatar', read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_id = serializers.IntegerField(source='author.id', required=True)

    # images = serializers.StringRelatedField(many=True, required=False,)
    images = ImageSerializer(many=True, required=False)
    likes = LikeSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = ('id', 'author_avatar', 'likes', 'author_username', 'images', 'author_id', 'created_at')
        extra_kwargs = {'author': {'read_only': True}}

    def create(self, validated_data):
        author = User.objects.get(pk=validated_data['author']['id'])
        post = Post.objects.create(author=author)
        return post


class CommentSerializer(serializers.ModelSerializer):
    author_avatar = serializers.ImageField(source='author.profile.avatar', read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_id = serializers.IntegerField(source='author.id', required=True)
    post_id = serializers.IntegerField(source='post.id', required=True)

    class Meta:
        model = Comment
        fields = ('id', 'author_avatar', 'post_id', 'author_username', 'author_id', 'text', 'created_at')
        extra_kwargs = {'author': {'read_only': True}}

    def create(self, validated_data):
        author = User.objects.get(pk=validated_data['author']['id'])
        post = Post.objects.get(pk=validated_data['post']['id'])
        comment = Comment.objects.create(
            author=author,
            post=post,
            text=validated_data['text'],
        )
        return comment