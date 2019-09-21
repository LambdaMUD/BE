from django.urls import include, path, re_path
from django.conf.urls import url
from rest_framework.authtoken import views
# from . import api

urlpatterns = [
    # path('', include('rest_auth.urls')),
    path('', views.obtain_auth_token),
    path('registration/', include('rest_auth.registration.urls')),
    # url('maze_init', api.maze_init)
]