from django.urls import path,re_path
from .views import sign_up,sign_in,home,upload_csv,quiz,submit_answer,result,get_all_word,delete_all_word
urlpatterns = [
    path('', home, name='home'),
    path('register/', sign_up, name='register'),
    path('login/', sign_in, name='login'),
    path('upload/', upload_csv, name='upload'),
    path('quiz/', quiz, name='quiz'),
    path('submit_answer/', submit_answer, name='submit_answer'),
    path('result/', result, name='result'),
    re_path(r'^(?P<key>\d+)/word/$',get_all_word , name='get_all_word'),
    path('delete_all_word',delete_all_word,name='delete_all_word')
]


