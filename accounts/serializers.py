from rest_framework import serializers
from django.contrib.auth import get_user_model
from django_countries.serializers import CountryFieldMixin
from .models import (
    UserRelationship, RegularProfile, FootballerProfile,
    ManagerProfile, OrganisationProfile, ProfileStatus
)

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone_number', 'username', 'firstname', 'lastname',
                  'user_type', 'is_moderator', 'is_developer', 'is_verified']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)

class UserRelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRelationship
        fields = ['id', 'follower', 'following', 'created_at']

class ProfileStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileStatus
        fields = ['id', 'status', 'reason', 'reconsidered_at', 'created_at', 'updated_at']

class BaseProfileSerializer(CountryFieldMixin, serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    status = ProfileStatusSerializer(read_only=True)
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)

    class Meta:
        abstract = True
        fields = ['id', 'user', 'country', 'bio', 'avatar', 'status', 'preferred_language',
                  'time_zone', 'created_at', 'updated_at', 'website', 'social_media_links',
                  'followers_count', 'following_count']

class RegularProfileSerializer(BaseProfileSerializer):
    class Meta(BaseProfileSerializer.Meta):
        model = RegularProfile

class FootballerProfileSerializer(BaseProfileSerializer):
    class Meta(BaseProfileSerializer.Meta):
        model = FootballerProfile
        fields = BaseProfileSerializer.Meta.fields + ['position', 'club', 'national_team']

class ManagerProfileSerializer(BaseProfileSerializer):
    class Meta(BaseProfileSerializer.Meta):
        model = ManagerProfile
        fields = BaseProfileSerializer.Meta.fields + ['current_team', 'coaching_style']

class OrganisationProfileSerializer(BaseProfileSerializer):
    class Meta(BaseProfileSerializer.Meta):
        model = OrganisationProfile
        fields = BaseProfileSerializer.Meta.fields + ['organisation_name', 'organisation_type']

class UserDetailSerializer(UserSerializer):
    profile = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['profile']

    def get_profile(self, obj):
        if hasattr(obj, 'regularprofile'):
            return RegularProfileSerializer(obj.regularprofile).data
        elif hasattr(obj, 'footballerprofile'):
            return FootballerProfileSerializer(obj.footballerprofile).data
        elif hasattr(obj, 'managerprofile'):
            return ManagerProfileSerializer(obj.managerprofile).data
        elif hasattr(obj, 'organisationprofile'):
            return OrganisationProfileSerializer(obj.organisationprofile).data
        return None