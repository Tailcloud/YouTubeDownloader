import os
import sys
import urllib.request
import re
from pytube import YouTube

def download(url,path):
    if '&' in url:
        inx = url.index('&')
    url = url[:inx]
    try:
        yt = YouTube(url)
    except Exception as e:
        with open(path+"/errlog.txt", "a") as logfile:
            logfile.write("Error:"+ str(e)+url+"'." + '\n')
        return
    try:
        video = yt.get('mp4', '720p')
    except Exception:
        video = sorted(yt.filter("mp4"), key=lambda video: int(video.resolution[:-1]), reverse=True)[0]
    print("Downloading", yt.filename+"...")
    try:
        video.download(path)
        print("Downlaod ", yt.filename, " Finish!")
    except OSError:
        print(yt.filename, "OSError")
def getListID(url):
    if 'list=' in url:
        idx = url.index('=') + 1 #find index of list=?
        pl_id = url[idx:]#get id
        if '&' in url:
            amp = url.index('&')
            pl_id = url[eq_idx:amp]
        return pl_id
    else:
        print(url, "sth err in get list id")
        exit(1)

def rematch(html,url,path):
    #/watch?v=5sQeQC4hT10&index=19&list=PLcciozUgByFwmHp7Kt4Y58A9xLSvcC6iG"
    listId = getListID(url)
    pattern = re.compile(r'watch\?v=\S+?list='+listId)
    result = re.findall(pattern,str(html))
    for i,dUrl in enumerate(result):#enumerate(list,start)
        downloadUrl = 'https://www.youtube.com/'+dUrl
        download(downloadUrl,path)

def listcontains(url,path):
    with urllib.request.urlopen(url) as response:
        html = response.read()
        rematch(html,url,path)

if __name__ == '__main__':
    # python3 downloadList.py XXXX dst
    if len(sys.argv)>3:
        print('Too many arguments')
        exit(1)
    else:
        if len(sys.argv)==3:
            dst = sys.argv[2]
            url = sys.argv[1]
        else:
            dst = os.getcwd()+'/Download'
            try:
                os.makedirs(dst, exist_ok=True)
            except OSError as e:
                print(e.reason)
                exit(1)
        path = dst
        listcontains(url,path)
