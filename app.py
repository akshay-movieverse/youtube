from flask import Flask,jsonify, request 
from flask_restful import Api, Resource
from youtubesearchpython import SearchVideos
from search_play import SearchPlaylists as sp
from home_search import Home
import Homie as hm
from sub_search import Sub
from flask_cors import CORS, cross_origin
import json
from json import JSONEncoder
import pafy
from sub_play import PlaylistYt

import urllib.parse
#query = {'client': {'hl': 'en', 'gl': 'US', 'visitorData': 'CgtlaGZ2TThzZGc3cyiztpX8BQ%3D%3D', 'userAgent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/84.0.4147.89 Safari/537.36,gzip(gfe)', 'clientName': 'WEB', 'clientVersion': '2.20201008.04.01', 'osName': 'X11', 'osVersion': '0', 'browserName': 'HeadlessChrome', 'browserVersion': '84.0.4147.89', 'screenWidthPoints': 800, 'screenHeightPoints': 600, 'screenPixelDensity': 1, 'screenDensityFloat': 1, 'utcOffsetMinutes': -240, 'userInterfaceTheme': 'USER_INTERFACE_THEME_LIGHT', 'connectionType': 'CONN_CELLULAR_4G'}, 'request': {'sessionId': '6883007880370077786', 'internalExperimentFlags': [], 'consistencyTokenJars': []}, 'adSignalsInfo': {'consentBumpParams': {'consentHostnameOverride': 'https://www.youtube.com', 'urlOverride': ''}}, 'user': {}, 'clientScreenNonce': 'MC40NDIxNjYyNzczNjYxMTk3', 'clickTracking': {'clickTrackingParams': 'CBwQ8eIEIhMIxOf41omx7AIVS7icCh1q0gqI'}}
##v=urllib.parse.quote(query)
#print(v)
#meta={"adSignalsInfo":{"consentBumpParams":{"consentHostnameOverride":"https://www.youtube.com","urlOverride":""}},"clickTracking":{"clickTrackingParams":"CBwQ8eIEIhMImMzPgZqx7AIVwu1gCh0TngW2"},"client":{"browserName":"HeadlessChrome","browserVersion":"84.0.4147.89","clientName":"WEB","clientVersion":"2.20201008.04.01","connectionType":"CONN_CELLULAR_4G","gl":"US","hl":"en","osName":"X11","osVersion":"0","screenDensityFloat":1,"screenHeightPoints":600,"screenPixelDensity":1,"screenWidthPoints":800,"userAgent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/84.0.4147.89 Safari/537.36,gzip(gfe)","userInterfaceTheme":"USER_INTERFACE_THEME_LIGHT","utcOffsetMinutes":-240,"visitorData":"CgtMWXRyY3NwSHRmWSjT2JX8BQ%3D%3D"},"clientScreenNonce":"MC45OTM5ODI5NTA1ODQ1OTU2","request":{"consistencyTokenJars":[],"internalExperimentFlags":[],"sessionId":"6883026709901351894"},"user":{}}
#url = "https://www.youtube.com/watch?v=pr-4GbR4DpQ"

app = Flask(__name__)

app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy   dog'
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/api3": {"origins": "*"}})

api = Api(app)

@app.route("/")
@cross_origin()
def helloWorld():
  return "Hello, cross-origin-world!"


link_data={'link_360': 0 , 'link_480':0 ,   'link_720': 0, 'link_1080': 0 ,'link_m4a': 0}

@app.route('/api3', methods=['POST'])
@cross_origin(origin='*')#,headers=['Content- Type','Authorization'])
def foo():
    try:
        data = request.get_json('data')
        link=data['link']
        #print(link)
        v = pafy.new(link)
        for s in v.allstreams:
            if ('x360' in s.resolution):
                    #print(s)
                link_data['link_360']=s.url
            elif ('x480' in s.resolution):
                link_data['link_480']=s.url
            elif ('x720' in s.resolution):
                link_data['link_720']=s.url
            elif ('x1080' in s.resolution):
                link_data['link_1080']=s.url
            elif ('m4a' in s.extension):
                link_data['link_m4a']=s.url
            else:
                pass

            #data = request.json('data')
            #data = request.args.get('data')     # status code 
            #print(data)

        return jsonify(link_data)    
    #return "HELL"
    except:
        return "FAIL"



class One(Resource):

    def get(self,name):
        try:
            search = SearchVideos(name, offset = 1, mode = "json", max_results = 20)
            return json.loads(search.result())
        except:
            return "Fail"



