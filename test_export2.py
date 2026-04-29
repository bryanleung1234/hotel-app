import urllib.request, json, urllib.error

try:
    # Login
    req = urllib.request.Request(
        'http://localhost:3000/api/auth/login',
        data=json.dumps({'phone': '13802531098', 'code': '123456'}).encode(),
        headers={'Content-Type': 'application/json'}
    )
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    token = data['token']
    print('LOGIN OK')

    # Test roomtypes export - first let's see the actual error
    from urllib.error import HTTPError
    try:
        req3 = urllib.request.Request(
            'http://localhost:3000/api/reports/export/roomtypes?year=2026&month=4',
            headers={'Authorization': 'Bearer ' + token}
        )
        resp3 = urllib.request.urlopen(req3)
        content3 = resp3.read()
        print('ROOMTYPES EXPORT OK, size:', len(content3), 'bytes')
    except HTTPError as e:
        print('HTTP Error:', e.code, e.read().decode()[:500])

except Exception as ex:
    print('Error:', ex)
