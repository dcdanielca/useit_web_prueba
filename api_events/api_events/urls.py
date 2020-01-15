"""api_events URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token
from events import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    url(r'logout/', views.Logout.as_view()),
    url(r'^users/register/',views.UserCreate.as_view()),
    url(r'^event/(?P<pk>[0-9]+)/', views.EventDetail.as_view()),
    url(r'^event/', views.EventView.as_view()),
    url(r'^events/(?P<ini>[0-9]+)/(?P<fin>[0-9]+)/', views.EventList.as_view()),
    url(r'^interaction/post/', views.InteractionCreate.as_view()),
    url(r'^comment/post/', views.CommentCreate.as_view()),
    url(r'^response/post/', views.ResponseCreate.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)