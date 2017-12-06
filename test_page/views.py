# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render_to_response

# Create your views here.

def view(request):
	return render_to_response('test.html')
