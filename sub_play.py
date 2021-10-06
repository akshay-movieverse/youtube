from youtubesearchpython import Playlist,ResultMode
import json


class PlaylistYt():

    def __init__(self,keyword):
        self.key = keyword
    
    def get_result(self):
        playlist = Playlist.get('https://www.youtube.com/playlist?list='+self.key, mode = ResultMode.json)
        return json.loads(playlist)


