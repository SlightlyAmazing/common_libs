try:
    from common_libs import base_classes
except:
    import base_classes

from datetime import datetime, date, time, timezone
from pathlib import Path

default_uri = "logs"
default_file_starter = "player"
default_ext = "log"

class logManager(base_classes.baseManager):

    def onInit(self, uri = None, file_starter = None, ext = None):        
        self.file_name = (uri if uri != None else default_uri)+"/"+(file_starter if file_starter != None else default_file_starter)+"."+(ext if ext != None else default_ext)
        self.prev_file_name = (uri if uri != None else default_uri)+"/"+(file_starter if file_starter != None else default_file_starter)+"_prev."+(ext if ext != None else default_ext)
        Path("/"+uri if uri!=None else default_uri).mkdir(parents=True, exist_ok=True)
        try:
            file = open(self.file_name,"r")
            file_content = file.read()
            file.close()
        except:
            file_content = ""
        file = open(self.file_name,"w")
        file.write("")
        file.close()
        file_prev = open(self.prev_file_name,"w")
        file_prev.write(file_content)
        file_prev.close()

    def addDate(self, message):
        time=datetime.now()
        return "["+str(time.year-2000)+"-"+str(time.month)+"-"+str(time.day)+" "+str(time.hour)+":"+str(time.minute)+":"+str(time.second)+"] "+ message
    
    def log(self,message):
        file = open(self.file_name,"a")
        file.write(message+"\n")
        file.close()
    
    def logInfo(self,message):
        message = self.addDate("[Info] "+message)
        self.log(message)
    
    def logWarning(self,message):
        message = self.addDate("[Warning] "+message)
        print(message)
        self.log(message)

    def logError(self,message):
        message = "\n\n"+self.addDate("[ERROR] "+message+"\n\n")
        print(message)
        self.log(message)

