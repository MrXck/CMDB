from django.conf.urls import url
from api import views


urlpatterns = [
    url(r'^server/$', views.ServerView.as_view()),
]
