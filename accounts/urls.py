from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.UserViewSet)
router.register(r'regular-profiles', views.RegularProfileViewSet)
router.register(r'footballer-profiles', views.FootballerProfileViewSet)
router.register(r'manager-profiles', views.ManagerProfileViewSet)
router.register(r'organisation-profiles', views.OrganisationProfileViewSet)
router.register(r'profile-statuses', views.ProfileStatusViewSet)
router.register(r'user-relationships', views.UserRelationshipViewSet)

urlpatterns = [
    path('', include(router.urls)),
]