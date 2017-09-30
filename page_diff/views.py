# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render_to_response
from django.http import JsonResponse, HttpResponse
from django.template.context_processors import csrf
from selenium import webdriver

import time

def simple_diff_view(request):
	c = {}
	c.update(csrf(request))
	return render_to_response('page_diff/simple.html', c)

def simple_diff(request):
	try:
		url_l = request.POST['url_l']
		url_r = request.POST['url_r']
	except Exception as e:
		return HttpResponse(status = 403)

	driver = webdriver.PhantomJS()
	driver.set_window_size(1200, 900)

	driver.get(url_l)
	print driver.title
	path_l = '%d.png' % int(time.time())
	driver.save_screenshot('/var/www/media/%s' % path_l)
	print path_l

	driver.get(url_r)
	print driver.title
	path_r = '%d.png' % int(time.time())
	driver.save_screenshot('/var/www/media/%s' % path_r)
	print path_r

	driver.quit()

	return JsonResponse({
		'path_l': path_l,
		'path_r': path_r,
		})

def 
