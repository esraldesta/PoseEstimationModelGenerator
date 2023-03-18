from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
def Home(request):
    return render(request,"core/home.html",{})




from django.shortcuts import render
from .forms import UploadFileForm

import numpy as np
import mediapipe as mp
import os
import json
import cv2
import csv

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression,RidgeClassifier
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier

from sklearn.metrics import accuracy_score,precision_score,recall_score
import pickle

import operator
def export_landmark(results,action,exersice_name):
    csvpath = "uploads/"+exersice_name+"/" + "coordsNew.csv"
    try:
        keypoints = np.array([[res.x,res.y,res.z,res.visibility]for res in results.pose_landmarks.landmark]).flatten().tolist()
        keypoints.insert(0,action)
        with open(csvpath,mode="a",newline="") as f:
            csv_wirter = csv.writer(f,delimiter=",",quotechar='"',quoting=csv.QUOTE_MINIMAL)
            csv_wirter.writerow(keypoints)
    except Exception as e:
        pass
mp_pose = mp.solutions.pose

def upload_display_video(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            mydata_str = request.POST.get('mydata')
            exersice_name = request.POST.get('exersice_name')
            mydata = json.loads(mydata_str)
            vidoe_des,text_dest = handle_uploaded_file(exersice_name,file,mydata)
            print("vidoe_des "+vidoe_des)
            print("text_dest "+text_dest)
            landmarks = ["class"]
            for val in range(1,33+1):
                landmarks += ['x{}'.format(val),'y{}'.format(val),"z{}".format(val),'v{}'.format(val)]


            ## lables of the csv
            landmarks[1:]

            ## saving the lables
            csvpath = "uploads/"+exersice_name+"/" + "coordsNew.csv"
            with open(csvpath,mode="w",newline="") as f:
                csv_wirter = csv.writer(f,delimiter=",",quotechar='"',quoting=csv.QUOTE_MINIMAL)
                csv_wirter.writerow(landmarks)
            with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:            
                cap = cv2.VideoCapture(vidoe_des)
                fps = cap.get(cv2.CAP_PROP_FPS)
                print('frames per second =',fps)

                with open(text_dest) as f:
                    data = json.load(f)
                    for label in data.keys():
                        for seconds,minutes in data[label]:
                            frame_id = int(fps*(minutes*60 + seconds))
                            print('frame id =',frame_id)
                            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)

                            try:
                                ret, frame = cap.read()


                                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                                image.flags.writeable = False

                                results = pose.process(image)

                                export_landmark(results,label,exersice_name) 
                            except Exception as e:
                                break
                ## generating model
                csv_path = "uploads/"+exersice_name+"/" + "coordsNew.csv"
                df = pd.read_csv(csv_path)
                x= df.drop('class',axis=1)
                y=df["class"]

                X_train,X_test,Y_train,Y_test  = train_test_split(x,y,test_size=0.3,random_state=1234)
                pipelines = {
                    "lr":make_pipeline(StandardScaler(),LogisticRegression()),
                    "rc":make_pipeline(StandardScaler(),RidgeClassifier()),
                    "rf":make_pipeline(StandardScaler(),RandomForestClassifier()),
                    "gb":make_pipeline(StandardScaler(),GradientBoostingClassifier()),
                }

                fit_models = {}

                for algo,pipeline in pipelines.items():
                    model = pipeline.fit(X_train,Y_train)
                    fit_models[algo]=model
                results = {}
                for algo,model in fit_models.items():
                    yhat = model.predict(X_test)
                    acc = accuracy_score(Y_test.values,yhat)
                    # prec = precision_score(Y_test.values,yhat,average="binary",pos_label="up")
                    # rec = recall_score(Y_test.values,yhat,average="binary",pos_label="up")
                    # results[algo] = {"accuracy": acc, "precision": prec, "recall": rec}
                    results[algo] = {"accuracy": acc}
                
                # for algo,result in results.items():
                    # print(algo, result["accuracy"], result["precision"], result["recall"])
                    # print(algo, result["accuracy"])
                
                sorted_models = sorted(results.items(), key=lambda x: x[1]['accuracy'], reverse=True)
                best_model = sorted_models[0][0]
                model_path = "uploads/"+exersice_name+"/" + "mymodel.pkl"
                print("Best model:", best_model)

                with open(model_path,"wb") as f:
                    pickle.dump(fit_models[best_model],f)
            
            return JsonResponse({"download_link":"http://127.0.0.1:8000/"+model_path})
            # return render(request, "core/response.html", {'filename': file.name,"download_link":"http://127.0.0.1:8000/"+model_path})
    else:
        form = UploadFileForm()
    return render(request, 'core/upload-display-video.html', {'form': form})

def handle_uploaded_file(exersice_name,file,mydata):
    vidoe_des = "uploads/"+exersice_name+"/" + file.name
    text_dest = "uploads/"+exersice_name+"/" + file.name.split(".")[0]+".json"
    os.makedirs("uploads/"+exersice_name)
    with open(vidoe_des, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    with open(text_dest, 'w+') as destination:
        destination.write(json.dumps(mydata))

    return [vidoe_des,text_dest]