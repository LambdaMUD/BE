from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework.authtoken import views

from rest_framework import routers
from notes.api import PersonalNoteViewSet

router = routers.DefaultRouter()
router.register('notes', PersonalNoteViewSet) # --> Registered notes/ endpoint

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    re_path(r'^api-token-auth/', views.obtain_auth_token),
]
