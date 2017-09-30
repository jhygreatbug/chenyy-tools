# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render_to_response
from django.http import JsonResponse, HttpResponse
from django.template.context_processors import csrf
from selenium import webdriver
from PIL import Image, ImageChops

import time

def simple_diff_view(request):
	c = {}
	c.update(csrf(request))
	return render_to_response('page_diff/simple.html', c)

def simple_diff(request):

	start_time = time.time()

	try:
		url_l = request.POST['url_l']
		url_r = request.POST['url_r']
	except Exception as e:
		return HttpResponse(status = 403)

	driver = webdriver.PhantomJS()
	driver.set_window_size(1200, 900)
	result = False
	print time.time() - start_time

	driver.get(url_l)
	file_name_l = '%d.png' % int(time.time())
	path_l = '/var/www/media/%s' % file_name_l
	result = driver.save_screenshot(path_l)
	if result != True:
		raise IOError('保存img_l失败！')
	print time.time() - start_time

	driver.get(url_r)
	file_name_r = '%d.png' % int(time.time())
	path_r = '/var/www/media/%s' % file_name_r
	result = driver.save_screenshot(path_r)
	if result != True:
		raise IOError('保存img_r失败！')
	print time.time() - start_time

	img_l = Image.open(path_l)
	img_r = Image.open(path_r)
	print time.time() - start_time

	if img_l.height > img_r.height:
		size = img_l.size
		img_r = img_r.crop((0, 0, size[0], size[1]))
	else:
		size = img_r.size
		img_l = img_l.crop((0, 0, size[0], size[1]))
	img_m = diff(img_l, img_r)
	file_name_m = '%d.png' % int(time.time())
	path_m = '/var/www/media/%s' % file_name_m
	img_m.save(path_m)
	print time.time() - start_time

	driver.quit()

	return JsonResponse({
		'file_name_l': file_name_l,
		'file_name_r': file_name_r,
		'file_name_m': file_name_m,
		})

def diff(img_l, img_r, color=(220, 50, 50, 0.7), alpha=0.7):
	size = img_l.size
	img_m = Image.new('RGBA', size, (255, 255, 255, 255))
	pixel_l = img_l.load()
	pixel_r = img_r.load()
	alpha1 = alpha
	# 半透明混合算法：
	# 背景图为A，半透明图为B，透过B去看A得到的图像是C
	# C = (1 - alpha) * B + alpha * A
	# cal = lambda x1, x2, alpha : int(x1 * alpha + x2 * (1 - alpha))
	for i in range(size[0]):
		for j in range(size[1]):
			pl = pixel_l[i, j]
			pr = pixel_r[i, j]
			r = pl[0]
			g = pl[1]
			b = pl[2]
			rr = pr[0]
			gr = pr[1]
			br = pr[2]
			if r != rr or g != gr or b != br:
				alpha2 = color[3]
				r = int(alpha2 * (alpha1 * pl[0] + (1 - alpha1) * pr[0]) + (1 - alpha2) * color[0])
				g = int(alpha2 * (alpha1 * pl[1] + (1 - alpha1) * pr[1]) + (1 - alpha2) * color[1])
				b = int(alpha2 * (alpha1 * pl[2] + (1 - alpha1) * pr[2]) + (1 - alpha2) * color[2])
				# r = cal(cal(pl[0], pr[0], 0.5), color[0], color[3])
				# g = cal(cal(pl[1], pr[1], 0.5), color[1], color[3])
				# b = cal(cal(pl[2], pr[2], 0.5), color[2], color[3])
			img_m.putpixel((i, j), (r, g, b, 255))
	return img_m
