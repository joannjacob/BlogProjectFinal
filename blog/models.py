from django.db import models
from django.db.models import signals
from django.utils import timezone

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def ensure_profile_exists(sender, **kwargs):
    if kwargs.get('created', False):
        Users.objects.get_or_create(user=kwargs.get('instance'))


def create_user(sender, instance, created, **kwargs):
    print("Save is called")

class Users(models.Model):

    firstname=models.CharField(max_length=100,default="")
    lastname=models.CharField(max_length=100,default="")
    emailid=models.CharField(max_length=100,default="",unique=True)
    mobile=models.CharField(max_length=100,default="")
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    security_question=models.CharField(max_length=100,default="")
    security_answer = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

signals.post_save.connect(create_user, sender=Users)


class Tag(models.Model):

    tag= models.CharField(max_length=35)
    #slug        = models.CharField(max_length=250)
    #created_at  = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

class Blog(models.Model):

    user=models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title=models.CharField(max_length=100,default="")
    content=models.CharField(max_length=500,default="")

    tag_name=models.CharField(max_length=200,default="")
    tag = models.ManyToManyField('Tag')

    def as_dict(self):
        return {
            "id": self.id,
            "tag_name": self.tag_name,
            "title": self.title,
            # other stuff
        }

    #tags = MultiSelectField(choices=Tag,null=True, blank=True)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"

class Question(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE,default="")
    blog = models.ForeignKey('Blog',on_delete=models.CASCADE)
    question = models.TextField(max_length=500,default="")


    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

class Answer(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE,default="")
    blog = models.ForeignKey('Blog',on_delete=models.CASCADE)
    answer = models.TextField(max_length=500,default="")
    qid=models.ForeignKey('Question',on_delete=models.CASCADE)

    def __str__(self):
        return self.answer

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"



class Comment(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE,default="")
    blog = models.ForeignKey('Blog',on_delete=models.CASCADE)
    comment = models.TextField(max_length=500,default=None)


    def __str__(self):
        return self.comment

class Like(models.Model):
    user = models.ForeignKey('auth.User',on_delete=models.CASCADE,default="")
    blog = models.ForeignKey('Blog',on_delete=models.CASCADE)



class Notifications(models.Model):
    recipient = models.ForeignKey('auth.User', related_name="recipient", on_delete=models.CASCADE, default="")
    sender = models.CharField(max_length=50,default="")
    senderid = models.ForeignKey('auth.User', related_name="sender", on_delete=models.CASCADE, default="")
    blog = models.ForeignKey('Blog',on_delete=models.CASCADE)
    comment = models.ForeignKey('Comment',on_delete=models.CASCADE,null=True, blank=True,default=True)
    like=models.ForeignKey('Like',on_delete=models.CASCADE,null=True, blank=True,default="")


    def __str__(self):
        return str(self.sender)






