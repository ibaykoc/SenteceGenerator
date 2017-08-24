from urllib.request import Request, urlopen

req = Request('http://kbbi.co.id/daftar-kata', headers={'User-Agent': 'Mozilla/5.0'})

content = urlopen(req).read()

print (content)