from Applogger.logger import Applogger
from sklearn.cluster import KMeans
from kneed import  KneeLocator
import matplotlib.pyplot as plt
from fileoperation.fileoperation import fileobject


class cluster:
    """ this  class will give appropate cluster and clustr formation
    """

    def __init__(self):
        self.log=Applogger()
        self.model=fileobject()


    def elbowplot(self,data):
        self.file = open('Traininglog/cluster.txt', 'a+')
        wcss=[]
        try:
            for i in range(1,11):
                k=KMeans(n_clusters=i,init='k-means++',random_state=42)
                k.fit(data)
                wcss.append(k.inertia_)
            plt.plot(range(1,11),wcss)
            plt.title('The elbow method')
            plt.xlabel('number of x label')
            plt.ylabel('WCSS')
            plt.savefig('data_preprocsessing/figure of cluster.png')
            self.kne=KneeLocator(range(1,11),wcss,curve='convex',direction='decreasing')
            self.log.logger("sucessfully transfered  apporpraita cluser number  ",self.file)
            self.file.close()
            return  self.kne.knee

        except Exception as e:
            self.file = open('Traininglog/cluster.txt', 'a+')
            self.log.logger("error happened::%s"%e,self.file)
            self.file.close()




    def create_cluster(self,data,cluster_num):
        self.file = open('Traininglog/cluster.txt', 'a+')
        self.data=data
        try:
            km=KMeans(n_clusters=cluster_num,init='k-means++',random_state=42)
            data_of_cluster=km.fit_predict(self.data)
            self.model.save_model(km, 'kmean')
            self.data['cluster']=data_of_cluster
            return self.data
        except Exception as e:
            self.file = open('Traininglog/cluster.txt', 'a+')
            self.log.logger("error occured ::%s"%e,self.file)
            self.file.close()