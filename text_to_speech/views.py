# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.shortcuts import render_to_response
from django.http import JsonResponse, HttpResponse
from io import BytesIO

import ctypes
import time
import os
import wave

TTS_LIB_NAME = 'libs/x64/libmsc.so'
TTS_LIB_PATH = os.path.join(*(os.path.split(__file__)[:-1] + (TTS_LIB_NAME,)))
msc = ctypes.cdll.LoadLibrary(TTS_LIB_PATH)

MSP_SUCCESS = 0
TTS_LOGIN_PARAMS = b'appid = 59bd4d08, work_dir = .'

TTS_SESSION_BEGIN_PARAMS = 'voice_name = xiaoyan, text_encoding = utf8, sample_rate = 16000, speed = 50, volume = 50, pitch = 50, rdn = 2'


def saveWave(raw_data, _tmpFile = 'test.wav'):
    f = wave.open('/var/www/media/' + _tmpFile, 'w')
    f.setparams((1, 2, 16000, 262720, 'NONE', 'not compressed'))
    f.writeframesraw(raw_data)
    f.close()
    return _tmpFile

def text_to_speech(text, filename):
    text = '测试文本'
    result_c = ctypes.c_int()
    result = 0

    session = msc.QTTSSessionBegin(TTS_SESSION_BEGIN_PARAMS, ctypes.byref(result_c))
    print(session)
    if result_c.value != MSP_SUCCESS:
        return '%d: QTTSSessionBegin failed' % result_c.value

    result = msc.QTTSTextPut(session, text, len(text), None)
    print(text)
    if result != MSP_SUCCESS:
        msc.QTTSSessionEnd(session, 'TextPutError');
        return '%d: QTTSTextPut failed' % result

    audio_len = ctypes.c_uint(0)
    synth_status = ctypes.c_int(0)
    f = BytesIO()
    while True:
        p = msc.QTTSAudioGet(session, ctypes.byref(audio_len), ctypes.byref(synth_status), ctypes.byref(result_c))
        print(p)
        print(audio_len.value)

        if result_c.value != MSP_SUCCESS:
            f.close()
            msc.QTTSSessionEnd(session, 'TextPutError');
            return '%d: QTTSAudioGet failed' % result_c.value

        if p != None:
            buf = (ctypes.c_char * audio_len.value).from_address(p)
            f.write(buf)

        if synth_status.value != 2:
            saveWave(f.getvalue(), filename)
            break

        time.sleep(0.1)

    f.close()
    msc.QTTSSessionEnd(session, 'TextPutError');

    return 0

def view(request):
    return render_to_response('text_to_speech.html')

def tts(request):

    text = '';
    if 'text' not in request.GET:
        return HttpResponse(status = 403)
    else:
        text = request.GET['text']

    result = msc.MSPLogin(None, None, TTS_LOGIN_PARAMS)
    if result != MSP_SUCCESS:
        return HttpResponse(status = 500)

    filename = str(int(time.time())) + '.wav'
    result = text_to_speech(text, filename);
    if result != 0:
        return HttpResponse(status = 500, content = result)

    msc.MSPLogout();

    return JsonResponse({ 'src': filename })
