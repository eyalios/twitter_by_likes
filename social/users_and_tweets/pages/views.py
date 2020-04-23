import tweepy
from django.shortcuts import render,redirect
from django.http import JsonResponse
from users_and_tweets.userManager.methods import get_api_for_tweepy
from ..userManager.models import UserTweeter
from django.http import HttpResponse
from ..userManager.methods import set_friends,go_to_fail,go_to_tweeter
import json
import operator
from django.core import serializers

# Create your views here.
def home_view(request,*args ,**kwargs):
    return render(request, "home.html", {})

def get_ids_by_likes(request):
    """
    return jsonresponse of a list with tweet ids
    :param request:
    :return:
    """
    api = get_api_for_tweepy(request)
    target = request.GET["friend"]
    try:
        #generetor of 100 tweets by requested user.
        gen_of_Tweets_by_requested_user = tweepy.Cursor(api.user_timeline, id=target).items()
        lst = []
        i = 0
        #we collect the amont of likes and pair them with id and sort by likes.
        for item in gen_of_Tweets_by_requested_user:
            lst.append((item._json['favorite_count'], item._json["id"]))
            i += 1
            if (i > 100): break
        lst.sort(key=operator.itemgetter(0), reverse=True)
        #creating a list of the ids affter sorting and sending them to client.
        lst_of_id = [str(item[1]) for item in lst]
        return JsonResponse(lst_of_id, safe=False)

    except Exception as twitter_issue:
        err_code = twitter_issue.response.status_code
        #if we could not find user on twitter.
        if(err_code == 404 or err_code == 403):
            set_friends(request)
            return JsonResponse(["-1","it seems @"+target+ " does not exist or you have no " \
                                      "permission to view his tweets"], safe=False)
        if(err_code == 401):
            #if the user somehow revoked app access.
            res = go_to_tweeter(request)
            if (res != 'fail'):
                msg ="it seems like this user does not have twitter app premissions press " \
                     "<a href="+res+">here to redirect to twitter auth</a> and fix this"
            else:
                msg = "somthing is very wrong"
            return JsonResponse(["-1", msg],safe=False)
            #unotherized will send us to give permission to app.









def display_view(request, *args,**kwargs):
    """
    page where we display the tweets
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    print(request.GET)



    if("friend" in request.GET):
        #if this request included a friend to find request will procces and return json with tweet IDS
        return get_ids_by_likes(request)

    #if this page is loaded with no request we will just send the list of
    #pepole this user follows on twitter

    cur_user = request.user
    try:
        user_friends = UserTweeter.objects.get(user=cur_user.id).friends
        data = json.loads(user_friends)
        ctx = {"user_friends": data}

        return render(request, "display.html", ctx)
    except:
        return redirect(go_to_tweeter(request))




