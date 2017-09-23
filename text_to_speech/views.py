# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render_to_response
from django.http import JsonResponse, HttpResponse

# Create your views here.

def view(request):
	return render_to_response('text_to_speech.html')

def tts(request):
	text = '';
	if 'text' not in request.GET:
		return HttpResponse(status = 403)
	else:
		text = request.GET['text']
	src = 'wav';
	return JsonResponse({ 'src': src })
