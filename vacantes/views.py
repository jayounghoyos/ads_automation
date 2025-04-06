from django.http import JsonResponse
from django.shortcuts import render
import json
import sys
import subprocess
import os
from backend.database import SessionLocal
from backend.models import Vacante

def home(request):
    # Obtener vacantes desde la base de datos
    db = SessionLocal()
    vacantes = db.query(Vacante).all()
    db.close()

    # Crear diccionario {job_id: titulo}
    job_data = {str(v.job_id): v.titulo for v in vacantes}
    job_data_json = json.dumps(job_data, ensure_ascii=False)

    return render(request, 'vacantes/home.html', {'job_data': job_data_json})

def publicar_vacantes(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            vacancies = data.get('vacancies', [])
            print("Datos recibidos en publicar_vacantes:", vacancies)

            ids = [vacante['job_id'] for vacante in vacancies]

            result = subprocess.run(
                [sys.executable, 'src/main.py'] + ids,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )

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
