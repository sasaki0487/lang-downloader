# coding=UTF-8
import os
import ffmpy
import urllib3
import re
import sys

http = urllib3.PoolManager()
addr = raw_input('請輸入直播網址：')
r = http.request('GET', addr)
#https://web.langlive.com/html/share/template2.html?live_id=3669719Y49409glOL
print(r.status)
if r.status != 200 :
    print('獲取網址失敗1')
    sys.exit()
addr = re.search(r'https:\\\/\\\/playback(.*)m3u8',r.data)
if not addr :
    print('獲取網址失敗2')
    sys.exit()
addr = re.sub(r'\\','',addr.group())
print(addr)

ff = ffmpy.FFmpeg(
    inputs = { addr : None},
    outputs = {'out.mp4' : '-c copy'}
)

ff.run()
