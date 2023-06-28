from datetime import datetime
class Applogger:
    def __init__(self):
        pass

    def logger(self,log,fileobject):
        self.now=datetime.now()
        self.date=self.now.date()
        self.currenttime=self.now.strftime("%H:%M:%S")
        fileobject.write(
            str(self.date)+"/"+str(self.currenttime)+"\t\t"+log+"\n"
        )