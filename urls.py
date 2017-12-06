"""chenyy_tools URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from index import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.view),
    url(r'^generate_url/', include('generate_url.urls')),
    url(r'^page_diff/', include('page_diff.urls')),
    url(r'^test/', include('test_page.urls')),
    url(r'^tts/', include('text_to_speech.urls')),
]