class Eleven(Resource):

    def get(self,name):
        try:
            search = sp(name, offset = 1, mode = "json", max_results = 40)
            return json.loads(search.result())
        except:
            return "Fail"


class Twelve(Resource):

    def get(self):
        try:
            search = Home()
            return json.loads(search.result())
        except:
            return "Fail"

from urllib.parse import unquote
class Seventeen(Resource):
    @cross_origin(origin='*')
    def get(self,visitdata,token):
        
            #print(unquote(name))
        search = hm.result(visitdata,token)
        return json.loads(search)
        #except:
        #    return "Fail"


class Eighteen(Resource):
    @cross_origin(origin='*')
    def post(self,name):
        try:
            data = request.get_json('data')
            return name
        except:
            return "Fail"

class Thirteen(Resource):
    @cross_origin(origin='*')
    def get(self,name):
        try:
            search = Sub(name)
            return json.loads(search.result())
        except:
            return "Fail"

class Seventy(Resource):
    @cross_origin(origin='*')
    def get(self,name):
        try:
            search = PlaylistYt(name)
            return json.dumps(search.get_result())
        except:
            return "Fail"
            
class Mid(Resource):

    def post(self):      
        data = request.get_json('data')
        link=data['link']
        #print(link)
        v = pafy.new(link)
        for s in v.allstreams:
            if ('x360' in s.resolution):
                #print(s)
                link_data['link_360']=s.url
            elif ('x480' in s.resolution):
                link_data['link_480']=s.url
            elif ('x720' in s.resolution):
                link_data['link_720']=s.url
            elif ('x1080' in s.resolution):
                link_data['link_1080']=s.url
            elif ('m4a' in s.extension):
                link_data['link_m4a']=s.url
            else:
                pass

        #data = request.json('data')
        #data = request.args.get('data')     # status code 
        #print(data)

        return jsonify(link_data)    #json.loads({'data':"HELLAA"}) , 201 #jsonify({'data': 'HELLL'}), 201
 


class Two(Resource):

    def get(self):
        try:
            video = pafy.new(url)
            best = video.getbest()
            playurl = best.url
            return {'id': str(playurl)}
        except:
            return "Fail"
class Three(Resource):

    def get(self):
        try:
            video = pafy.new(url)
            test=video.streams
            playurl=test[1].url
            return {'id': str(playurl)}
        except:
            return "Fail"

class Four(Resource):
    
    @cross_origin(origin='*')
    def get(self,name):
        try:
            #data = name
            #link=data['link']
            #print(link)

            link="https://www.youtube.com/watch?v="+name
            v = pafy.new(link)
            for s in v.allstreams:
                if ('x360' in s.resolution):
                        #print(s)
                    link_data['link_360']=s.url
                elif ('x480' in s.resolution):
                    link_data['link_480']=s.url
                elif ('x720' in s.resolution):
                    link_data['link_720']=s.url
                elif ('x1080' in s.resolution):
                    link_data['link_1080']=s.url
                elif ('m4a' in s.extension):
                    link_data['link_m4a']=s.url
                else:
                    pass

                #data = request.json('data')
                #data = request.args.get('data')     # status code 
                #print(data)

            return jsonify(link_data)    
        #return "HELL"
        except:
            return "FAIL"


@app.route('/api5/<string:name>', methods=['GET'])
@cross_origin(origin='*')
def met(name):
    
    link="https://www.youtube.com/playlist?list="+name
    playlist = pafy.get_playlist(link) 
    items = playlist["items"] 
    i=0
    result=[]
    for index in items:
        result_index = {
        "index": i,
        "meta":index['playlist_meta'], 
        }
        i=i+1
        result+=[result_index]

    return jsonify(result)
        #return "HELL"

@app.route('/api77/<string:name>', methods=['GET'])
@cross_origin(origin='*')
def meet(name):
    search = Sub(name)
    return json.loads(search.result())


api.add_resource(One, "/api/<string:name>")
api.add_resource(Eleven, "/apiplay/<string:name>")
api.add_resource(Twelve, "/apihome/")
api.add_resource(Seventeen, "/apihomestar/<string:visitdata>/<string:token>")
api.add_resource(Eighteen, "/apitest/<string:name>")
api.add_resource(Thirteen, "/apisub/<string:name>")
api.add_resource(Seventy,"/playlistsub/<string:name>")
api.add_resource(Mid, "/api2/")
api.add_resource(Four,'/api4/<string:name>')
api.add_resource(Two, "/test/")
api.add_resource(Three, "/test/360/")
if __name__ == "__main__":
    app.run(debug=True)