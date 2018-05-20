from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^members/view/(?P<pk>\d+)/mailman/(?P<list_id>\d+)/remove$', views.MemberRemove.as_view(), name='members.mailman.remove'),
    url(r'^members/view/(?P<pk>\d+)/mailman/add$', views.MemberAdd.as_view(), name='members.mailman.add'),
    url(r'^members/view/(?P<pk>\d+)/mailman$', views.MemberLists.as_view(), name='members.mailman.lists'),

    url(r'mailman/sync$', views.MailmanSync.as_view(), name='lists.sync'),
    url(r'mailman/$', views.MailmanView.as_view(), name='lists.dashboard'),
]
