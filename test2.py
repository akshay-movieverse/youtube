import requests
from bs4 import BeautifulSoup 

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
}

s = requests.session()
r = s.get("https://www.youtube.com/",headers = headers)

data = r.text

with open('wix.txt','a',encoding='utf-8') as f:
    f.write(data)


soup = BeautifulSoup(data,'html.parser')
st=soup.findAll('a')
print(st)
