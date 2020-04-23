import tweepy
import json
from .models import  UserTweeter
from django.shortcuts import render,redirect
from django.contrib.auth import logout

def get_api_for_tweepy(request):
    """
    now that we have a logged in user that has all the neccassery tokens we simply access this
    data and create an api object to work with twitter
    :param request:
    :return: api object to make tweepy actions.
    """
    consumer_key = "uPpV5uSZ1KsKUen46e8rE1gyT"
    consumer_secret = "i2STWuWUK55z0YF4qzLyAMqxePJO7EyaM2rCSvE2abAotrKWjz"
    cur_user = request.user
    try:
        cur_tweeter = UserTweeter.objects.get(user=cur_user.id)

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(cur_tweeter.access_token, cur_tweeter.access_token_secret)
        api = tweepy.API(auth)
        #if from some reason we dont have the key we try to get it from twitter.
    except:
        redirectURL  = go_to_tweeter(request)
        if (redirectURL != 'fail'):

            return redirect(redirectURL)
        else:

            return go_to_fail(request)

    return api



def go_to_fail(request):
    """
    will delete failed user and redirect to fail page.
    :param request:
    :return:
    """

    return render(request, "tweeterFail.html", {})



def go_to_tweeter(request):
    """
    :param request:
    :return: the url to redirect for twitter auth.
    """
    consumer_key = "uPpV5uSZ1KsKUen46e8rE1gyT"
    consumer_secret = "i2STWuWUK55z0YF4qzLyAMqxePJO7EyaM2rCSvE2abAotrKWjz"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    try:
        #if all is well, will return the url for our app to get user tokens.
        redirect_url = auth.get_authorization_url()

        request.session['request_token'] = auth.request_token['oauth_token']
        return redirect_url
    except tweepy.TweepError:
        print('Error! Failed to get request token.')
        return "fail"



def connect_to_tweeter_helper(request):
    """
    help the proccess of getting and saving tokens for user.
    :param request:
    :return:
    """
    consumer_key = "uPpV5uSZ1KsKUen46e8rE1gyT"
    consumer_secret = "i2STWuWUK55z0YF4qzLyAMqxePJO7EyaM2rCSvE2abAotrKWjz"
    #getting the tweeter tokens of the user just accuired in signUp.
    cur_tweeter = UserTweeter.objects.get(user=request.user.id)
    access_token_secret = cur_tweeter.access_token_secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    # updating the access token after we made the request and have the token secret.
    token = request.session['request_token']
    del request.session['request_token']
    auth.request_token = {'oauth_token': token,
                          'oauth_token_secret': cur_tweeter.access_token_secret}
    auth.get_access_token(access_token_secret)
    #updating the db with the user tokens.
    cur_tweeter.access_token = auth.access_token
    cur_tweeter.access_token_secret = auth.access_token_secret
    cur_tweeter.save()
    set_friends(request)

def set_friends(request):
    api = get_api_for_tweepy(request)
    try:
        friends_names_as_list = [item._json["screen_name"] for item in list(tweepy.Cursor(api.friends).items())]
        cur_tweeter = UserTweeter.objects.get(user=request.user.id)
        cur_tweeter.friends = json.dumps(friends_names_as_list)
        cur_tweeter.save()
    except:
        pass