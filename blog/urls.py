from django.conf.urls import url
from . import views
from .views import UserList

from django.contrib.auth import views as auth_views

app_name='blog'

urlpatterns = [
    # url(r'^$', views.users_list, name='users_list'),

    url(r'^$',views.home),
    url(r'^login/$',auth_views.login,name="login"),
    url(r'user',views.enter_login),
    url(r'chatroom_options',views.chatroom_options),
    url(r'^notification/(?P<user_id>[0-9]+)$',views.notification),
    #url(r'^login/user$',views.enter_login),
    url(r'^add_blog$',views.add_blog),
    url(r'^add_blogentry$',views.add_blogentry),

    url(r'^my_blogs', views.my_blogs),
    # url(r'^filter$', views.filter_all),
    url(r'^(?P<content_id>[0-9]+)/$', views.myblogs_detail),


    url(r'^(?P<content_id>[0-9]+)/edit_blog$', views.edit_blog),
    url(r'^(?P<content_id>[0-9]+)/myblog_editupdate', views.myblog_editupdate),

    url(r'^all_blogs', views.all_blogs),
    url(r'^(?P<content_id>[0-9]+)/all$', views.allblogs_detail),
    url(r'^(?P<content_id>[0-9]+)/like/',views.like),
    url(r'^(?P<content_id>[0-9]+)/add_comment',views.add_comment),
    url(r'^(?P<content_id>[0-9]+)/view_questions',views.ask_questions),
    url(r'^(?P<content_id>[0-9]+)/(?P<que_id>[0-9]+)/add_answers',views.add_answers),
    url(r'^(?P<content_id>[0-9]+)/ask_questions', views.ask_questions),
    url(r'^(?P<content_id>[0-9]+)/add_questions', views.add_questions),

    url(r'^signup/$', views.signup),
    url(r'^entersignup$', views.add_signup),
    #url(r'^login$', views.add_signup),
    url(r'logout$',views.logout),

    url(r'^login/forgot_password',views.forgot_password),
    url(r'^login/password_update',views.password_update),
    url(r'about/',UserList.as_view()),

    url(r'like/',views.like),



]