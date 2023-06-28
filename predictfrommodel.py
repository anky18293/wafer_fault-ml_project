import pandas as pd
from fileoperation.fileoperation import fileobject
from Applogger.logger import Applogger
from prediction_validation_insertion.data_valodation_for_prediction import Prediction_Data_validation
from data_preprocsessing.data_preprocessing import Preprocessor
from data_getter_output.Data import data



class prediction:
    def __init__(self,path):
        self.file=fileobject()
        self.log=Applogger()
        self.getter=data()
        #if path is not None:
        self.val=Prediction_Data_validation(path)
        self.pre=Preprocessor()



    def pred(self):
        try:
         self.val.deletePredictionFile()
         self.obj=open("Prediction_Logs/Predict.txt","w")
         self.log.logger("prediction has started",self.obj)
         data1=self.getter.getter()
         null=self.pre.is_null_present(data1)
         if (null):
             data1=self.pre.impute_missing_values(data1)
         #cols_to_drop=self.pre.get_columns_with_zero_std_deviation(data1)
         #self.pre.remove_columns(data1,cols_to_drop)
         kmeans=self.file.load_model("kmean")
         cluster=kmeans.predict(data1.drop(labels="Wafer",axis=1))
         data1["cluster"]=cluster
         clus_unique=data1["cluster"].unique()
         for i in clus_unique:
           cluster_data=data1[data1["cluster"]==i]
           wafer_name=list(cluster_data["Wafer"])
           cluster_data=cluster_data.drop(labels=["Wafer"],axis=1)
           cluster_data=cluster_data.drop(labels=["cluster"],axis=1)
           model_name=self.file.find_correct_model(i)
           model=self.file.load_model(model_name)
           result=list(model.predict(cluster_data))
           result=pd.DataFrame(zip(wafer_name,result),columns=['wafer','result'])
           path="Predictionfile/result.csv"
           result.to_csv("Predictionfile/result.csv",header=True,mode="a+")
         self.log.logger("end of prediection",self.obj)

        except Exception as e:
           self.obj=open("Prediction_Logs/Predict.txt","w")
           self.log.logger("error:::%s"%e,self.obj)
           #return path,result.head().to_json(orient="Records")

c=prediction('path')
c.pred()