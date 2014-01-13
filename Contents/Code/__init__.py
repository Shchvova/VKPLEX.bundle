import urllib
import json

ART  = 'art-default.jpg'
ICON = 'icon-default.png'


def Start():
    MediaContainer.title1 = "VK"
    MediaContainer.viewGroup = "List"
    
    #setting some globals for fun.
    HTTP.CacheTime = CACHE_1HOUR
    MediaContainer.title1 = "VK"
    MediaContainer.viewGroup = "List"
    MediaContainer.art = R(ART)
    DirectoryItem.thumb = R(ICON)
    VideoItem.thumb = R(ICON)

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
  


@handler('/video/vkplex', L('VideoTitle'))
def VideoMainMenu():

    # Container acting sort of like a folder on
    # a file system containing other things like
    # "sub-folders", videos, music, etc
    # see:
    #  http://dev.plexapp.com/docs/Objects.html#MediaContainer
    dir = MediaContainer(viewGroup="InfoList")


    # see:
    #  http://dev.plexapp.com/docs/Objects.html#DirectoryItem
    #  http://dev.plexapp.com/docs/Objects.html#function-objects
    dir.Append(
        Function(
            DirectoryItem(
                CallbackExample,
                "directory item title",
                subtitle="subtitle",
                summary="clicking on me will call CallbackExample",
                thumb=R(ICON),
                art=R(ART)
            )
        )
    )
  
    # Part of the "search" example 
    # see also:
    #   http://dev.plexapp.com/docs/Objects.html#InputDirectoryItem
    dir.Append(
        Function(
            InputDirectoryItem(
                SearchResults,
                "Search title",
                "Search subtitle",
                summary="This lets you search stuff",
                thumb=R(ICON),
                art=R(ART)
            )
        )
    )

  
    # Part of the "preferences" example 
    # see also:
    #  http://dev.plexapp.com/docs/Objects.html#PrefsItem
    #  http://dev.plexapp.com/docs/Functions.html#CreatePrefs
    #  http://dev.plexapp.com/docs/Functions.html#ValidatePrefs 
    dir.Append(
        PrefsItem(
            title="Your preferences",
            subtile="So you can set preferences",
            summary="lets you set preferences",
            thumb=R(ICON)
        )
    )

    # ... and then return the container
    return dir



@handler('/music/vkplex',  L('MusicTitle'))
def MusicMainMenu():

    # Container acting sort of like a folder on
    # a file system containing other things like
    # "sub-folders", videos, music, etc
    # see:
    #  http://dev.plexapp.com/docs/Objects.html#MediaContainer
    dir = MediaContainer(viewGroup="InfoList")


    # see:
    #  http://dev.plexapp.com/docs/Objects.html#DirectoryItem
    #  http://dev.plexapp.com/docs/Objects.html#function-objects
    dir.Append(
        Function(
            DirectoryItem(
                CallbackExample,
                "directory item title",
                subtitle="subtitle",
                summary="clicking on me will call CallbackExample",
                thumb=R(ICON),
                art=R(ART)
            )
        )
    )
  
    # Part of the "search" example 
    # see also:
    #   http://dev.plexapp.com/docs/Objects.html#InputDirectoryItem
    dir.Append(
        Function(
            InputDirectoryItem(
                SearchResults,
                "Search title",
                "Search subtitle",
                summary="This lets you search stuff",
                thumb=R(ICON),
                art=R(ART)
            )
        )
    )

  
    # Part of the "preferences" example 
    # see also:
    #  http://dev.plexapp.com/docs/Objects.html#PrefsItem
    #  http://dev.plexapp.com/docs/Functions.html#CreatePrefs
    #  http://dev.plexapp.com/docs/Functions.html#ValidatePrefs 
    dir.Append(
        PrefsItem(
            title="Your preferences",
            subtile="So you can set preferences",
            summary="lets you set preferences",
            thumb=R(ICON)
        )
    )

    # ... and then return the container
    return dir


#
# Example main menu referenced in the Start() method
# for the 'Photos' prefix handler
#
@handler('/photos/vkplex',  L('PhotosTitle'))
def PhotosMainMenu():

    # Container acting sort of like a folder on
    # a file system containing other things like
    # "sub-folders", videos, music, etc
    # see:
    #  http://dev.plexapp.com/docs/Objects.html#MediaContainer
    dir = MediaContainer(viewGroup="InfoList")


    # see:
    #  http://dev.plexapp.com/docs/Objects.html#DirectoryItem
    #  http://dev.plexapp.com/docs/Objects.html#function-objects
    dir.Append(
        Function(
            DirectoryItem(
                CallbackExample,
                "directory item title",
                subtitle="subtitle",
                summary="clicking on me will call CallbackExample",
                thumb=R(ICON),
                art=R(ART)
            )
        )
    )
  
    # Part of the "preferences" example 
    # see also:
    #  http://dev.plexapp.com/docs/Objects.html#PrefsItem
    #  http://dev.plexapp.com/docs/Functions.html#CreatePrefs
    #  http://dev.plexapp.com/docs/Functions.html#ValidatePrefs 
    dir.Append(
        PrefsItem(
            title="Your preferences",
            subtile="So you can set preferences",
            summary="lets you set preferences",
            thumb=R(ICON)
        )
    )

    # ... and then return the container
    return dir

def CallbackExample(sender):

    ## you might want to try making me return a MediaContainer
    ## containing a list of DirectoryItems to see what happens =)

    return MessageContainer(
        "Not implemented",
        "In real life, you'll make more than one callback,\nand you'll do something useful.\nsender.itemTitle=%s" % sender.itemTitle
    )

# Part of the "search" example 
# query will contain the string that the user entered
# see also:
#   http://dev.plexapp.com/docs/Objects.html#InputDirectoryItem
def SearchResults(sender,query=None):
    return MessageContainer(
        "Not implemented",
        "In real life, you would probably perform some search using python\nand then build a MediaContainer with items\nfor the results"
    )
    
  
