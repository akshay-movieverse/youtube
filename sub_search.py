
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
            request = "https://www.youtube.in/watch?v="+ self.keyword
            response = urlopen(request).read()
            self.page = response.decode('utf_8')

            if self.page[0:29] == '  <!DOCTYPE html><html lang="':
                self.validResponse = True

        except: 
            self.networkError = True

class ScriptHandler:
    def scriptResponseHandler(self):     
        self.views = []
        self.ids = []
        self.titles = []
        self.thumbnails = []
        self.time = []
        self.channel = []
        self.pubtime = []
        self.chthumbnails = []
        self.desc = []
        self.pubdate = []
        self.sviews = []
        self.pageSource = self.page.split('":"')

        for index in range(0, len(self.pageSource) - 1, 1):


            if self.pageSource[index][-51:]  == '"videoPrimaryInfoRenderer":{"title":{"runs":[{"text':
                self.sviews.append(self.pageSource[index+2].split('"')[0])
                

            self.chthumb=[]
            if self.pageSource[index][-93:]  == '"videoSecondaryInfoRenderer":{"owner":{"videoOwnerRenderer":{"thumbnail":{"thumbnails":[{"url':
                if 'https://yt3.ggpht' in self.pageSource[index+1].split('"')[0]:
                    self.chthumb.append(self.pageSource[index+1].split('"')[0])
                    if 'https://yt3.ggpht' in self.pageSource[index+2].split('"')[0]:
                        self.chthumb.append(self.pageSource[index+2].split('"')[0])
                        if 'https://yt3.ggpht' in self.pageSource[index+3].split('"')[0]:
                            self.chthumb.append(self.pageSource[index+3].split('"')[0])
                self.chthumbnails.append(self.chthumb)
                self.chthumb = []

            if self.pageSource[index][-25:]  == '},"dateText":{"simpleText':
                self.pubdate.append(self.pageSource[index+1].split('"')[0])
                

            ''' Setting Playlist ID and link. '''
            if self.pageSource[index][-32:] =='"compactVideoRenderer":{"videoId':                                       # Video Id
                self.ids.append(self.pageSource[index+1].split('"')[0])
                self.thumb=[]

                #print(self.pageSource[index+1].split('"')[0])
                if self.pageSource[index+1][-19:] =='"thumbnails":[{"url':                           # Thumbnails 2
                    if 'https://i.ytimg.com' in self.pageSource[index+2].split('"')[0]:
                        self.thumb.append(self.pageSource[index+2].split('"')[0])
                        if 'https://i.ytimg.com' in self.pageSource[index+3].split('"')[0]:
                            self.thumb.append(self.pageSource[index+3].split('"')[0])
                    self.thumbnails.append(self.thumb)
                    #print(self.pageSource[index+2].split('"')[0])
                    self.thumb=[]
            
            if self.pageSource[index][-53:] =='"title":{"accessibility":{"accessibilityData":{"label':                       # Title 
                if self.pageSource[index+2].split('"')[0] not in self.titles:
                    self.titles.append(self.pageSource[index+2].split('"')[0])
                    #print(self.pageSource[index+2].split('"')[0])
                
                
            if self.pageSource[index][-32:] =='"longBylineText":{"runs":[{"text':                       # Channel name
                self.channel.append(self.pageSource[index+1].split('"')[0])
                #print(self.pageSource[index+1].split('"')[0])

            if self.pageSource[index][-32:] == '"publishedTimeText":{"simpleText':                      # published time and views
                #print(self.pageSource[index+1].split('"')[0])
                if self.pageSource[index+1][-28:] == '"viewCountText":{"simpleText':
                        self.pubtime.append(self.pageSource[index+1].split('"')[0])
                        #print(self.pageSource[index+1].split('"')[0])
                        self.time.append(self.pageSource[index+4].split('"')[0])
                        #print(self.pageSource[index+4].split('"')[0])
                        self.views.append(self.pageSource[index+4].split('"')[0])
            if self.pageSource[index][-33:] == '"shortViewCountText":{"simpleText':
                if self.pageSource[index+1].split('"')[0] not in self.views:
                    self.views.append(self.pageSource[index+1].split('"')[0])
                    #print(self.pageSource[index+1].split('"')[0]) 
            if  self.pageSource[index][-76:] == '"microformat":{"playerMicroformatRenderer":{"thumbnail":{"thumbnails":[{"url':
                temp=index

                while self.pageSource[temp][-17:] != '},"trackingParams':
                    if self.pageSource[temp][-26:] == '"description":{"simpleText':
                        self.desc.append(self.pageSource[temp+1].split('"}')[0])
                    temp=temp+1

 



        self.max_results = len(self.views)
        
        if len(self.titles) > self.max_results: #and len(self.thumbnails) > self.max_results:
            max_results = len(self.views)
            self.titles = self.titles[0:max_results]
            self.ids = self.ids[0:max_results]
            self.views = self.views[0:max_results]
            self.thumbnails = self.thumbnails[0:max_results]
            self.time = self.time[0:max_results]
            self.channel = self.channel[0:max_results]
            self.pubtime = self.pubtime[0:max_results]



import json

class Sub(RequestHandler, ScriptHandler):
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

    def __init__(self, keyword , offset = 1, mode = "json", max_results = 20):

        self.offset = offset
        self.mode = mode
        self.max_results = max_results
        self.keyword = keyword
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
                        "views": self.views[index],
                        "title": self.titles[index],
                        "thumbnails": self.thumbnails[index],
                        "time": self.time[index],
                        "channel": self.channel[index],
                        "pubtime": self.pubtime[index],
                        
                    }
                    result+=[result_index]

                if self.mode == "json":
                    return json.dumps({"search_result": result, 'meta': {'channel' :self.chthumbnails, 'description': self.desc , 'publishDate':self.pubdate, 'sviews': self.sviews} }, indent=4)
                else:
                    return {"search_result": result, 'meta': {'channel' :self.chthumbnails, 'description': self.desc , 'publishDate':self.pubdate, 'sviews': self.sviews}}
            
            elif self.mode == "list":
                
                for index in range(len(self.ids)):
                    list_index=[
                        index,
                        self.ids[index],
                        self.views[index],
                        self.titles[index],
                        self.thumbnails[index],
                        self.time[index],
                        self.channel[index],
                        self.pubtime[index],
                    ]
                    result+=[list_index]
                
                return result , {'channel' :self.chthumbnails, 'description': self.desc , 'publishDate':self.pubdate,'sviews': self.sviews}

