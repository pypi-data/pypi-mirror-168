
from io import RawIOBase

class MyFileStream(RawIOBase):

    def __init__(self, content:bytes):
        self.content = content


    def read(self, n:int=-1):  # real signature unknown
        return self.content[:n]

    def readall(self, *args, **kwargs):  # real signature unknown
        """ Read until EOF, using multiple read() call. """
        return self.content




