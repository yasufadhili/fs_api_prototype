from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import (
    User, UserRelationship, RegularProfile, FootballerProfile,
    ManagerProfile, OrganisationProfile, ProfileStatus
)
from .serializers import (
    UserSerializer, UserDetailSerializer, UserRelationshipSerializer,
    RegularProfileSerializer, FootballerProfileSerializer,
    ManagerProfileSerializer, OrganisationProfileSerializer,
    ProfileStatusSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['list', 'create']:
            return UserSerializer
        return UserDetailSerializer

    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        user = self.get_object()
        follower = request.user
        UserRelationship.objects.get_or_create(follower=follower, following=user)
        return Response({'status': 'now following'})

    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        user = self.get_object()
        follower = request.user
        UserRelationship.objects.filter(follower=follower, following=user).delete()
        return Response({'status': 'unfollowed'})

    @action(detail=True, methods=['get'])
    def followers(self, request, pk=None):
        user = self.get_object()
        followers = user.followers.all()
        serializer = UserSerializer(followers, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def following(self, request, pk=None):
        user = self.get_object()
        following = user.following.all()
        serializer = UserSerializer(following, many=True)
        return Response(serializer.data)

class BaseProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class RegularProfileViewSet(BaseProfileViewSet):
    queryset = RegularProfile.objects.all()
    serializer_class = RegularProfileSerializer

class FootballerProfileViewSet(BaseProfileViewSet):
    queryset = FootballerProfile.objects.all()
    serializer_class = FootballerProfileSerializer

class ManagerProfileViewSet(BaseProfileViewSet):
    queryset = ManagerProfile.objects.all()
    serializer_class = ManagerProfileSerializer

class OrganisationProfileViewSet(BaseProfileViewSet):
    queryset = OrganisationProfile.objects.all()
    serializer_class = OrganisationProfileSerializer

class ProfileStatusViewSet(viewsets.ModelViewSet):
    queryset = ProfileStatus.objects.all()
    serializer_class = ProfileStatusSerializer
    permission_classes = [permissions.IsAdminUser]

class UserRelationshipViewSet(viewsets.ModelViewSet):
    queryset = UserRelationship.objects.all()
    serializer_class = UserRelationshipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(follower=self.request.user)

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)