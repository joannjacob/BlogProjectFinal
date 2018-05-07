from django.shortcuts import render
from django.http import HttpResponse
from django.utils.safestring import mark_safe
import json

def index(request):
    #return HttpResponse("hello")
    return render(request, 'chat/index.html', {})

def room(request, user_name,room_name):
    return render(request, 'chat/room.html', {
        'user_name_json': mark_safe(json.dumps(user_name)),
        'room_name_json': mark_safe(json.dumps(room_name))
    })