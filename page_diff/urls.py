from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^simple/$', views.simple_diff_view),
    url(r'^simple/d$', views.simple_diff),
]
