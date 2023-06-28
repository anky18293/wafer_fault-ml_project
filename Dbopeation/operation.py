from Applogger.logger import Applogger
import sqlite3
from os import listdir
import os
import csv
from Data_validation.raw_data import rawdata
from Transformation.Transform import Transfrom



class DB:
    """In this class we will do some db operation
    """

    def __init__(self):
        self.good_path='training_data/Good_data'
        self.bad_data='training_data/Bad_data'
        self.logger=Applogger()
        self.path='Training_database/'





    def db_connection(self,database):
        """this method will try to connect my database with sqlite """


        try:
            conn=sqlite3.connect(self.good_path+database+'.db')



            file=open("Traininglog\dbconnection.txt ","w")
            self.logger.logger("database connection suceesfull ",file)
            file.close()
            return conn



        except Exception as e:
            file=open("Traininglog\Databaselog.txt","w")
            self.logger.logger("error while creating a data base {%s}"%e,file)
            file.close()


    def createtable(self,database,column_names):
        """ This method will create table ,if the databases exist it will alter
            the data column name and if not it will create the table """


        try:
            conn=sqlite3.connect("all.db") #self.db_connection(database)
            c = conn.cursor()
            c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='zaid'")
            if c.fetchone()[0]==1:
                conn.close()
                file=open("Traininglog\dbconnection.txt","w")
                self.logger.logger("database table  is present ",file)
                file.close()

            else:

             for key in column_names.keys():
                 type=column_names[key]
                 #columns = [(key, type)]
                # column_def = ",".join("{}{}".format(col[0], col[1]) for col in columns)
                 try:
                     # cur = cur.execute("SELECT name FROM {dbName} WHERE type='table' AND name='Good_Raw_Data'".format(dbName=DatabaseName))
                     conn.execute(
                         'ALTER TABLE  zaid ADD COLUMN "{column_name}" {dataType}'.format(column_name=key,
                                                                                                  dataType=type))

                 except:
                     conn.execute('CREATE TABLE  zaid ({column_name} {dataType})'.format(column_name=key, dataType=type))







             c.close()

        except Exception as e:
           file=open("Traininglog\dbconnection.txt","w")
           self.logger.logger(" kel %s :: " %e ,file)
           file.close()






    def insertintodb(self,Database):
            """ This method will inset data from good folder file to database
            """
            conn=sqlite3.connect("all.db") #self.db_connection(Database)
            goodfile=self.good_path
            badfile=self.bad_data
            onlyfile=[f for f in listdir(goodfile)]
            logfile=open("Traininglog/dbconnection.txt","w")
            c=conn.cursor()


            for files in onlyfile:
              try:
                  with open(goodfile+'/'+files,'r') as f:
                    next(f)
                    reader=csv.reader(f,delimiter="\n")
                    for i in enumerate(reader):
                        for list_ in (i[1]):
                          try:
                               c.execute('INSERT INTO zaid  values ({VALUE})'.format(VALUE=list_))
                               conn.commit()

                               self.logger.logger("%s ::insert file succesfully" % files ,logfile)
                          except Exception as e :
                              raise e


              except Exception as e:
                  #c.rollback()
                  self.logger.logger("::%s:: "%e,logfile)
                  conn.close()




    def transportintocsv(self, Database):


         self.filefromdb='Trainingfilefromdb/'
         self.filename='Inputfile.csv'
         self.logfile=open("Traininglog/dbconnection.txt",'w')

         try:
             conn=sqlite3.connect("all.db")
             cur=conn.cursor()
             sql="SELECT * FROM zaid "
             cur.execute(sql)
             result=cur.fetchall()
             header=[i[0] for i in cur.description]

             if not os.path.isdir(self.filefromdb):
                   os.makedirs(self.filefromdb)

             file=open('Trainingfilefromdb\Inputfile.csv','w',newline='')
             csv_file=csv.writer(file, delimiter=',',lineterminator='\r\n',quoting=csv.QUOTE_ALL,escapechar='\\')


             csv_file.writerow(header)
             csv_file.writerows(result)

             self.logger.logger("file expoerted",self.logfile)
             self.logfile.close()



         except Exception as e:
                self.logger.logger("::%s"%e,self.logfile)
                self.logfile.close()




#c=DB()
#z=rawdata("path")
#d,t,n,col_name=z.load()
##print(t)
##p=Transfrom()
##p.fill()
#c.createtable("training",col_name)
##c.insertintodb("training")
#c.transportintocsv("training")
##c.transportintocsv("zaid")





















