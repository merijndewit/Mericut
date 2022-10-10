import os

class FileToMeriCode:
    @staticmethod
    def GetMeriCodeFromTxt():
        with open('Test/MeriCodeTestFile.txt') as f:
            return f.readlines()
