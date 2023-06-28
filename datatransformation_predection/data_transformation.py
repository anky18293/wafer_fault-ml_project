
from os import listdir
import pandas as pd
from Applogger.logger import Applogger


class dataTransformPredict:

     """
                  This class shall be used for transforming the Good Raw Training Data before loading it in Database!!.

                  Written By: iNeuron Intelligence
                  Version: 1.0
                  Revisions: None

                  """

     def __init__(self):
          self.goodDataPath = "Prediction_raw_Files_Validated/Good_Raw"
          self.logger = Applogger()


     def replaceMissingWithNull(self):

          """
                                  Method Name: replaceMissingWithNull
                                  Description: This method replaces the missing values in columns with "NULL" to
                                               store in the table. We are using substring in the first column to
                                               keep only "Integer" data for ease up the loading.
                                               This column is anyway going to be removed during prediction.

                                   Written By: iNeuron Intelligence
                                  Version: 1.0
                                  Revisions: None

                                          """

          try:
               log_file = open("Prediction_Logs/dataTransformLog.txt", 'a+')
               onlyfiles = [f for f in listdir(self.goodDataPath)]
               for file in onlyfiles:
                    csv = pd.read_csv(self.goodDataPath + '/' + file)
                    #csv['Wafer'] = pd.to_numeric(csv['Wafer'], errors='coerce').fillna(csv['Wafer']).astype(str).str[6:]
                    csv.fillna('NULL', inplace=True)
                    csv['Wafer'] = csv['Wafer'].str[6:]
                    csv.to_csv(self.goodDataPath+ "/" + file, header=True)
                    csv.to_csv(self.goodDataPath + "/" + file, index=False)

                    self.logger.logger(" %s: File Transformed successfully!!" % file,log_file)
                    log_file.close()
               #log_file.write("Current Date :: %s" %date +"\t" + "Current time:: %s" % current_time + "\t \t" +  + "\n")

          except Exception as e:
            log_file = open("Prediction_Logs/dataTransformLog.txt", 'a+')
            self.logger.logger( "Data Transformation failed because:: %s" % e,log_file)
            #log_file.write("Current Date :: %s" %date +"\t" +"Current time:: %s" % current_time + "\t \t" + "Data Transformation failed because:: %s" % e + "\n")
            log_file.close()
            raise e


#c=dataTransformPredict()

#c.replaceMissingWithNull()