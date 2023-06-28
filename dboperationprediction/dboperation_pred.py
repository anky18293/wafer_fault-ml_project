import shutil
import sqlite3
from os import listdir
import os
import csv
from Applogger.logger import Applogger
#from datatransformation_predection.data_transformation import dataTransformPredict
from prediction_validation_insertion.data_valodation_for_prediction import Prediction_Data_validation



class dBOperation:
    """
          This class shall be used for handling all the SQL operations.

          Written By: iNeuron Intelligence
          Version: 1.0
          Revisions: None

          """

    def __init__(self):
        self.path = 'Prediction_Database/'
        self.badFilePath = "Prediction_Raw_Files_Validated/Bad_Raw"
        self.goodFilePath = "Prediction_Raw_Files_Validated/Good_Raw"
        self.logger = Applogger()


    def dataBaseConnection(self,DatabaseName):

        """
                        Method Name: dataBaseConnection
                        Description: This method creates the database with the given name and if Database already exists then opens the connection to the DB.
                        Output: Connection to the DB
                        On Failure: Raise ConnectionError

                         Written By: iNeuron Intelligence
                        Version: 1.0
                        Revisions: None

                        """
        try:
            conn = sqlite3.connect("zaid.db")

            file = open("Prediction_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.logger( "Opened %s database successfully" % DatabaseName,file)
            file.close()
        except ConnectionError:
            file = open("Prediction_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.logger( "Error while connecting to database: %s" %ConnectionError,file)
            file.close()
            raise ConnectionError
        return conn

    def  createTableDb(self,DatabaseName,column_names):

        """
           Method Name: createTableDb
           Description: This method creates a table in the given database which will be used to insert the Good data after raw data validation.
           Output: None
           On Failure: Raise Exception

            Written By: iNeuron Intelligence
           Version: 1.0
           Revisions: None

        """
        try:
            conn =sqlite3.connect("zaid.db") #sqlite3.connect("zaid.db")
            conn.execute('DROP TABLE IF EXISTS olphine')

            for key in column_names.keys():
                type = column_names[key]

                # we will remove the column of string datatype before loading as it is not needed for training
                #in try block we check if the table exists, if yes then add columns to the table
                # else in catch block we create the table
                try:
                    #cur = cur.execute("SELECT name FROM {dbName} WHERE type='table' AND name='Good_Raw_Data'".format(dbName=DatabaseName))
                    conn.execute('ALTER TABLE olphine ADD COLUMN "{column_name}" {dataType}'.format(column_name=key,
                                                                                                           dataType=type))
                except:
                    conn.execute('CREATE TABLE olphine  ({column_name} {dataType})'.format(column_name=key, dataType=type))

            conn.close()

            file = open("Prediction_Logs/DbTableCreateLog.txt", 'a+')
            self.logger.logger( "Tables created successfully!!",file)
            file.close()

            file = open("Prediction_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.logger( "Closed %s database successfully" % DatabaseName,file)
            file.close()

        except Exception as e:
            file = open("Prediction_Logs/DbTableCreateLog.txt", 'a+')
            self.logger.logger( "Error while creating table: %s " % e,file)
            file.close()

            file = open("Prediction_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.logger( "Closed %s database successfully" % DatabaseName,file)
            file.close()
            raise e


    def insertIntoTableGoodData(self,Database):

        """
                                       Method Name: insertIntoTableGoodData
                                       Description: This method inserts the Good data files from the Good_Raw folder into the
                                                    above created table.
                                       Output: None
                                       On Failure: Raise Exception

                                        Written By: iNeuron Intelligence
                                       Version: 1.0
                                       Revisions: None

                """

        conn =sqlite3.connect("zaid.db") #sqlite3.connect("zaid.db")
        goodFilePath= self.goodFilePath
        badFilePath = self.badFilePath
        onlyfiles = [f for f in listdir(goodFilePath)]
        log_file = open("Prediction_Logs/DbInsertLog.txt", 'a+')

        for file in onlyfiles:
            try:

                with open(goodFilePath+'/'+file, "r") as f:
                    next(f)
                    reader = csv.reader(f, delimiter="\n")
                    for line in enumerate(reader):
                        for list_ in (line[1]):
                            try:
                                conn.execute('INSERT INTO olphine values ({values})'.format(values=(list_)))
                                self.logger.logger(" %s: File loaded successfully!!" % file,log_file)
                                conn.commit()
                            except Exception as e:
                                raise e

            except Exception as e:

                conn.rollback()
                self.logger.logger("Error while creating table: %s " % e,log_file)
                #shutil.move(goodFilePath+'/' + file, badFilePath)
                #self.logger.logger("File Moved Successfully %s" % file,log_file)
                log_file.close()
                conn.close()
                raise e

        conn.close()
        log_file.close()


    def selectingDatafromtableintocsv(self,Database):

        """
                                       Method Name: selectingDatafromtableintocsv
                                       Description: This method exports the data in GoodData table as a CSV file. in a given location.
                                                    above created .
                                       Output: None
                                       On Failure: Raise Exception

                                        Written By: iNeuron Intelligence
                                       Version: 1.0
                                       Revisions: None

                """

        self.fileFromDb = 'Prediction_FileFromzaid/'
        self.fileName = 'outputFile.csv'
        log_file = open("Prediction_Logs/ExportToCsv.txt", 'a+')
        try:
            conn = sqlite3.connect("zaid.db")
            sqlSelect = "SELECT *  FROM olphine"
            cursor = conn.cursor()

            cursor.execute(sqlSelect)

            results = cursor.fetchall()

            #Get the headers of the csv file
            headers = [i[0] for i in cursor.description]

            #Make the CSV ouput directory
            if not os.path.isdir(self.fileFromDb):
                os.makedirs(self.fileFromDb)

            # Open CSV file for writing.
            file=open('Prediction_FileFromzaid/outputfile.csv','w',newline='')
            csvFile = csv.writer(file,delimiter=',', lineterminator='\r\n',quoting=csv.QUOTE_ALL, escapechar='\\')

            # Add the headers and data to the CSV file.
            csvFile.writerow(headers)
            csvFile.writerows(results)

            self.logger.logger( "File exported successfully!!!",log_file)

        except Exception as e:
            self.logger.logger( "File exporting failed. Error : %s" %e,log_file)
            raise e





#c=dBOperation()
##z=dataTransformPredict()
#x=Prediction_Data_validation('Prediction_Batch_files')
#d,t,col_name,no_col=x.valuesFromSchema()
##z.replaceMissingWithNull()
#c.createTableDb("Good_Raw",col_name)
#c.insertIntoTableGoodData("Good_raw")
#c.selectingDatafromtableintocsv("Good_Raw")

