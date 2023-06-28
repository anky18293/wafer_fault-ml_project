from Applogger.logger import Applogger
from dboperationprediction.dboperation_pred import dBOperation
from datatransformation_predection.data_transformation import dataTransformPredict
from prediction_validation_insertion.data_valodation_for_prediction import  Prediction_Data_validation

class Pred_val:
    def __init__(self,path):
        self.val=Prediction_Data_validation(path)
        self.db=dBOperation()
        self.transorm=dataTransformPredict()
        self.file=open("Prediction_Logs/predictlog.txt",'w')
        self.log=Applogger()


    def predict(self):
        try:
            self.log.logger("Validation of prediction has strated ",self.file)
            Length_of_date,Length_of_time,column_name,no_of_col=self.val.valuesFromSchema()
            regex=self.val.manualRegexCreation()
            self.val.validationFileNameRaw(regex,Length_of_date,Length_of_time)
            self.log.logger("Valdatining column length",self.file)
            self.val.validateColumnLength(no_of_col)
            self.log.logger("seeing missing value",self.file)
            self.val.validateMissingValuesInWholeColumn()
            self.log.logger("validation done",self.file)
            self.log.logger("transforamtion started",self.file)
            self.transorm.replaceMissingWithNull()
            self.log.logger("transfromation has been done",self.file)
            self.db.createTableDb("Predection",column_name)
            self.log.logger("Table has been created ",self.file)
            self.log.logger("Insertion process started",self.file)
            self.db.insertIntoTableGoodData('Predection')
            self.log.logger("Insertion has been done",self.file)
            self.val.deleteExistingGoodDataTrainingFolder()
            self.val.moveBadFilesToArchiveBad()
            self.log.logger("Selecting data from csv file",self.file)
            self.db.selectingDatafromtableintocsv('Predection')
            self.log.logger("Sent it to predictionfilefromzaid",self.file)
        except Exception as e:
            file=open("Prediction_Logs/predictlog.txt",'w')
            self.log.logger("Error",file)
            file.close()


#c=Pred_val()
#c.predict()