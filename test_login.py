# -*- coding: utf-8 -*-
import urllib.request, urllib.error, json

url = 'http://localhost:3000/api/auth/login'
data = json.dumps({"phone": "13802531098", "code": "123456"}).encode()
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

try:
    r = urllib.request.urlopen(req)
    print("SUCCESS:", r.read().decode())
except urllib.error.HTTPError as e:
    print("HTTP ERROR:", e.code, e.reason)
    print("Body:", e.read().decode()[:2000])
except Exception as e:
    print("ERROR:", e)
