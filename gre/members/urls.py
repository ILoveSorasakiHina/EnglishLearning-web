from django.urls import path, re_path
from .views import (
    sign_up, sign_in, home, upload_csv, quiz, submit_answer, 
    result, get_all_word, delete_all_word, quiz2, profile, 
    update, authorize, callback, input_word,ecpay_view
)

urlpatterns = [
    path('', home, name='home'),
    path('register/', sign_up, name='register'),
    path('login/', sign_in, name='login'),
    path('profile/', profile, name='profile'),
    path('profile/update/', update, name='update'),
    path('words/', input_word, name='input_word'),
    re_path(r'^(?P<key>\d+)/words/$', get_all_word, name='get_all_word'),
    path('words/delete/', delete_all_word, name='delete_all_word'),
    path('quiz/', quiz, name='quiz'),
    path('quiz/submit/', submit_answer, name='submit_answer'),
    path('quiz/result/', result, name='result'),
    path('quiz2/', quiz2, name='quiz2'),
    path('oauth2/authorize/', authorize, name='authorize'),
    path('oauth2/callback/', callback, name='callback'),
    path('upload/', upload_csv, name='upload'),
    path('ecpay/', ecpay_view, name= 'ecpay_view'),

]
