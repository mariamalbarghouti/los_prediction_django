import csv

import numpy as np
import pandas as pd
from io import BytesIO, StringIO
from django.shortcuts import render, redirect
import requests
from keras.models import load_model
provider_names = []
diagnosis_list = []

specific_assessment = {"Assessment_650": "Normal Delivery",
                       "Assessment_669.70": "Cesarean delivery, without mention of indication, unspecified as to episode of care",
                       "Assessment_669.71": "Cesarean delivery, without mention of indication, delivered, with or without mention of antepartum condition"
                       }
days = {'Friday', 'Saturday', 'Saturday', 'Sunday', 'Thursday', 'Tuesday', 'Wednesday'}
month_names = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
               7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}


def index(request):
    getProviderNames()
    getDiagnosis()
    submit_form(request)
    return render(request, 'pages/index.html', {"specific_assessment": specific_assessment,
                                                'days': days, 'months': month_names, "diagnosis_list": diagnosis_list,
                                                "provider_names": provider_names})


def getDiagnosis():
    # diagnosis_file_path = 'D:/work/los_model/New folder/los_ui/los_prediction/src/static/local_data/diagnosis.csv'
    diagnosis_file_path = 'https://raw.githubusercontent.com/mariamalbarghouti/los_prediction_django/main/diagnosis.csv'
    df = pd.read_csv(diagnosis_file_path, sep='\t')
    diagnosis_list.extend(df.values.flatten().tolist())


def getProviderNames():
    provider_file_path = 'https://raw.githubusercontent.com/mariamalbarghouti/los_prediction_django/main/provider_name.csv'

    # Fetch the raw content of the CSV file
    response = requests.get(provider_file_path)
    if response.status_code == 200:
        csv_content = StringIO(response.text)
        reader = csv.DictReader(csv_content)
        for row in reader:
            print("Dreem",row )
            provider_names.append(row['Provider Name_Al �Iman Hospital'])

    else:
        print(f"Failed to fetch CSV file from GitHup. Status code: {response.status_code}")


def submit_form(request):
    if request.method == 'POST':
        prediction_value = applyModel(request.POST)
        print("Post value =======>", prediction_value)
        if prediction_value != "Error":
            return render(request, 'pages/prediction.html', {'prediction_value': prediction_value})
    return redirect('index')


