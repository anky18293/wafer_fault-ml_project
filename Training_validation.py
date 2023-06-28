from Applogger.logger import Applogger
from Dbopeation.operation import DB
from Data_validation.raw_data import rawdata
from Transformation.Transform import Transfrom



class train_validation:
     """
     this class will validat my data thorugh file name validation , datetime,column ,fill mission value ,
     transformation  etc
     """

     def __init__(self,path):
        self.rawdata=rawdata(path)
        self.db=DB()
        self.Transform=Transfrom()
        self.fileobject=open("Traininglog/Validationfile.txt","a+")
        self.log=Applogger()

     def train_validate(self):
         try:
           self.log.logger("Validation started ",self.fileobject)
           length_date , length_time, no_column,col_name=self.rawdata.load()
           regex=self.rawdata.manualregex()
           self.rawdata.validatefilename(regex,length_date,length_time)
           self.rawdata.validatecolumn(no_column)
           self.rawdata.misscolumn()
           self.log.logger("Data validation complete",self.fileobject)
           self.log.logger("Starting Data transformation",self.fileobject)
           self.Transform.fill()
           self.log.logger("transformation complete",self.fileobject)
           self.db.createtable('training',col_name)
           self.log.logger("Table created successfully",self.fileobject)
           self.log.logger("Insertion strated",self.fileobject)
           self.db.insertintodb('TraininG')
           self.log.logger("insertion complted",self.fileobject)
           self.log.logger("deleting good data folder",self.fileobject)
           self.rawdata.good_folder_delete()
           self.log.logger("moving bad file to Archive",self.fileobject)
           self.rawdata.movefileArchieveFolder()
           self.db.transportintocsv('training')
           self.fileobject.close()

         except Exception as e:
             self.fileobject=open("Traininglog/Validationfile.txt","a+")
             self.log.logger(":%s"%e,self.fileobject)
             self.fileobject.close()







#c=train_validation()
#c.train_validate()






