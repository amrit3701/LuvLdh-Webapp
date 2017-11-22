from decouple import config
from django.conf import settings
import facebook
import requests
import re
import json


def getMaximiumLikes(api, posts):
    first_count = 0
    second_count = 0
    first_count_post = None
    second_count_post = None
    first_count_username = None
    second_count_username = None
    first_count_post_img = None
    second_count_post_img = None
    first_count_user_profile = None
    second_count_user_profile = None
    first_count_post_data = None
    second_count_post_data = None
    for post in posts:
        response = requests.get("https://graph.facebook.com/v2.11/" + post["id"] + "?fields=reactions.summary(true).limit(0),permalink_url&access_token=" + config('PAGE_ACCESS_TOKEN'))
        response = response.json()
        likes = response["reactions"]["summary"]["total_count"]
        if likes > second_count:
            if likes > first_count:
                first_count = likes
                first_count_post_data = post
                first_count_post = response["permalink_url"]
            else:
                second_count = likes
                second_count_post_data = post
                second_count_post = response["permalink_url"]
    if first_count_post_data is not None:
        first_count_username = re.search('Username: (.*)\n', first_count_post_data["message"]).group(1)
        first_count_user_profile = re.search('\n(.*)\nCategory:', first_count_post_data["message"]).group(1)
        first_count_post_img = api.get_object(first_count_post_data["id"], fields="link")["link"]
    if second_count_post_data is not None:
        second_count_username = re.search('Username: (.*)\n', second_count_post_data["message"]).group(1)
        second_count_user_profile = re.search('\n(.*)\nCategory:', second_count_post_data["message"]).group(1)
        second_count_post_img = api.get_object(second_count_post_data["id"], fields="link")["link"]
    return {1: {"image": first_count_post_img,
                "username": first_count_username,
                "likes": first_count,
                "user_profile": first_count_user_profile,
                "post": first_count_post},
            2: {"image": second_count_post_img,
                "username": second_count_username,
                "likes": second_count,
                "user_profile": second_count_user_profile,
                "post": second_count_post}}

def updateContestWinners():
    access_token = config('PAGE_ACCESS_TOKEN')
    api = facebook.GraphAPI(access_token)
    posts = api.get_object("me", fields="posts")['posts']['data']
    PhotographyPosts = []
    ContentWritingPosts = []
    SouvenirPosts = []
    json_dic = {}
    for post in posts:
        try:
            if "Category: Photography Contest #LuvLdh #sscsLdh" in post['message']:
                PhotographyPosts.append(post)
            elif "Content Writing Contest #LuvLdh #sscsLdh" in post['message']:
                ContentWritingPosts.append(post)
            elif "Souvenir Contest #LuvLdh #sscsLdh" in post['message']:
                SouvenirPosts.append(post)
        except KeyError:
            continue
    json_dic["PhotographyContest"] = getMaximiumLikes(api, PhotographyPosts)
    json_dic["ContentWritingContest"] =  getMaximiumLikes(api, ContentWritingPosts)
    json_dic["SouvenirContest"] =  getMaximiumLikes(api, SouvenirPosts)
    with open(settings.MEDIA_ROOT + '/WinnersData.json', 'w') as outfile:
        json.dump(json_dic, outfile)
