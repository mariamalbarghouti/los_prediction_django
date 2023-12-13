import csv

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

# def index(request):
#     return HttpResponse("Hello World")

def index(request):
    # TODO
    providers= get_doctor_names_file()
    specific_assessment= {"650":"Normal Delivery", "669.71": "Cesarean delivery, without mention of indication, delivered, with or without mention of antepartum condition",  "669.70":"Cesarean delivery, without mention of indication, unspecified as to episode of care"}
    return render(request, 'pages/index.html', {"specific_assessment":specific_assessment})

def get_doctor_names_file():

   # Create an empty list to store doctor names
   doctor_names = []

   # Specify the file path to your CSV file (replace 'x.csv' with your file's path)
   csv_file_path = 'D:/work/los_model/New folder/professional _names.csv'

   # Read the CSV file and extract the "Professional Name" column
   with open(csv_file_path, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
           professional_name = row.get("Professional Name")
           if professional_name:
              doctor_names.append(professional_name)
   # Now, the doctor_names list contains all the values from the "Professional Name" column
   return doctor_names

def hey(request):
    return render(request, 'pages/hey.html')
