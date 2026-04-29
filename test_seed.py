# -*- coding: utf-8 -*-
import urllib.request, urllib.error

url = 'http://localhost:3000/api/seed'
req = urllib.request.Request(url, data=b'')
req.add_header('Content-Type', 'application/json')

try:
    r = urllib.request.urlopen(req)
    print('OK:', r.read().decode())
except urllib.error.HTTPError as e:
    print('HTTP Error', e.code, ':', e.read().decode())
