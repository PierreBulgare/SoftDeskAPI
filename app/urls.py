"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentication.views import UserCreateView, UserViewSet
from contributors.views import ContributorViewSet
from projects.views import ProjectViewSet
from issues.views import IssueViewSet
from comments.views import CommentViewSet

router = routers.SimpleRouter()
router.register('users', UserViewSet, basename='user')
router.register('contributors', ContributorViewSet)
router.register('projects', ProjectViewSet)
router.register('issues', IssueViewSet)
router.register('comments', CommentViewSet)


urlpatterns = [
    path('api/register/', UserCreateView.as_view(), name='user-register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
]
