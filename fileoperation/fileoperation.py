from Applogger.logger import Applogger
import os
import shutil
import pickle



class fileobject:
    """
    this methhod will save model ,load model ,and find correct model
    """


    def __init__(self):
        self.model_directory='model/'
        self.logger=Applogger()
        #self.file=open('Traininglog/Savedmodel.txt','w')


    def save_model(self,model,filename):
        #self.logger.logger("Entred the saving model of file obeject class",self.file)
        try:
            path=os.path.join(self.model_directory+filename)
            if os.path.isdir(path):
                shutil.rmtree(self.model_directory)
                os.makedirs(path)
            else:
                os.makedirs(path)
            with open(path+'/'+filename+'.sav','wb') as f:
                pickle.dump(model,f)
            #self.logger.logger("model saved",self.file)
            #self.file.close()

        except Exception as e:
            with open('Traininglog/traininglog.txt', 'w') as file:
               self.logger.logger("Error :::%s",file)
            #self.file.close()






    def load_model(self,filename):
        try:
            with open(self.model_directory+filename+'/'+filename+'.sav','rb') as f:
                 return pickle.load(f)


        except Exception as e:
            with open('Traininglog/traininglog.txt','w') as file:
                self.logger.logger("error:::%s"%e,file)
            #self.file.close()





    def find_correct_model(self,cluster_number):
        """
        to find correct model from the cluster number


         """

        #self.logger.logger("enter to find correct model ",self.file)
        try:
            self.cluster_number=cluster_number
            self.model=self.model_directory
            self.list_of_model=[]
            self.list_of_models=os.listdir(self.model)
            for file in self.list_of_models:
                try:
                    if (file.index(str(self.cluster_number))!=-1):
                        self.model_name=file
                except:
                    continue
            self.model_name=self.model_name.split(',')[0]
            return self.model_name
        except Exception as e:
            with open('Traininglog/traininglog.txt', 'w') as file:
               self.logger.logger("error happed::%s"%e,file)
            #self.file.close()










