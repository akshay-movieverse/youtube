import sys

if sys.version_info[0] == 2:
    from urllib import urlencode, urlopen
else:
    from urllib.request import urlopen
    from urllib.parse import urlencode
import io

class RequestHandler:
    def request(self):
        try:
            query = urlencode({
                "search_query": self.keyword,
                "page": self.offset,
                "sp": self.searchPreferences
            })
            request = "https://www.youtube.com/results" + "?" + query
            response = urlopen(request).read()
            self.page = response.decode('utf_8')

            if self.page[0:29] == '  <!DOCTYPE html><html lang="':
                self.validResponse = True

        except: 
            self.networkError = True


class ScriptHandler:
    def scriptResponseHandler(self):     
        self.links = []
        self.ids = []
        self.titles = []
        self.thumbnails = []
        self.count = []
        self.channel = []

        self.pageSource = self.page.split('":"')

        for index in range(0, len(self.pageSource) - 1, 1):
            
            ''' Setting Playlist ID and link. '''

            if self.pageSource[index][-10:] == 'playlistId':

                if self.pageSource[index+1].split('"')[0] not in self.ids:
                    if self.pageSource[index+1].split('"')[0] == "WL":
                        pass
                    else:
                        self.ids+=[self.pageSource[index+1].split('"')[0]]
                        self.links+=["https://www.youtube.com/playlist?list=" + self.pageSource[index+1].split('"')[0]]
 
            ''' Setting Playlist Title. '''

            if self.pageSource[index][-20:] == '"title":{"simpleText' and self.pageSource[index+1][-3:] == 'url':
                self.titles+=[self.pageSource[index+1].split('"},"')[0].replace("\\u0026", "&")]


            self.thumb=[]
            if self.pageSource[index][-34:] == '"thumbnails":[{"thumbnails":[{"url':
                temp=index
                while self.pageSource[temp][-10:] != 'videoCount':
                    if 'https://i.ytimg.com' in self.pageSource[temp]:
                        self.thumb.append(self.pageSource[temp].split('","')[0].replace("\\u0026", "&"))
                    temp=temp+1
                if self.pageSource[temp+1][-41:] == 'navigationEndpoint":{"clickTrackingParams':
                    self.count.append(self.pageSource[temp+1].split('","')[0])
                self.thumbnails.append(self.thumb)
                #print(self.thumb)
                self.thumb=[]

                        
            if self.pageSource[index][-33:]=='"shortBylineText":{"runs":[{"text':
                self.channel.append(self.pageSource[index+1].split('","')[0])


            if len(self.titles) > self.max_results and len(self.ids) > self.max_results:
                max_results = min(len(self.titles), len(self.ids))
                self.titles = self.titles[0:max_results]
                self.ids = self.ids[0:max_results]
                self.links = self.links[0:max_results]
                self.thumbnails = self.thumbnails[0:max_results]
                self.count = self.count[0:max_results]
                self.channel = self.channel[0:max_results]
                break


import json

class SearchPlaylists(RequestHandler, ScriptHandler):
    '''
    Search for playlists in YouTube.
    Parameters
    ----------
    keyword : str
        Used as a query to search for playlists in YouTube.
    offset : int, optional
        Offset for result pages on YouTube. Defaults to 1.
    mode : str
        Search result mode. Can be 'json', 'dict' or 'list'.
    maxResults : int, optional
        Maximum number of playlist results. Defaults to 20.
    Methods
    -------
    result()
        Returns the playlists fetched from YouTube by search().
    '''
    networkError = False
    validResponse = False

    def __init__(self, keyword, offset = 1, mode = "list", max_results = 20):

        self.offset = offset
        self.mode = mode
        self.keyword = keyword
        self.max_results = max_results
        self.searchPreferences = "EgIQAw%3D%3D"
        self.main()

    def main(self):
        self.request()
        if self.networkError:
            self.networkError = True
        else:
            self.scriptResponseHandler()

    def result(self):
        '''
        Returns
        -------
        None, str, dict, list
            Returns playlist results from YouTube. Returns None, if network error occurs.
        '''
        if self.networkError:
            return None

        else:

            result = []

            if self.mode in ["json", "dict"]:

                for index in range(len(self.ids)):
                    result_index = {
                        "index": index,
                        "id": self.ids[index],
                        "link": self.links[index],
                        "title": self.titles[index],
                        "count": self.count[index],
                        "channel": self.channel[index],
                        "thumbnails": self.thumbnails[index],



                    }
                    result+=[result_index]

                if self.mode == "json":
                    return json.dumps({"search_result": result}, indent=4)
                else:
                    return {"search_result": result}
            
            elif self.mode == "list":
                
                for index in range(len(self.ids)):
                    list_index=[
                        index,
                        self.ids[index],
                        self.links[index],
                        self.titles[index],
                        self.thumbnails[index],
                        self.count[index],
                        self.channel[index],
                    ]
                    result+=[list_index]
                
                return result


