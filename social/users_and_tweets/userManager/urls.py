from django.urls import path
from .views import *
urlpatterns = [
    path('signUp/', signUP_view, name='signUp'),
    path('redirect/', redirect_view, name ='redirect'),
    path('login/', login_view, name ='login'),
    path('logout/', logout_view, name ='logout'),
]
