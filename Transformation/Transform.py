import os
from Applogger.logger import Applogger
from os import listdir
import pandas



class Transfrom:
    """this class will fill missing valies with null
    """

    def __init__(self):
        self.good_path='training_data/Good_data'
        self.logger=Applogger()


    def fill(self):

        file=open('Traininglog/column1.txt','a+')
        try:
            onlyfile=[f for f in listdir(self.good_path)]
            for f in onlyfile:
                csv=pandas.read_csv(self.good_path+'/'+f)
                #csv['Wafer'] = pandas.to_numeric(csv['Wafer'], errors='coerce').fillna(csv['Wafer']).astype(str).str[6:]

                csv.fillna('NULL',inplace=True)

                csv['Wafer']=csv['Wafer'].str[6:]
                csv.to_csv(self.good_path+"/"+f,header=True,)
                csv.to_csv(self.good_path+"/"+f,index=False)
                self.logger.logger("filled with null value and renamed first column with integer",file)
                file.close()



        except Exception as e:
             file=open("Traininglog/column1.txt","a+")
             self.logger.logger(":::%s:::"%e,file)
             file.close()





#c=Transfrom()
#c.fill()


