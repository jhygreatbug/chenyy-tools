# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render_to_response
from django.http import JsonResponse, HttpResponse

import ctypes
import time
import os

TTS_LIB_NAME = 'libmsc.so'
TTS_LIB_PATH = os.path.join(*(os.path.split(__file__)[:-1] + (TTS_LIB_NAME,)))
tts = ctypes.cdll.LoadLibrary(TTS_LIB_PATH)

MSP_SUCCESS = 0
TTS_LOGIN_PARAMS = 'appid = 59bd4d08, work_dir = .'

TTS_SESSION_BEGIN_PARAMS = 'engine_type = local,voice_name=xiaoyan, text_encoding = UTF8, tts_res_path = fo|res/tts/xiaoyan.jet;fo|res/tts/common.jet, sample_rate = 16000, speed = 50, volume = 50, pitch = 50, rdn = 2'

def view(request):
	return render_to_response('tool/text_to_speech.html')

def tts(request):

	text = '';
	if 'text' not in request.GET:
		return HttpResponse(status = 403)
	else:
		text = request.GET['text']

	result = tts.MSPLogin(None, None, TTS_LOGIN_PARAMS)
	if result != MSP_SUCCESS:
		return HttpResponse(status = 500)

	filename = str(time.time()) + '.wav'
	result = tts.text_to_speech(text, filename, TTS_SESSION_BEGIN_PARAMS);
	if result != MSP_SUCCESS:
		return HttpResponse(status = 500)

	tts.MSPLogout();

	return JsonResponse({ 'src': filename })
