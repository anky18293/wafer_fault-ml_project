from wsgiref import simple_server
from flask import Flask, request, render_template
from flask import Response
import os
from flask_cors import CORS, cross_origin
from Training_validation import train_validation
from Train_model import train_model
from predict_validation import Pred_val
from predictfrommodel import prediction

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')


app = Flask(__name__)
CORS(app)

@app.route('/predict',methods=['GET'])
@cross_origin()
def predict():
    try:
        if request.json is not None:
            path=request.json['filepath']
            pred_val=Pred_val(path)
            pred_val.predict()
            pre_model=prediction(path)
            path=pre_model.pred()
            return  Response("Predciton file has been created",headers={'Content-Type': 'application/json'})

    except Exception as e:
        return Response("Error Occurred! %s" % e, headers={'Content-Type': 'application/json'})


@app.route('/train',methods=['POST'])
@cross_origin()
def train():
    try:
        if request.json['folderPath'] is not None:
            path=request.json['folderPath']
            train_val=train_validation(path)
            train_val.train_validate()
            trainmodel=train_model()
            trainmodel.train_model()
            return Response("Traininng completed ")
    except Exception as e:
        return Response("Error happned %s" % e, headers={'Content-Type': 'application/json'})



port = int(os.getenv("PORT",5001))
if __name__ == "__main__":
    app.run(port=port,debug=True)


















