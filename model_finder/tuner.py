from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score,accuracy_score
from sklearn.model_selection import GridSearchCV
from xgboost import XGBClassifier
from Applogger.logger import  Applogger
from sklearn.model_selection import train_test_split



class model:
    def __init__(self):
        self.log=Applogger()
        self.rf=RandomForestClassifier()
        self.xgb=XGBClassifier(objective='binary:logistic')




    def parm_for_random_forest(self,train_x,train_y):
        self.file=open("Traininglog/Model.txt",'w')
        self.log.logger("Enterd into best param for random forest",self.file)
        try:
            self.best_parm={"n_estimators":[10,50,100],'criterion':['gini','entropy'],'max_depth':range(2,4,1),
                       'max_features':['log2']}
            self.grid=GridSearchCV(estimator=self.rf,param_grid=self.best_parm,cv=5,verbose=3)
            self.grid.fit(train_x,train_y)


            self.criteion=self.grid.best_params_['criterion']
            self.estimator=self.grid.best_params_['n_estimators']
            self.max_depth=self.grid.best_params_['max_depth']
            self.max_feature=self.grid.best_params_['max_features']


            self.rf=RandomForestClassifier(n_estimators=self.estimator,max_depth=self.max_depth,criterion=self.criteion,
                                      max_features=self.max_feature)
            self.rf.fit(train_x,train_y)
            self.file=open('Traininglog/Model.txt','w')
            self.log.logger("trained random forest model",self.file)
            self.file.close()
            return self.rf

        except Exception as e:
            self.file = open('Traininglog/Model.txt', 'w')
            self.log.logger("an error occured %s"%e,self.file)
            self.file.close()





    def best_parm_for_xgboost(self,train_x,train_y):

       self.file = open("Traininglog/Model.txt", 'w')
       self.log.logger("entered into xgboost model",self.file)
       try:
            self.parm= {'learning_rate': [0.5, 0.1, 0.01, 0.001],
                'max_depth': [3, 5, 10, 20],
                'n_estimators': [10, 50, 100, 200]}
            self.xg_booost = GridSearchCV(XGBClassifier(objective='binary:logistic'), self.parm, verbose=3,
                                     cv=5)
            self.xg_booost.fit(train_x,train_y)


            self.learning_rate=self.xg_booost.best_params_['learning_rate']
            self.max_depth=self.xg_booost.best_params_['max_depth']
            self.n_estimator=self.xg_booost.best_params_['n_estimators']


            self.xg=XGBClassifier(n_estimators=self.n_estimator,learning_rate=self.learning_rate,max_depth=self.max_depth)
            self.xg.fit(train_x,train_y)
            self.file = open('Traininglog/Model.txt', 'w')
            self.log.logger("training for xg_boost is done ",self.file)
            self.file.close()
            return self.xg


       except Exception as e:
            self.file = open('Traininglog/Model.txt', 'w')
            self.log.logger("error occured %s"%e,self.file)
            self.file.close()







    def best_model(self,train_x,train_y,test_x,test_y):
        """

        this method will compare between two model and give the best model deppening upon auc_roc_score return
        model name and pickel file
        """




        try:

            self.random_forest=self.parm_for_random_forest(train_x,train_y)
            prd_rf=self.random_forest.predict(test_x)


            if len(test_y.unique())==1:
                random_score=accuracy_score(test_y,prd_rf)
                #self.log.logger("The score of model is "+str(random_score),self.file)

            else:
                random_score=roc_auc_score(test_y,prd_rf)
                #self.log.logger("the score of random forest is "+str(random_score),self.file)



            self.xg_boost=self.best_parm_for_xgboost(train_x,train_y)
            prd_xg=self.xg_boost.predict(test_x)


            if len(test_y.unique()==1):
                xg_boost_score=accuracy_score(test_y,prd_xg)
                #self.log.logger("score of the xg boost is "+str(xg_boost_score),self.file)


            else:
                xg_boost_score=roc_auc_score(test_y,prd_xg)
                #self.log.logger("Scpre of the xg_boost model is  "+str(xg_boost_score),self.file)






            if (xg_boost_score>random_score):

                return 'XG_boost',self.xg_boost

            else:

                return 'Random_forest',self.random_forest





        except Exception as e:
            self.file = open('Traininglog/Model.txt', 'w')
            self.log.logger("Error happedn :::%s"%e,self.file)
            self.file.close()





#c=model()
#file=open('preprocesingfile/null_file.csv')
#z=pandas.read_csv(file)
#t=Preprocessor()
#z=t.impute_missing_values(z)
#feature=z.drop(['cluster','Labels'],axis=1)
#label=z['Labels']
##label=label.map({-1: 0, 1: 1})
#
##print(label)
#x_train,x_test,y_train,y_test=train_test_split(feature,label,test_size=1/3,random_state=33)
#c.best_parm_for_xgboost(x_train,y_train)





