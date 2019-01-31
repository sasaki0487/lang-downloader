# coding=UTF-8
import os.path
import ffmpy
import urllib3
import re
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()
addr = input('請輸入直播網址：')
r = http.request('GET', addr)
#https://web.langlive.com/html/share/template2.html?live_id=3669719Y49409glOL
print(r.status)
if r.status != 200 :
    print('獲取網址失敗1')
    sys.exit()
start = r.data.decode('utf-8').find('nickname\":\"')
end = r.data.decode('utf-8').find('\"',start+11)
nickname = r.data.decode('utf-8')[start+11:end]

start = r.data.decode('utf-8').find('title\":\"')
end = r.data.decode('utf-8').find('\"',start+8)
title = r.data.decode('utf-8')[start+8:end]

addr = re.search(r'https:\\\/\\\/playback(.*)m3u8',r.data.decode('utf-8'))
if not addr :
    print('獲取網址失敗2')
    sys.exit()
addr = re.sub(r'\\','',addr.group())

start = addr.find('--')
end = addr.find('.m3u8')
date = addr[start+2:end]
print(addr)
out = date + '.mp4'
name = nickname + '_' + title + '_' + date + '.mp4'
name = re.sub(r'[\\\/:\*\?<>|]','',name)
print(name) 

ff = ffmpy.FFmpeg(
    inputs = { addr : None},
    outputs = { out : '-c copy'}
)

ff.run()

if os.path.isfile(out):
	os.rename(out, name)
else :
	print('轉換錯誤')
	sys.exit()
