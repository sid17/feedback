from django.conf.urls import patterns, url
from gui import views

urlpatterns = patterns('',
    url(r'playTraj/', views.playTraj, name='playTraj'),
    url(r'saveSeq/', views.saveSeq, name='playTraj'),
)
