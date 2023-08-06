# -*- coding: utf-8 -*-
# __author__ : Ricky
# __createTime__ : 2021/1/7 15:17
# __fileName__ : GoldenCoordinateV2 Settings.py
# __devIDE__ : PyCharm


from PySide2 import QtCore as qtc


class Settings:


    def __init__(self, configFile):
        _Settings = qtc.QSettings(configFile, qtc.QSettings.IniFormat)
        _Settings.setIniCodec(qtc.QTextCodec.codecForName('utf-8'.encode()))
        self._Settings = _Settings
        self._currentSec = ""

    def keys(self, section=""):
        self._Settings.beginGroup(section or self._currentSec)
        keys = self._Settings.childKeys()
        self._Settings.endGroup()
        return keys

    def Sections(self):
        return self._Settings.childGroups()

    def setSection(self, section):
        self._currentSec = section

    def allKeys(self):
        return self._Settings.allKeys()

    def value(self,key, defaultValue=None, typ=str, section=""):
        self._Settings.beginGroup(section or self._currentSec)
        value = self._Settings.value(key, defaultValue=defaultValue, type=typ)
        self._Settings.endGroup()
        return value

    def setValue(self,key, value, section=""):
        self._Settings.beginGroup(section or self._currentSec)
        self._Settings.setValue(key, value)
        self._Settings.sync()
        self._Settings.endGroup()

    def setValues(self, dic:dict=None, section=""):
        self._Settings.beginGroup(section or self._currentSec)
        for k in (dic or {}):
            self._Settings.setValue(k, dic[k])
        self._Settings.sync()
        self._Settings.endGroup()

    def items(self, ks=None, isHidden=False, section=""):
        _ks = set(self.keys(section=section))
        _fields = ks and set(ks) or set()
        fields = _fields.intersection(_ks) or _ks
        if isHidden:
            fields = _ks.difference(_fields)
        return {
            field: self.value(field, section=section)
            for field in fields
        }









