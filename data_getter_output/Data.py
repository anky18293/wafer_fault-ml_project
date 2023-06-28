import pandas as pd



class data:
    def __init__(self):
        self.file="Prediction_FileFromzaid/outputfile.csv"

    def getter(self):
        file=pd.read_csv(self.file)
        return file


#c=data()
#d=c.getter()
#print(d)