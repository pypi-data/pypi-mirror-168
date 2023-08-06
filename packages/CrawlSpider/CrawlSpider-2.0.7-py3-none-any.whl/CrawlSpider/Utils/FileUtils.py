# -*- coding: utf-8 -*-
# __author__ : Ricky
# __createTime__ : 2022/7/7 15:59
# __fileName__ : XueshuSpider FileUtils.py
# __devIDE__ : PyCharm
from PySide2 import QtCore as qtc


def getDir(fileDirPath, customDir=None):
    fileDir = customDir if customDir else qtc.QDir.home()
    flag = fileDir.cd(fileDirPath)
    if not flag:
        fileDir.mkpath(fileDirPath)
        fileDir.cd(fileDirPath)
    return fileDir
def copyFile(fileName:str, fileDirPath, customDir=None):
    fileDir = getDir(fileDirPath, customDir=customDir)
    newName = fileDir.filePath(fileName.split('/')[-1])
    qtc.QFile.copy(fileName, newName)
    return newName



def mkdir(fileDirPath, customDir=None):
    fileDir = customDir if customDir else qtc.QDir.home()
    flag = fileDir.cd(fileDirPath)
    if not flag:
        while not fileDir.mkpath(fileDirPath):
            qtc.QThread.msleep(200)
            print(f"创建目录: {fileDirPath}")
        fileDir.cd(fileDirPath)
    return fileDir.path()

def delDir(fileDirPath, customDir=None):
    fileDir = customDir if customDir else qtc.QDir.home()
    if fileDir.cd(fileDirPath):
        f = fileDir.removeRecursively()
        print(f"删除目录: {fileDirPath}", f)


def deleteBak(dirPath):
    fileDir = qtc.QDir(dirPath)
    entryInfoList = fileDir.entryInfoList(filters=qtc.QDir.Filter.Files)
    for entryInfo in entryInfoList:
        entryInfo: qtc.QFileInfo

        if entryInfo.suffix() == 'bak':
            fileName = entryInfo.fileName()
            fileDir.remove(fileName)
