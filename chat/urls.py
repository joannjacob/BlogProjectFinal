from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<user_name>[^/]+)/(?P<room_name>[^/]+)/$', views.room, name='room'),
]