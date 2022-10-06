import os

class FileToMeriCode:
    @staticmethod
    def GetMeriCodeFromTxt():
        with open('MeriCodeFiles/MeriCodeTestFile.txt') as f:
            return f.readlines()
