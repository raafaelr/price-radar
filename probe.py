import re, urllib.request
UA={"User-Agent":"Mozilla/5.0 (Linux; Android 14) Chrome/124 Mobile Safari/537.36"}
for t in ["ryzen%207%207800x3d","ryzen%207%209800x3d"]:
    s=urllib.request.urlopen(urllib.request.Request("https://www.zoom.com.br/search?q="+t,headers=UA),timeout=25).read().decode()
    print(t, sorted(set(re.findall(r'href="(/processador/[^"?#]*x3d[^"?#]*)',s)))[:6])
