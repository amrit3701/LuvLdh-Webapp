# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from decouple import config
from django.core.files.storage import FileSystemStorage



import ipdb
@login_required
def home(request):
    #ipdb.set_trace()
    return render(request, 'src/index.html')

import facebook

@login_required
def upload(request):
    social = request.user.social_auth.get(provider='facebook')
    access_token = social.extra_data['access_token']
    api = facebook.GraphAPI(access_token)
    user_id = api.get_object('me', fields="id")['id']
    url_share = request.POST.get('message')
    fi = request.FILES.get('userfile')
    fs = FileSystemStorage()
    savedFilename = user_id + "_pic." + fi.name.split('.')[-1]
    filename = fs.save(savedFilename, fi)
    savedFilenameURL = request.get_host() + "/media/" + savedFilename
#    ipdb.set_trace()
    graph = facebook.GraphAPI(access_token = config('PAGE_ACCESS_TOKEN'))
    msg = "#hang"
    attachment =  {
        'name': 'Link name',
        'link': savedFilenameURL,
       'caption': 'Check out this example',
       'description': 'This is a longer description of the attachment',
       'picture': savedFilenameURL
    }
    print attachment['link']
    status = graph.put_wall_post(msg, attachment)
    return HttpResponse("Check post on <a href='https://www.facebook.com/Song-126210538066873'>Song</a>")