def applyModel(data):
    print("ER", data.get('er'))
    print("Age", data.get('age'))
    print("Month", data.get('delivery_month'))
    print("Day", data.get('delivery_day'))
    print("Specific", data.get('selected_assessment'))
    print(data.get('diagnosis'))
    print(data.get('provider_name'))
    if (data.get('delivery_month') != "Select Month") and (
            (data.get('selected_assessment') != 'Select Specific Assessment') and (
            data.get('delivery_day') != "Select Delivery Day")):

        # model = load_model('D:/work/los_model/New folder/los_ui/los_prediction/src/static/model/last_model.h5')
        # return dealingWithModel(model, data)
        csv_url = 'https://raw.githubusercontent.com/mariamalbarghouti/los_prediction_django/main/provider_name.csv'

        # Fetch the raw content of the CSV file
        response = requests.get(csv_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Use StringIO to create a file-like object from the string content
            csv_content = StringIO(response.text)

            # Read the CSV content
            reader = csv.DictReader(csv_content)

            # List to store provider names
            provider_names = []

            # Extract the 'Provider Name_Al Iman Hospital' column and remove double spaces
            for row in reader:
                provider_name = row['Provider Name_Al Iman Hospital']
                provider_name = provider_name.replace('  ', ' ')  # Replace double spaces with a single space
                provider_names.append(provider_name)

            return provider_names
        else:
            # Print an error message if the request was not successful
            print(f"Failed to fetch CSV file from {csv_url}. Status code: {response.status_code}")

        return "Error"
    else:
        return "Error"


def dealingWithModel(model, data):
    data2 = {'ER': [0],
 'Age': [30],
 'Month': [1],
 'Specific Assessment_650 Normal Delivery': [0],
 'Specific Assessment_669.70 Cesarean delivery, without mention of indication, unspecified as to episode of care': [0],
 'Specific Assessment_669.71 Cesarean delivery, without mention of indication, delivered, with or without mention of antepartum condition': [1],
 'Day_Friday': [1],
 'Day_Monday': [0],
 'Day_Saturday': [0],
 'Day_Sunday': [0],
 'Day_Thursday': [0],
 'Day_Tuesday': [0],
 'Day_Wednesday': [0],
 'Discharge Diagnosis_218.9 Leiomyoma Of Uterus, Unspecified': [0],
 'Discharge Diagnosis_281.9 Unspecified Deficiency Anemia': [0],
 'Discharge Diagnosis_285.9 Anemia, Unspecified': [0],
 'Discharge Diagnosis_435.9 Unspecified Transient Cerebral Ischemia': [0],
 'Discharge Diagnosis_553.1 Umbilical Hernia Without Mention Of Obstruction Or Gangrene': [0],
 'Discharge Diagnosis_575.10 Cholecystitis, Unspecified': [0],
 'Discharge Diagnosis_640.80 Other specified hemorrhage in early pregnancy, unspecified as to episode of care': [0],
 'Discharge Diagnosis_641.11 Hemorrhage from placenta previa, with delivery': [0],
 'Discharge Diagnosis_642.40 Mild or unspecified pre-eclampsia, unspecified as to episode of care': [0],
 'Discharge Diagnosis_649.50 Spotting complicating pregnancy, unspecified as to episode of care or not applicable': [0],
 'Discharge Diagnosis_650 Normal Delivery': [0],
 'Discharge Diagnosis_658.11 Premature rupture of membranes in pregnancy, delivered': [0],
 'Discharge Diagnosis_669.70 Cesarean delivery, without mention of indication, unspecified as to episode of care': [0],
 'Discharge Diagnosis_669.71 Cesarean delivery, without mention of indication, delivered, with or without mention of antepartum condition': [0],
 'Discharge Diagnosis_780.60 Fever, unspecified': [0],
 'Discharge Diagnosis_782.1 Rash And Other Nonspecific Skin Eruption': [0],
 'Discharge Diagnosis_784.0 Headache': [0],
 'Discharge Diagnosis_784.1 Throat Pain': [0],
 'Discharge Diagnosis_B34.2 Coronavirus infection, unspecified': [0],
 'Discharge Diagnosis_N80.3 Endometriosis of pelvic peritoneum': [0],
 'Discharge Diagnosis_N83.0 Follicular cyst of ovary': [0],
 'Discharge Diagnosis_O14.10 Severe pre-eclampsia, unspecified trimester': [0],
 'Discharge Diagnosis_O14.13 Severe pre-eclampsia, third trimester': [0],
 'Discharge Diagnosis_O14.93 Unspecified pre-eclampsia, third trimester': [0],
 'Discharge Diagnosis_O16.3 Unspecified maternal hypertension, third trimester': [0],
 'Discharge Diagnosis_O32.1XX0 Maternal care for breech presentation, not applicable or unspecified': [0],
 'Discharge Diagnosis_O32.1XX1 Maternal care for breech presentation, fetus 1': [0],
 'Discharge Diagnosis_O33.9 Maternal care for disproportion, unspecified': [0],
 'Discharge Diagnosis_O34.21 Maternal care for scar from previous cesarean delivery': [0],
 'Discharge Diagnosis_O34.29 Maternal care due to uterine scar from other previous surgery': [0],
 'Discharge Diagnosis_O36.4XX0 Maternal care for intrauterine death, not applicable or unspecified': [0],
 'Discharge Diagnosis_O36.5930 Maternal care for other known or suspected poor fetal growth, third trimester, not applicable or unspecified': [0],
 'Discharge Diagnosis_O36.5990 Maternal care for other known or suspected poor fetal growth, unspecified trimester, not applicable or unspecified': [0],
 'Discharge Diagnosis_O36.63X1 Maternal care for excessive fetal growth, third trimester, fetus 1': [0],
 'Discharge Diagnosis_O41.03X0 Oligohydramnios, third trimester, not applicable or unspecified': [0],
 'Discharge Diagnosis_O44.00 Placenta previa specified as without hemorrhage, unspecified trimester': [0],
 'Discharge Diagnosis_O44.03 Placenta previa specified as without hemorrhage, third trimester': [0],
 'Discharge Diagnosis_O45.8X3 Other premature separation of placenta, third trimester': [0],
 'Discharge Diagnosis_O45.93 Premature separation of placenta, unspecified, third trimester': [0],
 'Discharge Diagnosis_O60.12X1 Preterm labor second trimester with preterm delivery second trimester, fetus 1': [0],
 'Discharge Diagnosis_O60.14X0 Preterm labor third trimester with preterm delivery third trimester, not applicable or unspecified': [0],
 'Discharge Diagnosis_O60.14X1 Preterm labor third trimester with preterm delivery third trimester, fetus 1': [0],
 'Discharge Diagnosis_O60.14X2 Preterm labor third trimester with preterm delivery third trimester, fetus 2': [0],
 'Discharge Diagnosis_O62.0 Primary inadequate contractions': [0],
 'Discharge Diagnosis_O62.1 Secondary uterine inertia': [0],
 'Discharge Diagnosis_O62.4 Hypertonic, incoordinate, and prolonged uterine contractions': [0],
 'Discharge Diagnosis_O66.40 Failed trial of labor, unspecified': [0],
 'Discharge Diagnosis_O66.41 Failed attempted vaginal birth after previous cesarean delivery': [0],
 'Discharge Diagnosis_O68 Labor and delivery complicated by abnormality of fetal acid-base balance': [0],
 'Discharge Diagnosis_O75.82 Onset (spontaneous) of labor after 37 completed weeks of gestation but before 39 completed weeks gestation, with delivery by (planned) cesarean section': [0],
 'Discharge Diagnosis_O76 Abnormality in fetal heart rate and rhythm complicating labor and delivery': [0],
 'Discharge Diagnosis_O77.9 Labor and delivery complicated by fetal stress, unspecified': [0],
 'Discharge Diagnosis_O80 Encounter for full-term uncomplicated delivery': [0],
 'Discharge Diagnosis_O82 Encounter for cesarean delivery without indication': [0],
 'Discharge Diagnosis_O98.511 Other viral diseases complicating pregnancy, first trimester': [1],
 'Discharge Diagnosis_O99.013 Anemia complicating pregnancy, third trimester': [0],
 'Discharge Diagnosis_P59.9 Neonatal jaundice, unspecified': [0],
 'Discharge Diagnosis_V27.0 Outcome of delivery, single liveborn': [0],
 'Discharge Diagnosis_V27.1 Outcome of delivery, single stillborn': [0],
 'Discharge Diagnosis_V27.2 Outcome of delivery, twins, both liveborn': [0],
 'Discharge Diagnosis_V27.9 Outcome of delivery, unspecified': [0],
 'Discharge Diagnosis_Z01.818 Encounter for other preprocedural examination': [0],
 'Discharge Diagnosis_Z37.0 Single live birth': [0],
 'Discharge Diagnosis_Z37.1 Single stillbirth': [0],
 'Discharge Diagnosis_Z37.2 Twins, both liveborn': [0],
 'Discharge Diagnosis_Z38.00 Single liveborn infant, delivered vaginally': [0],
 'Discharge Diagnosis_Z38.01 Single liveborn infant, delivered by cesarean': [0],
 'Discharge Diagnosis_Z38.31 Twin liveborn infant, delivered by cesarean': [0],
 'Discharge Diagnosis_Z82.0 Family history of epilepsy and other diseases of the nervous system': [0],
 'Provider Name_Al  Iman Hospital': [1],
 'Provider Name_Al  Zahraa Hospital': [0],
 'Provider Name_Al Assy Hospital': [0],
 'Provider Name_Al Jabal Hospital - Kornayel': [0],
 'Provider Name_Al Rayan Hospital': [0],
 'Provider Name_Al-Hayat Hospital': [0],
 'Provider Name_American University of Beirut Medical Center': [0],
 'Provider Name_Baakline Medical Center': [0],
 'Provider Name_Bahman Hospital': [0],
 'Provider Name_Bekaa Hospital': [0],
 'Provider Name_Bellevue Medical Center': [0],
 'Provider Name_CHU - Notre Dame Des Secours Hospital': [0],
 'Provider Name_Centre  Hospitalier Du Nord': [0],
 'Provider Name_Chtaura Hospital': [0],
 'Provider Name_Clemenceau Medical Center': [0],
 'Provider Name_Clemenceau Medical center-UAE': [0],
 'Provider Name_Clinique Dr. Georges Moarbes': [0],
 'Provider Name_Clinique Du Levant': [0],
 'Provider Name_Dallaa  Hospital': [0],
 'Provider Name_Dar Al Chifaa hospital': [0],
 'Provider Name_Dr. H. Farhat Hospital': [0],
 'Provider Name_El Youssef Medical Center': [0],
 'Provider Name_Fakih Hospital': [0],
 'Provider Name_Family Medical Center  - FMC': [0],
 'Provider Name_Hammoud Hospital University Medical Center': [0],
 'Provider Name_Health Medical Center': [0],
 'Provider Name_Hiram Hospital': [0],
 'Provider Name_Hopital Abou Jaoudeh': [0],
 'Provider Name_Hopital Ain Wazein': [0],
 'Provider Name_Hopital Al Koura': [0],
 'Provider Name_Hopital Dr. S. Serhal': [0],
 'Provider Name_Hopital El Arz': [0],
 'Provider Name_Hopital Haddad des Soeurs du Rosaire': [0],
 'Provider Name_Hopital Islamique de Bienfaisance': [0],
 'Provider Name_Hopital Libano-Francais': [0],
 'Provider Name_Hopital Monla': [0],
 'Provider Name_Hopital Nini': [0],
 'Provider Name_Hopital Notre Dame De La Paix - Kobeyat': [0],
 'Provider Name_Hopital Notre Dame Maritime': [0],
 'Provider Name_Hopital Rayak': [0],
 'Provider Name_Hopital Sacre-Coeur': [0],
 'Provider Name_Hopital St. Charles': [0],
 'Provider Name_Hopital St. Joseph': [0],
 'Provider Name_Hopital Tel Chiha': [0],
 'Provider Name_Hopital Universitaire Dar Al Amal': [0],
 'Provider Name_Hospital Albert Haykal': [0],
 'Provider Name_Hotel-Dieu De France': [0],
 'Provider Name_Iklim Health Foundation': [0],
 'Provider Name_Irfan Medical Center': [0],
 'Provider Name_Islamic Health Society Hospital-Bent jbeil': [0],
 'Provider Name_Jabal Amel Hospital': [0],
 'Provider Name_Kassab Hospital s.a.l': [0],
 'Provider Name_Keserwan Medical Center': [0],
 'Provider Name_Khoury General Hospital': [0],
 'Provider Name_LAUMC - St. John Hospital': [0],
 'Provider Name_Labib Medical Center': [0],
 'Provider Name_Lebanese Healthcare Management (L.H.M) SAL': [0],
 'Provider Name_Lebanese Italian Hospital': [0],
 'Provider Name_Makassed General Hospital': [0],
 'Provider Name_Meiss Al Jabal Governmental Hospital': [0],
 'Provider Name_Middle East Institute Of Health': [0],
 'Provider Name_Mount Lebanon Hospital': [0],
 'Provider Name_NEXtCARE OEA': [0],
 'Provider Name_Nabih Berri Governental Uni Hosp of Nabatieh': [0],
 'Provider Name_Najjar Hospital- General Hospital  Institute': [0],
 'Provider Name_New Hospital Mazloum': [0],
 'Provider Name_Rachaya Governmental Hospital': [0],
 'Provider Name_Raee Hospital': [0],
 'Provider Name_Rassoul Al Aazam Hospital': [0],
 'Provider Name_Sahel General Hospital': [0],
 'Provider Name_Saint George Medical Center (SGMC)': [0],
 'Provider Name_Secours Populaire Libanais': [0],
 'Provider Name_Sheikh Khalaf Hamad Al Habtoor - Medical Line': [0],
 'Provider Name_Sheikh Ragheb Harb Hospital': [0],
 'Provider Name_Siblin Governmental Hospital': [0],
 'Provider Name_St. George Hospital - University Medical Center': [0],
 'Provider Name_Taanayel General Hospital': [0],
 'Provider Name_Trad Hospital & Medical Center': [0],
 'Provider Name_University Medical Center - Rizk Hospital': [0]}
    data3 = pd.DataFrame(data2)
    prediction_value = model.predict(data3)
    prediction_ceil_value = np.ceil(prediction_value)
    return np.array(prediction_ceil_value[0])[0]
