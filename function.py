import urllib.request
import zipfile
import os
import shutil
import time
import datetime
import xml.dom.minidom
import requests
from PIL import Image

urlXml = 'http://game.ds.qq.com/Com_TableCom_Android/TableCom.zip'#xml文件下载链接
url = 'http://game.ds.qq.com/Com_SongRes/song'#资源文件下载目录
timeFile = '/time.txt'#更新歌单时间文件
xmlFile = 'mrock_song_client_android.xml'#xml文件

fileType = ['.jpg','.mp3','_4k_ez.imd', '_4k_nm.imd', '_4k_hd.imd', '_5k_ez.imd', \
'_5k_nm.imd', '_5k_hd.imd', '_6k_ez.imd', '_6k_nm.imd', '_6k_hd.imd', '_ipad.jpg',\
'_title_ipad.jpg',  '_Papa_Easy.mde', '_Papa_Normal.mde', '_Papa_Hard.mde']#资源文件补全

runPath = os.path.abspath('.')+'/'#获取当前运行目录

#下载文件存到目录
def  download(url, downPath):
    fileUrl = 0
    for i in range(len(url)):
        if url[i] == '/':
            fileUrl = i
    fileName = url[fileUrl:]
    try :
        if (not(requests.get(url).status_code == '404') and not(os.path.exists(downPath+fileName))): #链接不存在或者文件存在则不下载
            urllib.request.urlretrieve(url, downPath+fileName)
    except urllib.error.HTTPError:
        print('文件不存在')
        




#解压目标文件到1/文件夹，并将目标文件移动到运行目录
def getFile(path, files):
    zipFile = zipfile.ZipFile(path, mode='r') #zip解压
    for file in zipFile.namelist():
        zipFile.extract(file,'1/')
    if os.path.exists(runPath+xmlFile):
        os.remove(runPath+xmlFile)
    shutil.move('1/'+files, runPath)
    floder = os.listdir('1/')				#删除目录1下文件
    for file in floder:
        filePath = os.path.join('1/', file)
        if os.path.isfile(filePath):
            os.remove(filePath)
        elif os.path.isdir(filePath):
            shutil.rmtree(filePath)
    shutil.rmtree('1')						#删除目录1

#得到两个xml和一个更新时间的文件
def getXml():
    timefile = runPath+timeFile
    currentTime = time.mktime(datetime.datetime.now().timetuple()) #获取当前系统时间的UNIX时间戳
    if not(os.path.exists(timefile)):								#判断时间文件否存在，创建文件
        file = open(timefile, 'w+')
        try:
            file.write('0')
        finally:
            file.close()
    file = open(timefile)										#打开文件读取时间
    try:
        fileTime = file.read()
    finally:
        file.close()
        #如果超过1天未更新或者缺少文件则重新下载
    if (currentTime - float(fileTime) > 86400 or not(os.path.exists(xmlFile))):
        outFile = open(timefile, 'w+')
        try:
            outFile.write(str(currentTime))
        finally:
            outFile.close()
        download(urlXml, runPath)
        getFile('TableCom.zip', xmlFile)
        os.remove(runPath+'TableCom.zip')						#删除压缩包

#获得歌曲name和path数组
def getSongList():                                               
    #if not(os.path.exists(runPath+xmlFile)) or not(os.path.exists(runPath+timeFile)):                     #判断xml文件存在，不存在则调用getXml
        getXml()
    #    getSongList()
   # else:
        songList = []                                             #歌曲数组
        songInfo = []                                             #当前歌曲信息临时数组
        root = xml.dom.minidom.parse(runPath+xmlFile)            #xml文件操作
        data = root.documentElement
        songListNode = data.getElementsByTagName('SongConfig_Client')
        for song in songListNode:
            songName = song.getElementsByTagName('m_szSongName')[0]
            songInfo.append(songName.childNodes[0].data)
            songPath = song.getElementsByTagName('m_szPath')[0]
            songInfo.append(songPath.childNodes[0].data)
            songList.append(songInfo)
            songInfo = []
        return songList
 
 #下载歌曲文件并保存在歌曲path目录下       
def downSong(path):
    songUrl = url + '/' + path + '/' + path
    if not(os.path.exists(runPath+path)):                     #目录不存在则创建
        os.mkdir(runPath+path)
    for files in fileType:
        download(songUrl+files, runPath+path)
        #print(songUrl+files)
 
 #压缩歌曲文件夹       
def getZip(path, fileName, isDelOriginal):
    if not(os.path.exists(runPath+fileName)):
        compression = zipfile.ZIP_DEFLATED                         #压缩文件操作
        start = path.rfind(os.sep) + 1
        z = zipfile.ZipFile(fileName, mode='w', compression = compression)
        try:
            for dirpath, dirs, files in os.walk(path):
                for file in files:
                    if file == fileName:
                        continue
                    zPath = os.path.join(dirpath, file)
                    z.write(zPath, zPath[start:])
            z.close()
        except:
            if z:
                z.close()
    if isDelOriginal:                                      #如果选择删除原文件则删除
        floder = os.listdir(path)
        for file in floder:
             filePath = os.path.join(path, file)
             if os.path.isfile(filePath):
                 os.remove(filePath)
             elif os.path.isdir(filePath):
                shutil.rmtree(filePath)
        shutil.rmtree(path)				

#将目录下所有jpg转png并删除原文件
def getPng(path):
    floder = os.listdir(path)
    for file in floder:
        (fileName, file_type) = os.path.splitext(file)
        if file_type == '.jpg':
            im = Image.open(path+file)
            im.save(path+fileName+'.png', 'png')
            os.remove(path+file)

#if __name__ == '__main__':
    #getXml()
   # getSongList()
    #downSong('beiduofenbingdu')
    #getZip('beiduofenbingdu/', 'beiduofenbingdu.zip', True)
    #getPng('beiduofenbingdu/')
    

