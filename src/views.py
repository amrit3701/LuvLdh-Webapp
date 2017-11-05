# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from decouple import config
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from wand.image import Image

import ipdb
@login_required
def home(request):
    #ipdb.set_trace()
    return render(request, 'src/index.html')

import facebook

@login_required
def upload_photo(request):
    fi = request.FILES.get('userfile')
    message = request.POST.get('message')
    social = request.user.social_auth.get(provider='facebook')
    access_token = social.extra_data['access_token']
    api = facebook.GraphAPI(access_token)
    user_id = api.get_object('me', fields="id")['id']
    username = api.get_object('me', fields="name")['name']
    profile_link = api.get_object("me", fields="link")['link']
    fs = FileSystemStorage(location=settings.MEDIA_ROOT+"/photography/")
    savedFilename = user_id + "." + fi.name.split('.')[-1]
    filename = fs.save(savedFilename, fi)
    savedFilenameURL = request.get_host() + "/media/photography/" + savedFilename
    graph = facebook.GraphAPI(access_token = config('PAGE_ACCESS_TOKEN'))
    msg = "Username: " + username + "(" + profile_link + ")\nCategory: Photography\n" + "Description: " + message
    attachment =  {
        #'name': 'Link name',
        'link': savedFilenameURL,#"http://lab.gdy.club:7777/media/1580271875386906_pic.png", #savedFilenameURL,
        #'caption': 'Check out this example',
        #'description': 'This is a longer description of the attachment',
        'picture': savedFilenameURL,#"http://lab.gdy.club:7777/media/1580271875386906_pic.png" #savedFilenameURL
    }
    print attachment['link']
    status = graph.put_wall_post(msg, attachment)
    fbpostURL = URLofSharedPost(status)
    return HttpResponse("Check <a href='" + fbpostURL + "'>post</a>")

@login_required
def upload_contentwriting(request):
    fi = request.FILES.get('userfile')
    message = request.POST.get('message')
    social = request.user.social_auth.get(provider='facebook')
    access_token = social.extra_data['access_token']
    api = facebook.GraphAPI(access_token)
    user_id = api.get_object('me', fields="id")['id']
    username = api.get_object('me', fields="name")['name']
    profile_link = api.get_object("me", fields="link")['link']
    fs = FileSystemStorage(location=settings.MEDIA_ROOT+"/contentwriting/")
    savedFilename = user_id + "." + fi.name.split('.')[-1]
    filename = fs.save(savedFilename, fi)
    #ipdb.set_trace()
    savedFilenameURL = request.get_host() + "/media/contentwriting/" + savedFilename
    imageLocation = settings.MEDIA_ROOT + "/contentwriting/" + user_id + ".jpg"
    imageURL = request.get_host() + "/media/contentwriting/" + user_id + ".jpg"
    pdfLocation = fs.base_location+savedFilename
    pdf_to_image(pdfLocation+"[0]", imageLocation)
    graph = facebook.GraphAPI(access_token = config('PAGE_ACCESS_TOKEN'))
    msg = "Username: " + username + "(" + profile_link + ")\nCategory: Photography\n" + "Description: " + message
    attachment =  {
        #'name': 'Link name',
        'link': savedFilenameURL,#"http://lab.gdy.club:7777/media/1580271875386906_pic.png", #savedFilenameURL,
        #'caption': 'Check out this example',
        #'description': 'This is a longer description of the attachment',
        'picture': imageURL,#"http://lab.gdy.club:7777/media/1580271875386906_pic.png" #savedFilenameURL
    }
    status = graph.put_wall_post(msg, attachment)
    fbpostURL = URLofSharedPost(status)
    return HttpResponse("Check <a href='" + fbpostURL + "'>post</a>")


def URLofSharedPost(status):
    post_id = status['id'].split('_')[-1]
    return "https://www.facebook.com/permalink.php?story_fbid="+ post_id +"&id=126210538066873"

def pdf_to_image(pdf_location, img_location):
    with Image(filename=pdf_location) as img:
        img.save(filename=img_location)
