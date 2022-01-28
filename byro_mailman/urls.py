from django.urls import path

from . import views

urlpatterns = [
    path(
        "members/view/<int:pk>/mailman/<int:list_id>/remove",
        views.MemberRemove.as_view(),
        name="members.mailman.remove",
    ),
    path(
        "members/view/<int:pk>/mailman/add",
        views.MemberAdd.as_view(),
        name="members.mailman.add",
    ),
    path(
        "members/view/<int:pk>/mailman",
        views.MemberLists.as_view(),
        name="members.mailman.lists",
    ),
    path("mailman/sync", views.MailmanSync.as_view(), name="lists.sync"),
    path("mailman/", views.MailmanView.as_view(), name="lists.dashboard"),
]
