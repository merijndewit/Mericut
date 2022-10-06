import os

class FileToMicroGcode:
    @staticmethod
    def GetMicroGcodeFromTxt():
        with open('microGcodeFiles/microG-code.txt') as f:
            return f.readlines()
