from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification


@receiver(post_save, sender=Notification)
def create_notification(sender, instance, created, **kwargs):
     print("hey")



#
# def my_handler(sender, instance, created, **kwargs):
#
#     notify.send(instance, verb='was saved')
#
# post_save.connect(my_handler, sender=Notification)
