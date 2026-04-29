import urllib.request, json

# Login
req = urllib.request.Request(
    'http://localhost:3000/api/auth/login',
    data=json.dumps({'phone': '13802531098', 'code': '123456'}).encode(),
    headers={'Content-Type': 'application/json'}
)
resp = urllib.request.urlopen(req)
data = json.loads(resp.read())
token = data['token']
print('LOGIN OK, token prefix:', token[:20])

# Test daily export
req2 = urllib.request.Request(
    'http://localhost:3000/api/reports/export/daily?year=2026&month=4',
    headers={'Authorization': 'Bearer ' + token}
)
resp2 = urllib.request.urlopen(req2)
content = resp2.read()
print('DAILY EXPORT OK, size:', len(content), 'bytes')

# Test roomtypes export
req3 = urllib.request.Request(
    'http://localhost:3000/api/reports/export/roomtypes?year=2026&month=4',
    headers={'Authorization': 'Bearer ' + token}
)
resp3 = urllib.request.urlopen(req3)
content3 = resp3.read()
print('ROOMTYPES EXPORT OK, size:', len(content3), 'bytes')
