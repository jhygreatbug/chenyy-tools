# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render_to_response
from django.http import JsonResponse, HttpResponse

# Create your views here.

def view(request):
    return render_to_response('generate_url.html')
