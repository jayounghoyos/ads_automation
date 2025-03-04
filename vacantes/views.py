from django.http import JsonResponse
from django.shortcuts import render
import pandas as pd
import json
import sys
import subprocess

def home(request):
    # Cargar el archivo CSV
    file_path = 'jobs/vacantes.csv'
    df = pd.read_csv(file_path, dtype={'Job Id': str})  # Asegurarse de que los IDs sean cadenas de texto

    # Convertir los datos en un diccionario con Job Id como clave y Job Title como valor
    job_data = df.set_index('Job Id')['Job Title'].to_dict()

    # Serializar el diccionario a JSON de manera segura
    job_data_json = json.dumps(job_data, ensure_ascii=False)

    # Pasar el diccionario al contexto
    return render(request, 'vacantes/home.html', {'job_data': job_data_json})

def publicar_vacantes(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            vacancies = data.get('vacancies', [])
            print("Datos recibidos en publicar_vacantes:", vacancies)

            # Ejecutar el script de automatización con el intérprete de Python del entorno virtual
            ids = [vacante['id'] for vacante in vacancies]
            result = subprocess.run([sys.executable, 'src/main.py'] + ids, capture_output=True, text=True)
            
            print("Resultado del script:", result.stdout)
            print("Errores del script:", result.stderr)

            if result.returncode == 0:
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': result.stderr})
        
        except Exception as e:
            print("Error en publicar_vacantes:", str(e))
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})
