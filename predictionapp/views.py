
from django.shortcuts import redirect, render
import json
from django.http import HttpResponse,JsonResponse
# Create your views here.
import pickle
import numpy as np
def home(request):
    json_data = open('model/columns.json')
    data1 = json.load(json_data)
    global arr
    arr=data1['data_columns'][3:]
    mydictionary={
        'arr':arr
    }

    return render(request,'index.html',context=mydictionary)
def submit(request):
    a={
    'area':request.POST['Squareft'],
    'bhk':request.POST['uiBHK'],
    'bath':request.POST['uiBathrooms'],
    'location':request.POST['uiLocations']
    }
    loc_index = arr.index(a['location'])+3
    x=np.zeros(len(arr)+3)
    x[0] = int(a['area'])
    x[1] = int(a['bhk'])
    x[2] = int(a['bath'])
    am=False
    bm=False
    cm=False
    if (x[0]/x[1])<300 or (x[0]/x[1])>500:
        am=True
    if x[2]>(x[1]+1):
        bm=True
    if  x[2]<(x[1]-2):
        cm=True
    if loc_index >= 0:
        x[loc_index] = 1
    model=pickle.load(open('model/banglore_homeprice_model.pickle', 'rb'))
    k=model.predict([x])[0]
    zi=False
    if k<=0:
        zi=True
    p=str(round(k)) + ' Lakhs'
    ai=request.method
    b=False
    if ai=='POST':
        b=True
    di={
        'pi':p,
        'b':b,
        'z':zi,
        'a':a,
        'am':am,
        'bm':bm,
        'cm':cm
    }
    return render(request,'index.html',context=di)