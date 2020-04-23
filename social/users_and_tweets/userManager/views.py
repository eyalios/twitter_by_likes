from django.shortcuts import render,redirect
from .forms import  UserSignUP
import tweepy
import json
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from .methods import go_to_tweeter,go_to_fail,connect_to_tweeter_helper,set_friends
from .models import  UserTweeter


def signUP_view(request,*args ,**kwargs):
   """
    signup page, if succesful will also redirct to twitter.
    :param request:
    :param args:
    :param kwargs:
    :return:
   """
   if(request.method =='POST'):
        form = UserCreationForm(request.POST)
        if(form.is_valid()):
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user =authenticate(username=username, password = password)
            login(request,user)
            #request.session['username'] = request.POST['username']
            #if form was submitted and cleared save it, and redirect to next page.

            res = go_to_tweeter(request)
            if(res!='fail'):

                return redirect(res)
            else:

                return  go_to_fail(request)
        else:

            print(form.errors)
            return render(request,"signUP.html",{'form' :  form})

   else:#if this a get request
        form = UserCreationForm()
        contex = {
            'form': form
        }
        return render(request,"signUP.html",contex)



def login_view(request,*args ,**kwargs):
    """

    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    if(request.method == 'GET'):
        form =  AuthenticationForm(data = request.POST)
        print("printed from get")
        print(form.error_messages)
        return render(request,"login.html",{"form": form})
    else:
        print(request.POST)
        form = AuthenticationForm(request,data = request.POST)
        if form.is_valid():
            print("its valid")
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user =authenticate(username=username, password = password)
            login(request,user)
            #making sure that user has twitter tokens.
            if not UserTweeter.objects.get(user=request.user.id):
                res = go_to_tweeter(request)
                if (res != 'fail'):
                    return redirect(res)
                else:

                    return go_to_fail(request)
            #get friends list and update for user.
            set_friends(request)
            return redirect( request.build_absolute_uri('/'))
        else:
            print("not valid")
            print(form.error_messages)
            return render(request, "login.html", {'form': form})


def logout_view(request):
    """
    logsout and goes back to home page.
    :param request:
    :return:
    """
    if(request.user.is_authenticated):
        logout(request)
    return redirect( request.build_absolute_uri('/'))


def redirect_view(request,*args ,**kwargs):
    """
    this page is when returning from twitter aprroval. will set the required values of
    the user signing up.
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    if(request.method == 'POST'):
        print("error")
    elif not ('oauth_token' in request.GET):
        #if the user did not let us get tokens for his tweeter.
            return go_to_fail(request)
    else:
        #if this was a get request and we recived a valid token form twitter
        #update user data.
        cur_user = request.user
        try:
            cur_tweeter = UserTweeter.objects.get(user=cur_user.id)
        except:
             cur_tweeter  = UserTweeter()
             cur_tweeter.user = cur_user

        cur_tweeter.access_token_secret = request.GET['oauth_verifier']
        cur_tweeter.save()


    #set tokens for user
    connect_to_tweeter_helper(request)
    return redirect(request.build_absolute_uri('/'))

