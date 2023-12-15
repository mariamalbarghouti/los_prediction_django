# import csv

from django.shortcuts import render
import joblib
import pandas as pd
import numpy as np

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
# from .forms import AssessmentForm

# Create your views here.
# from django.shortcuts import render
# from django.http import HttpResponse

# def index(request):
#     return HttpResponse("Hello World")
specific_assessment = {"Assessment_650": "Normal Delivery",
                       "Assessment_669.70": "Cesarean delivery, without mention of indication, unspecified as to episode of care",
                       "Assessment_669.71": "Cesarean delivery, without mention of indication, delivered, with or without mention of antepartum condition"
                       }
days = {'Friday', 'Saturday',  'Saturday', 'Sunday',  'Thursday',  'Tuesday', 'Wednesday'}
months= {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
        7: 'July', 8:'August', 9:'September', 10:'October',11:'November',12:'December'}
def index(request):
    submit_form(request)
    return render(request, 'pages/index.html', {"specific_assessment":specific_assessment,'days':days,'months':months})

# def get_doctor_names_file():

#   # Create an empty list to store doctor names
#   doctor_names = []

#   # Specify the file path to your CSV file (replace 'x.csv' with your file's path)
#   csv_file_path = 'D:/work/los_model/New folder/professional _names.csv'

#   # Read the CSV file and extract the "Professional Name" column
#   with open(csv_file_path, 'r', newline='') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#           professional_name = row.get("Professional Name")
#           if professional_name:
#               doctor_names.append(professional_name)
#   # Now, the doctor_names list contains all the values from the "Professional Name" column
#   return doctor_names


def submit_form(request):
    if request.method == 'POST':
        prediction_value = applyModel(request.POST)
        if prediction_value!="Error":
          return render(request, 'pages/prediction.html', {'prediction_value': prediction_value})

    return redirect('index')

def applyModel(data):
    if (data.get('delivery_month') != "Select Month") and (
            (data.get('selected_assessment') != 'Select Specific Assessment') and (
            data.get('delivery_day') != "Select Delivery Day")):
        model, col, target = joblib.load("static/model/model.h")
        print(data.get('delivery_month'))
        print(data.get('selected_assessment'))
        print(data.get('delivery_day'))

        data = {
             'ER': [data.get('er')],
             'Month': [data.get('delivery_month')],
             'Assessment_650': [1 if (data.get('selected_assessment') == 'Assessment_650') else 0],
             'Assessment_669.70': [1 if (data.get('selected_assessment') == 'Assessment_669.70') else 0],
             'Assessment_669.71': [1 if (data.get('selected_assessment') == 'Assessment_669.71') else 0],
             'Day_Friday': [1 if ("Day_"+data.get('delivery_day') == 'Day_Friday') else 0],
             'Day_Monday': [1 if ("Day_"+data.get('delivery_day') == 'Day_Monday') else 0],
             'Day_Saturday': [1 if ("Day_"+data.get('delivery_day') == 'Day_Saturday') else 0],
             'Day_Sunday': [1 if ("Day_"+data.get('delivery_day') == 'Day_Sunday') else 0],
             'Day_Thursday': [1 if ("Day_"+data.get('delivery_day') == 'Day_Thursday') else 0],
             'Day_Tuesday': [1 if ("Day_"+data.get('delivery_day') == 'Day_Tuesday') else 0],
             'Day_Wednesday': [1 if ("Day_"+data.get('delivery_day') == 'Day_Wednesday') else 0],
             }

        df = pd.DataFrame(data)
        prediction_value = np.ceil(model.predict(df.iloc[0:1]))
        print(prediction_value[0])

        return prediction_value[0]
    else:
        return "Error"