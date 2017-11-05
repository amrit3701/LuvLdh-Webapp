# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from decouple import config
from django.core.files.storage import FileSystemStorage
from django.conf import settings


#import ipdb
@login_required
def home(request):
    #ipdb.set_trace()
    return render(request, 'src/index.html')

import facebook

@login_required
def upload(request):
    fi = request.FILES.get('userfile')
    message = request.POST.get('message')
    social = request.user.social_auth.get(provider='facebook')
    access_token = social.extra_data['access_token']
    api = facebook.GraphAPI(access_token)
    user_id = api.get_object('me', fields="id")['id']
    username = api.get_object('me', fields="name")['name']
    url_share = request.POST.get('message')
    #ipdb.set_trace()
    fs = FileSystemStorage(location=settings.MEDIA_ROOT+"/profile")
    savedFilename = user_id + "_pic." + fi.name.split('.')[-1]
    filename = fs.save(savedFilename, fi)
    savedFilenameURL = request.get_host() + "/media/profile" + savedFilename
    #ipdb.set_trace()
    graph = facebook.GraphAPI(access_token = config('PAGE_ACCESS_TOKEN'))
    msg = "Username: " + username + "\nCategory: Photography\n" + "Description: " + message
    attachment =  {
        #'name': 'Link name',
        'link': savedFilenameURL#"http://lab.gdy.club:7777/media/1580271875386906_pic.png", #savedFilenameURL,
        #'caption': 'Check out this example',
        #'description': 'This is a longer description of the attachment',
        'picture': savedFilenameURL#"http://lab.gdy.club:7777/media/1580271875386906_pic.png" #savedFilenameURL
    }
    print attachment['link']
    status = graph.put_wall_post(msg, attachment)
    fbpostURL = URLofSharedPost(status)
    return HttpResponse("Check <a href='" + fbpostURL + "'>post</a>")

def URLofSharedPost(status):
    post_id = status['id'].split('_')[-1]
    return "https://www.facebook.com/permalink.php?story_fbid="+ post_id +"&id=126210538066873"

def URLofUserProfile(user_id):
    return "https://www.facebook.com/profile.php?id=" + user_id
