from django.shortcuts import render
import pandas as pd
import json

def home(request):
    # Carga el archivo CSV
    file_path = 'jobs/vacantes.csv'
    df = pd.read_csv(file_path)

    # Convierte los datos en un diccionario con Job Id como clave y Job Title como valor
    job_data = df.set_index('Job Id')['Job Title'].to_dict()

    # Convierte el diccionario en JSON seguro para JavaScript
    job_data_json = json.dumps(job_data)

    # Pasa el diccionario serializado al contexto
    return render(request, 'vacantes/home.html', {'job_data': job_data_json})
