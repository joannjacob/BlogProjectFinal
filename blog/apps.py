from django.apps import AppConfig
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from .signals import create_notification

from django.contrib.auth.models import User

class BlogConfig(AppConfig):
     name = 'blog'
     verbose_name = _('blogs')

     def ready(self):
          post_save.connect(create_notification, sender=User)
          myccl = self.get_model('Notification')
          post_save.connect(create_notification, sender=myccl, dispatch_uid="my_unique_identifier")
