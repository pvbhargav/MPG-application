from django.shortcuts import render
import joblib
import pandas as pd

reloadModel=joblib.load('./models/RFModelforMPG.pkl')

from pymongo import MongoClient
# client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['mpgDataBase']
collectionD = db['mpgTable']

def index(request):
    # temp={}
    # temp['cylinders']=8
    # temp['displacement']=307
    # temp['horsepower']=130
    # temp['weight']=3504
    # temp['acceleration']=12
    # temp['model_year']=70
    # temp['origin']=1
    # context={'temp':temp}
    return render(request,'index.html')
    
def predictMPG(request):
    if request.method=="POST":
        temp={}
        temp['cylinders']=request.POST.get('cylinderVal')
        temp['displacement']=request.POST.get('dispVal')
        temp['horsepower']=request.POST.get('hrsPwrVal')
        temp['weight']=request.POST.get('weightVal')
        temp['acceleration']=request.POST.get('accVal')
        temp['model_year']=request.POST.get('modelVal')
        temp['origin']=request.POST.get('originVal')
        temp2=temp.copy()
        temp2['model year']=temp['model_year']
        
    testDtaa=pd.DataFrame({'x':temp2}).transpose()
    scoreval=reloadModel.predict(testDtaa)[0]
    context={'scoreval':scoreval,'temp':temp}
    return render(request,'index.html',context)

def viewDatabase(request):
    countOfrow = collectionD.count_documents({})
    context={'countOfrow':countOfrow}
    return render(request,'viewDB.html',context)

def updateDataBase(request):
    temp={}
    temp['cylinders']=request.POST.get('cylinderVal')
    temp['displacement']=request.POST.get('dispVal')
    temp['horsepower']=request.POST.get('hrsPwrVal')
    temp['weight']=request.POST.get('weightVal')
    temp['acceleration']=request.POST.get('accVal')
    temp['model year']=request.POST.get('modelVal')
    temp['origin']=request.POST.get('originVal')
    temp['mpg']=request.POST.get('mpgVal')
    collectionD.insert_one(temp)
    countOfrow = collectionD.count_documents({})

    
    context={'countOfrow':countOfrow}
    return render(request,'viewDB.html',context)
