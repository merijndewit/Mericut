import os

class FileToMeriCode:
    @staticmethod
    def GetMeriCodeFromTxt():
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        with open(os.path.dirname(dname) + '/Test/MeriCodeTestFile.txt') as f:
            return f.readlines()
