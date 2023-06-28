from Applogger.logger import Applogger
import pandas


class data:
    def __init__(self):
        self.training_object='Trainingfilefromdb/Inputfile.csv'
        self.log=Applogger()
        self.file=open('Traininglog/Inputdata.txt','a+')

    def loader(self):
        try:
            self.log.logger("Entred to data geter file method",self.file)
            self.data=pandas.read_csv(self.training_object)
            self.file.close()
            return self.data

        except Exception as e:
              self.log.logger("error occured::%s"%e,self.file)
              self.file.close()













