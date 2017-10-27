from django.conf.urls import url
from . import views

app_name = 'grading_code'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<classroom_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^quizs/(?P<filter_by>[a-zA_Z]+)/$', views.quizs, name='quizs'),
    url(r'^create_classroom/$', views.create_classroom, name='create_classroom'),
    url(r'^(?P<classroom_id>[0-9]+)/create_quiz/$', views.create_quiz, name='create_quiz'),
    url(r'^(?P<classroom_id>[0-9]+)/delete_quiz/(?P<quiz_id>[0-9]+)/$', views.delete_quiz, name='delete_quiz'),
    url(r'^(?P<classroom_id>[0-9]+)/delete_classroom/$', views.delete_classroom, name='delete_classroom'),
    url(r'^(?P<classroom_id>[0-9]+)/grading/(?P<quiz_id>[0-9]+)/$', views.grading, name='grading'),
    url(r'^(?P<classroom_id>[0-9]+)/grading/(?P<quiz_id>[0-9]+)/result/$', views.grade, name='grade')
]
