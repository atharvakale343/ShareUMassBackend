from django.urls import path
import postings.views

import user.views

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("callback", views.callback, name="callback"),
    path(route="api/public", view=views.public, name="public"),
    path(route="api/private", view=views.private, name="private"),
    path(route="user/get", view=user.views.GetAccount.as_view()),
    path(route="posting/create", view=postings.views.UserPosting.as_view()),
    path(route="postings/get", view=postings.views.PostingsView.as_view()),
    path(route="delete", view=postings.views.DeleteView.as_view()),
]
