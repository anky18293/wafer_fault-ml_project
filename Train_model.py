from Applogger.logger import   Applogger
from loadfile.dataload import data
from fileoperation.fileoperation import fileobject
from data_preprocsessing.cluster import cluster
from data_preprocsessing.data_preprocessing import Preprocessor
from model_finder.tuner import model
from sklearn.model_selection import train_test_split
import pandas


class train_model:


    def __init__(self):
        self.log=Applogger()
        self.load_file=data()
        self.file_opeartaion=fileobject()
        self.cluster=cluster()
        self.processing=Preprocessor()
        self.model=model()



    def train_model(self):

      try:
           with open ('Traininglog/training_log', 'a+') as file:
             self.log.logger("start of training",file)
           data=self.load_file.loader()


           """removing column"""
           data=self.processing.remove_columns(data,['Wafer'])
           file = open('Traininglog/training_log', 'a+')
           self.log.logger("removing column Wafer",file)



           """seprating label and feature"""
           X,Y=self.processing.separate_label_feature(data,label_column_name='Output')
           null_present_on=self.processing.is_null_present(X)
           if (null_present_on):
              X=self.processing.impute_missing_values(X)
           #cols_to_drop=self.processing.get_columns_with_zero_std_deviation(X)
           #X=self.processing.remove_columns(X,cols_to_drop)
           cluster_num=self.cluster.elbowplot(X)
           X=self.cluster.create_cluster(X,cluster_num)
           X['Labels']=Y
           X.to_csv("null_file.csv")
           list_of_cluster=X['cluster'].unique()
           self.log.logger("list of cluster {}".format(list_of_cluster),file)
           for i in list_of_cluster:
             cluster_data=X[X['cluster']==i]
             cluster_feature=cluster_data.drop(["cluster","Labels"],axis=1)
             cluster_output=cluster_data['Labels']
             x_train,x_test,y_train,y_test=train_test_split(cluster_feature,cluster_output,test_size=1/3,random_state=33)
             model_name,model=self.model.best_model(x_train,y_train,x_test,y_test)
             self.file_opeartaion.save_model(model,model_name+str(i))
           self.log.logger("Suceesfull training",file)

      except  Exception as e:
          file = open('Traininglog/training_log', 'a+')
          self.log.logger("%s"%e,file)














#c=train_model()

#c.train_model()










