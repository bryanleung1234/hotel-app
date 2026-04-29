# -*- coding: utf-8 -*-
import urllib.request
r = urllib.request.urlopen('http://localhost:3000/api/seed', data=b'')
print(r.read().decode())
