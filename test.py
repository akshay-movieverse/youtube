
import requests

data={'data':'rrr'}
r = requests.("http://127.0.0.1:5000/api2/",json={'link':'https://www.youtube.com/watch?v=aVpJGGQHSqc'})
#
print(r.json())
'''
import pytube
from pytube import YouTube

link='https://www.youtube.com/watch?v=aVpJGGQHSqc'
video = YouTube(link)
print(video.streams)
print(video.streams[0].url)
#print(video.extract.get_ytplayer_config)

import pafy
link='https://www.youtube.com/watch?v=aVpJGGQHSqc'
url = "https://www.youtube.com/watch?v=bMt47wvK6u0"
video = pafy.new(link)

#best = video.streams

#print(best[])

best = video.getbest()
print(best.url)
#print(best[-6].url)
'''
