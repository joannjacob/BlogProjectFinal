from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Users, Blog, Like, Comment,Tag,Question,Answer,Notifications

from . import serializers

from .serializers import UserSerializer, BlogSerializer, CommentSerializer
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.utils.safestring import mark_safe
import json

from channels.generic.websocket import AsyncWebsocketConsumer


from channels.layers import get_channel_layer

from asgiref.sync import async_to_sync



class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]
    queryset = Comment.objects.all()


class UserList(generics.ListAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer


def home(request):
    return render(request, 'blog/home.html')


def signup(request):
    return render(request, 'blog/signup.html')


def login(request):
    return render(request, 'blog/login.html')


def logout(request):
    return render(request, 'blog/home.html')

def chatroom_options(request):
    current_user=request.user
    return render(request, 'blog/chatroom_options.html',{'user':current_user})

# def users_list(request):
#     return render(request, 'blog/users_list.html')

def notification(request,user_id):
    # current_user=request.user
    # if(current_user.id==content_id):
    # return render(request, 'noti/room.html', {
    #     'user_name_json': mark_safe(json.dumps(user_id)),
    #
    # })
    notif_obj = Notifications.objects.filter(recipient=user_id)




    return render(request, 'blog/notification.html',{'notifications':notif_obj,'user_id':user_id})




def add_signup(request):
    if request.method == 'POST':
        if (request.POST.get('firstname') and request.POST.get('lastname') and
                request.POST.get('emailid') and request.POST.get('mobile') and request.POST.get('username') and
                request.POST.get('password') and request.POST.get('retypepassword')
                and request.POST.get('question') and request.POST.get('answer')):

            firstname = request.POST.get('firstname', '')
            lastname = request.POST.get('lastname', '')
            emailid = request.POST.get('emailid', '')
            mobile = request.POST.get('mobile', '')

            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            retypepassword = request.POST.get('retypepassword', '')
            question = request.POST.get('question', '')
            answer = request.POST.get('answer', '')

            obj = Users()
            obj.firstname = firstname
            obj.lastname = lastname
            obj.emailid = emailid
            obj.mobile = mobile
            obj.username = username
            obj.password = password
            obj.security_question = question
            obj.security_answer = answer
            obj.save()


            auth_user=User()
            auth_user.first_name=firstname
            auth_user.last_name = lastname
            auth_user.username = username
            auth_user.set_password(password)
            auth_user.is_superuser = 1
            auth_user.save()

            return render(request, 'blog/home.html')
        else:
            return render(request, 'blog/signup.html')


def add_blog(request):
    tags=Tag.objects.all()
    return render(request, 'blog/add_blog.html',{'tags':tags})

def edit_blog(request):
    return render(request, 'blog/edit_blog.html')

def edit_blogentry(request):
    if request.method == 'POST':
        if (request.POST.get('content') and request.POST.get('title') and request.POST.getlist('tags')):
            current_user=request.user
            obj = Blog()
            print(request.POST.getlist('tags'))
            obj.title = request.POST.get('title')
            obj.content = request.POST.get('content')
            obj.user=current_user
            obj.save()

            return render(request, 'blog/user.html')
        else:
            return render(request, 'blog/fail.html')




def add_blogentry(request):
    if request.method == 'POST':
        if (request.POST.get('content') and request.POST.get('title')):
            current_user = request.user
            list=request.POST.getlist('tags')
            obj = Blog()
            tagobj=Tag.objects.all()
            obj.title = request.POST.get('title')
            obj.content = request.POST.get('content')
            obj.user = current_user
            #obj.email = request.session['emailid']
            obj.tag_name = request.POST.getlist('tags')

            obj.save()
            for tag in tagobj:
                for item in list:
                    if(item==tag.tag):
                        tagobject=Tag.objects.get(tag=tag.tag)
                        obj.tag.add(tagobject)

            return render(request, 'blog/user.html')
        else:
            return render(request, 'blog/fail.html')





'''class MyBlogs(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'my_blogs.html'
    def get(self, request):
        queryset = Blog.objects.filter(email=request.session['emailid'])
        serializer_class = BlogSerializer
        return Response({'myblogs':queryset})

def all_blogs(request):
    myblogs=Blog.objects.all()
    return render(request,'my_blogs.html',{'myblogs':myblogs})
'''

def my_blogs(request):
    current_user = request.user
    all_contents = Blog.objects.filter(user=current_user)
    tags = Tag.objects.all()
    if request.method == 'GET':
        tag=request.GET.get('tag', None)
        # return render(request, 'blog/fail.html')
        if(tag!=None and tag != ''):
            for a in tag.split(","):
                tagobj = Tag.objects.get(id=a)
                print("------------- Tag " + tagobj.tag)
                blogs= Blog.objects.filter(tag=tagobj)

                dictionaries = [obj.as_dict() for obj in blogs]
                print("------------- Blogs " + json.dumps(dictionaries))

                data = {
                       'blogs': dictionaries
                }
                data = json.dumps(data)
                return HttpResponse(data,content_type='application/json')

    return render(request, 'blog/myblog_links.html', {'all_blogs': all_contents,'tags': tags})




def myblogs_detail(request,content_id):

    try:
        all_contents = Blog.objects.get(id=content_id)
        all_comments = Comment.objects.filter(blog=content_id)
        if Like.objects.filter(user=request.user,blog=content_id):
            flag=True
        else:
            flag=False
    except Blog.DoesNotExist:
        raise Http404("Blog doesnt exist")
    return render(request, 'blog/blog_details.html', {'all_blogs': all_contents,'all_comments' : all_comments,'flag':flag})


def myblog_editupdate(request, content_id):
    # return HttpResponse("<h2>Details: "+ str(content_id) +"</h2>")
    if request.method == 'POST':
        if (request.POST.get('edittedblog')):
            try:
                obj= Blog.objects.get(id=content_id)
                obj.content = request.POST.get("edittedblog")
                obj.save()
                return render(request, 'blog/user.html')
            except Blog.DoesNotExist:
                raise Http404("Blog doesnt exist")
        else:
            return render(request, 'blog/fail.html')


def all_blogs(request):
    all_contents = Blog.objects.all()
    userflag=request.user
    tags = Tag.objects.all()
    if request.method == 'GET':
        tag=request.GET.get('tag', None)
        # return render(request, 'blog/fail.html')
        if(tag!=None and tag != ''):
            for a in tag.split(","):
                tagobj = Tag.objects.get(id=a)
                print("------------- Tag " + tagobj.tag)
                blogs= Blog.objects.filter(tag=tagobj)

                dictionaries = [obj.as_dict() for obj in blogs]
                print("------------- Blogs " + json.dumps(dictionaries))

                data = {
                       'blogs': dictionaries
                }
                data = json.dumps(data)
                return HttpResponse(data,content_type='application/json')

                # return render(request, 'blog/allblog_links.html',{'all_blogs': blogs, 'userflag': userflag, 'tags': tags})


    return render(request, 'blog/allblog_links.html', {'all_blogs': all_contents,'userflag':userflag,'tags': tags})


def allblogs_detail(request, content_id):
    # return HttpResponse("<h2>Details: "+ str(content_id) +"</h2>")
    try:
        all_contents = Blog.objects.get(id=content_id)
        all_comments = Comment.objects.filter(blog=content_id)
        if Like.objects.filter(user=request.user,blog=content_id):
            flag=True
        else:
            flag=False

        if Blog.objects.filter(user=request.user,id=content_id):
            userflag=True
        else:
            userflag=False
    except Blog.DoesNotExist:
        raise Http404("Blog doesnt exist")
    return render(request, 'blog/all_blogs.html', {'all_blogs': all_contents,'all_comments' : all_comments,
                                                   'flag':flag,'userflag':userflag})


def enter_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        try:
            obj = Users.objects.get(username=username)
            print(obj)
            if (obj is not None and obj.password == password):
                request.session['emailid'] = obj.emailid
                blogobj = Blog.objects.all()
                blogobj.email = request.session['emailid']
                return render(request, 'blog/user.html')
            else:
                return render(request, 'login.html')
        except Users.DoesNotExist:
            return render(request, 'login.html')


def forgot_password(request):
    return render(request, 'forgot_password.html')


def password_update(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        question = request.POST.get('question', '')
        answer = request.POST.get('answer', '')

        try:
            obj = Users.objects.get(username=username)
            if (obj.security_question == question and obj.security_answer == answer):
                password = request.POST.get('password', '')
                obj.password = password
                obj.save()
                return render(request, 'login.html')
            else:
                return render(request, 'blog/fail.html')
        except Users.DoesNotExist:
            return render(request, 'login.html')


def password_change(request):
    if request.method == 'POST':
        if (request.POST.get('password')):
            password = request.POST.get('password', '')
            obj = Users()
            obj.password = password
            obj.save()
            return render(request, 'login.html')
        else:
            return render(request, 'update_password.html')


def like(request, content_id):

    blogobj=Blog.objects.get(id=content_id)
    current_user = request.user
    likeobj=Like.objects.filter(blog=blogobj,user=current_user).count()
    if(likeobj==0):
        obj=Like()
        obj.user = current_user
        obj.blog = blogobj
        obj.save()

        obj1 = Notifications()
        obj1.senderid = current_user
        obj1.sender = current_user.username
        obj1.recipient = blogobj.user
        obj1.blog = blogobj
        obj1.like = obj
        obj1.save()

    try:
        all_contents = Blog.objects.get(id=content_id)
        all_comments = Comment.objects.filter(blog=content_id)
        if Like.objects.filter(user=request.user,blog=content_id):
            flag=True
        else:
            flag=False
    except Blog.DoesNotExist:
        raise Http404("Blog doesnt exist")
    return render(request, 'blog/all_blogs.html', {'all_blogs': all_contents,'all_comments' : all_comments,'flag':flag})




def add_comment(request,content_id):
    if request.method == 'POST':
        if (request.POST.get('comment')):
            blogobj = Blog.objects.get(id=content_id)
            current_user = request.user

            obj = Comment()
            obj.user = current_user
            obj.blog = blogobj
            obj.comment=request.POST.get("comment")
            obj.save()

            obj1 = Notifications()
            obj1.senderid = current_user
            obj1.sender = current_user.username
            obj1.recipient = blogobj.user
            obj1.blog = blogobj
            obj1.comment = obj
            obj1.save()

            notif_obj=Notifications.objects.filter(recipient=blogobj.user)
            # data = {
            #     'notifications':notif_obj
            # }
            # data = json.dumps(data)
            # print(data)

            # Channel('notification/current_user.id').send({
            #     'notification': json.dumps({
            #         'notifications': notif_obj
            #     })
            # })

            send_channel_msg('notification_'+str(blogobj.user.id), "A new comment")
            # return HttpResponse(data, content_type='application/json')


            try:
                all_contents = Blog.objects.get(id=content_id)
                all_comments = Comment.objects.filter(blog=content_id)
                if Like.objects.filter(user=request.user, blog=content_id):
                    flag = True
                else:
                    flag = False
            except Blog.DoesNotExist:
                raise Http404("Blog doesnt exist")
            return render(request, 'blog/all_blogs.html',
                          {'all_blogs': all_contents, 'all_comments': all_comments, 'flag': flag})
        else:
            return render(request, 'blog/fail.html')


def view_questions(request, content_id):
    try:
        all_questions = Question.objects.filter(blog=content_id)
        all_answers = Answer.objects.filter(blog=content_id)
    except Question.DoesNotExist:
        raise Http404("Blog doesnt exist")
    return render(request, 'blog/view_questions.html',
                  {'all_q': all_questions, 'all_a': all_answers})

def add_answers(request, content_id ,que_id):
    if request.method == 'POST':
        if (request.POST.get('answer')):
            blogobj = Blog.objects.get(id=content_id)
            queobj=Question.objects.get(id=que_id)
            current_user = request.user
            obj = Answer()
            obj.user = current_user
            obj.blog = blogobj
            obj.answer=request.POST.get("answer")
            obj.qid=queobj
            obj.save()
            return render(request, 'blog/user.html')
        else:
            return render(request, 'blog/fail.html')


def ask_questions(request, content_id):
    try:
        all_questions = Question.objects.filter(blog=content_id)
        all_answers = Answer.objects.filter(blog=content_id)

        blogobj = Blog.objects.get(id=content_id)
        user=request.user
        if(user==blogobj.user):
            flag=True
        else:
            flag=False
    except Question.DoesNotExist:
        raise Http404("Blog doesnt exist")
    return render(request, 'blog/add_questions.html',
                  {'all_q': all_questions, 'all_a': all_answers,'flag':flag,'data': zip(all_answers, all_questions)})

def add_questions(request, content_id):
    if request.method == 'POST':
        if (request.POST.get('question')):
            blogobj = Blog.objects.get(id=content_id)
            current_user = request.user
            obj = Question()
            obj.user = current_user
            obj.blog = blogobj
            obj.question=request.POST.get("question")
            obj.save()
            return render(request, 'blog/user.html')
        else:
            return render(request, 'blog/fail.html')





def send_channel_msg(channel_name, msg):
    channel_layer = get_channel_layer()

    # chatSocket.send(JSON.stringify({
    #     'message': msg
    # }));

    async_to_sync(channel_layer.group_send)(channel_name, {
        "type": 'notification_message',
        "text": msg,
    })



