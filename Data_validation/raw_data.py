from Applogger.logger import Applogger
import json
import os
from os import listdir
import shutil
import re
import pandas as pd
class rawdata:
    """
    This class will help me to validate my file  and get to good and  bad directory
    """



    def __init__(self,path):
        self.path=path
        self.batch_file='schema_training.json'
        self.logger=Applogger()

    def load(self):
        """
           load
                 """


        with open(self.batch_file ,'r') as f:
                 dic=json.load(f)
                 f.close()
        pattern=dic['SampleFileName']
        LengthOfDateStampInFile=dic['LengthOfDateStampInFile']
        LengthOfTimeStampInFile=dic['LengthOfTimeStampInFile']
        NumberofColumns=dic['NumberofColumns']
        col_name=dic['ColName']
        file=open('Traininglog/valuesfromcol.txt','a+')
        message="length of Date %s::"%LengthOfDateStampInFile+"\t"+"length of time  stamp %s::"%LengthOfTimeStampInFile+"\t"+"number of col:%s"%NumberofColumns
        self.logger.logger(message,file)
        f.close()


        return LengthOfDateStampInFile,LengthOfTimeStampInFile,NumberofColumns,col_name





    def makedirectroyGood_and_Bad(self):

      try:
         path=os.path.join("training_data/","Good_data/")
         if not os.path.isdir(path):
             os.makedirs(path)

         path=os.path.join("training_data/","Bad_data/")
         if not os.path.isdir(path):
              os.makedirs(path)

      except Exception as e:
          file=open('Traininglog\Generalog.txt','w')
          self.logger.logger("Haiving an error while working giving os error %s"%e,file)



    def good_folder_delete(self):
        try:
            path = 'training_data/'
            if os.path.isdir(path + 'Good_data/'):
                shutil.rmtree(path + 'Good_data/')
                file = open('Traininglog\Generalog.txt','a+')
                self.logger.logger( "goodaw directory deleted before starting validation!!!",file)
                file.close()
        except OSError as s:
            file = open('Traininglog\Generalog.txt','a+')
            self.logger.logger( "Error while Deleting Directory : %s" % s,file)
            file.close()
            raise OSError

    def bad_Data_delete(self):
       try:
           path='training_data/'
           if os.path.isdir(path+'Bad_data'):
               shutil.rmtree(path+"Bad_data")
           file=open('Traininglog\Generalog.txt','a+')
           self.logger.logger("deleted",file)
           file.close()

       except Exception as e:
         file = open('Traininglog\Generalog.txt', 'a+')
         self.logger.logger("Error happend::%s" %e, file)
         file.close()




    def movefileArchieveFolder(self):


      try:
            source='training_data/Bad_data/'
            if os.path.isdir(source):
               path='BadArchive'
               if not os.path.isdir(path):
                   os.makedirs(path)
               dest='BadArchieve/bad_Data'
               if not os.path.isdir(dest):
                   os.makedirs(dest)
               files=os.listdir(source)
               for f in files:
                   if f not in os.listdir(dest):
                      shutil.move(source +f ,dest)
               f=open("Traininglog/Generallog",'w')
               self.logger.logger("Files moved to archieve",f)
               path='training_data'
               if os.path.isdir(path +'Bad_data/'):
                  shutil.rmtree(path+'Bad_data/')
               self.logger.logger("Bad data deleted ",f)
               f.close()

      except Exception as e:
          f=open("Traininglog/Generalog.txt","w")
          self.logger.logger("  %s::"%e,f)
          f.close()




    def manualregex(self):
        regex= "['wafer']+['\_'']+[\d_]+[\d]+\.csv"
        return regex



    def validatefilename(self, regex, LengthOfDateStampInFile, LengthOfTimeStampInFile):
        """
        this will validate my file name ,date column, and timestamp
        """

        self.good_folder_delete()
        self.bad_Data_delete()
        self.makedirectroyGood_and_Bad()
        files=[f for f in listdir(self.path)]
        try:
            f = open("Traininglog/namevalidationlog.txt", 'a+')
            for l in files:
                if (re.match(regex,l)):
                    splitat=re.split('.csv',l)
                    splitat=(re.split('_',splitat[0]))
                    if len(splitat[1])==LengthOfDateStampInFile:
                        if len(splitat[2])==LengthOfTimeStampInFile:
                            shutil.copy("TrainingBatch/"+ l,
                                        "training_data\Good_data")
                            self.logger.logger("file moved to good directory",f)
                        else:
                           self.logger.logger("Invalid file name ::",f)
                           shutil.copy(r"TrainingBatch/"+ l,"training_data/bad_data")
                    else:
                        self.logger.logger("Invalid file name",f)
                        shutil.copy("TrainingBatch/"+ l,"training_data/bad_data")
                else:
                    self.logger.logger("invalid file name",f)
                    shutil.copy("TrainingBatch/"+ l,"training_data/bad_data")

        except Exception as e:
            f=open("Traininglog/namevalidationlog.txt",'a+')
            self.logger.logger("error happended :: %s"%e,f)
            f.close()




    def validatecolumn(self,NumberofColumns):

      try:
          f=open('Traininglog\Columnval.txt','a+')
          self.logger.logger("column validation started",f)
          for file in listdir('training_data/Good_data/'):
              csv=pd.read_csv('training_data/Good_data/'+file)
              if csv.shape[1]==NumberofColumns:
                  pass
              else:
                  shutil.move('training_data\Good_data/'+file,'training_data/bad_data/')
                  self.logger.logger("invalid colum length ",f)
              self.logger.logger("file is good",f)


      except Exception as e:
          f=open('Traininglog/Generalog.txt','a+')
          self.logger.logger("error happedn %s:: "%e ,f)
          f.close()

      f.close()




    def misscolumn(self):
        """we are seeing if we have null coulmn or not if we have we rejecting that column"""
        try:
             file=open("traininglog/validatecolumn.txt",'a+')
             self.logger.logger("validating column length",file)
             for f in listdir('training_data/Good_data/'):
                 csv=pd.read_csv("training_data\Good_data/"+ f)
                 count=0
                 for columns in csv:
                    if (len(csv[columns])-csv[columns].count())==len(csv):
                        count+=1
                        shutil.move('training_data\Good_data/'+f,'training_data/bad_data')
                        self.logger.logger("filemoved due to bad column length",file)
                        break
                    if count==0:
                        csv.rename(columns={"Unnamed: 0": "Wafer"}, inplace=True)
                        #csv.to_csv(r"C:/Users/Mohd Kaif/OneDrive/Desktop/Zaid_project/training_data/Good_data/ " + f, index=None, header=True)
             file.close()

        except Exception as e:
            file=open("Traininglog\column.txt","a+")
            self.logger.logger("error happend %s:: "%e,  file)
            file.close()







        
        






        





                









