import urllib
import json

ART  = 'art-default.jpg'
ICON = 'icon-default.png'


def Start():
    MediaContainer.title1 = "VK"
    MediaContainer.viewGroup = "List"
    
    HTTP.CacheTime = CACHE_1HOUR
    MediaContainer.title1 = "VK"
    MediaContainer.art = R(ART)
    DirectoryItem.thumb = R(ICON)
    VideoItem.thumb = R(ICON)



@handler('/video/vkplex', L('VideoTitle'))
def VideoMainMenu():
    oc = ObjectContainer()
    oc.add(DirectoryObject(key=Callback(MyVideos, offset=0), title="My Videos"))
    return oc



@route('/video/vkplex/my/{offset}')
def MyVideos(offset):
    offset = int(offset or 0)
    res = api('video.get', count=20, extnded=0, offset=offset)
    count = int(res['count'])
    #this page title: title=
    oc = ObjectContainer(title1="My Videos, page {0} of {1}".format(1+offset/20, 1+count/20))

    if offset > 0:
        oc.add(DirectoryObject(key=Callback(MyVideos, offset=offset-20), title="Previous Page"))

    for v in res["items"]:
        url = ""
        for k in v['files']:
            url = v['files'][k]
            break
        #mo = MovieObject(title=v['title'], rating_key=v['id'], url=url )
        #mo.add( MediaObject(parts=[PartObject(key = url)]) )
        #oc.add(mo)
        if 'youtube' not in url:
            oc.add(VideoClipObject(url=url, title=v['title']))

    if count > offset+20:
        oc.add(DirectoryObject(key=Callback(MyVideos, offset=offset+20), title="Next Page"))

    Log.Debug("Here is things: " + str(count))

    return oc

#@indirect
#@route('/video/vkplex/play/',"url")
#def PlayURL(url):
#    return ObjectContainer(objects=[MovieObject(objects=[MediaObject(parts=[PartObject(key = url)])])])
#



@handler('/music/vkplex',  L('MusicTitle'))
def MusicMainMenu():
    oc = ObjectContainer()
    return oc

#
# Example main menu referenced in the Start() method
# for the 'Photos' prefix handler
#
@handler('/photos/vkplex',  L('PhotosTitle'))
def PhotosMainMenu():
    oc = ObjectContainer()
    return oc


#   http://dev.plexapp.com/docs/Objects.html#InputDirectoryItem
def SearchResults(sender,query=None):
    return MessageContainer(
        "Not implemented",
        "In real life, you would probably perform some search using python\nand then build a MediaContainer with items\nfor the results"
    )
    

def ValidatePrefs():
    email = Prefs['username']
    password = Prefs['password']
    client_id, secret, scope ="2054573", "KUPNPTTQGApLFVOVgqdx", 'friends,groups,photos,audio,video,offline'
    if not email and not password:
        Dict['token'] = ""
        Dict.Save()
        Log.Info("Logged out")
        return MessageContainer("Success", "Logged out!")

    if not email or not password:
        return MessageContainer("Success", "Just cleaning info!")

    out = {}
    try:
        url = urllib.urlopen("https://oauth.vk.com/token?" + urllib.urlencode({
                "grant_type": "password",
                "client_id": client_id,
                "client_secret": secret,
                "username": email,
                "password": password,
                "scope": scope
            }))
        out = json.load(url)
        if "access_token" not in out:
            return MessageContainer("Error", "You need to provide both a user and password")
    except:
        Log.Info("Unable to authorize due to exception. Invalid Login/Password?")    
        return MessageContainer("Error", "You need to provide both a user and password")
    Dict['token'] = out["access_token"]
    Dict.Save()
    Log.Info("Logged int with token: " + Dict['token'])
    return MessageContainer("Success", "User and password provided ok")
  
def api(api, **params):
    f = {'access_token': Dict['token'], 'v':'5.5'}
    f.update(params)
    #Log.Debug("https://api.vk.com/method/" + api + "?" + urllib.urlencode(f))
    url = urllib.urlopen("https://api.vk.com/method/" + api + "?" + urllib.urlencode(f))
    return json.load(url)['response']
