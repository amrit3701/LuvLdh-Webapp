# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from decouple import config

import ipdb
@login_required
def home(request):
    #ipdb.set_trace()
    return render(request, 'src/index.html')

import facebook

@login_required
def upload(request):
    url_share = request.POST.get('message')
    social = request.user.social_auth.get(provider='facebook')
    access_token = social.extra_data['access_token']
    import facebook
    graph = facebook.GraphAPI(access_token = config('PAGE_ACCESS_TOKEN'))
    msg = "#hang"
    attachment =  {
       # 'name': 'Link name'
        'link': url_share
       # 'caption': 'Check out this example',
       # 'description': 'This is a longer description of the attachment',
       # 'picture': 'https://www.example.com/thumbnail.jpg'
    }
    print attachment['link']
    status = graph.put_wall_post(msg, attachment)
    return HttpResponse("Check post on <a href='https://www.facebook.com/Song-126210538066873'>Song</a>")

