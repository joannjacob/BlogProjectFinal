from django.conf.urls import url,include
from rest_framework import routers
from blog import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'blogs', views.BlogViewSet)
router.register(r'comments', views.CommentViewSet)



urlpatterns = router.urls



