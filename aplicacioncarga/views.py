from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ConsumirServicioForm

import urllib.request
import concurrent.futures
import urllib.parse
from openpyxl import Workbook
import threading
import os

urls_parametros = [{
        'url': 'https://serviciosdigitalesdev.uexternado.edu.co/estudianteservicios/webresources/servicios/getMateriasProp',
        'params': {
            'objid': '0720938'
        }
    }
]

num_hilos_simultaneos = 10
# Create your views here.
def index(request):
    return render(request, 'index.html')

def consumirServicio(request):
    if request.method == 'GET':
        return render(request, 'consumirServicio/index.html', {
            'form': ConsumirServicioForm()
        })
    else:
        print(f"URL: {urls_parametros}")
        print(f"Cantidad de hilos: {num_hilos_simultaneos}")
        
        ejecutar_concurrente(num_hilos_simultaneos )
        return redirect('resultadoServicio')

def resultadoServicio(request):
    return render(request, 'consumirServicio/resultadoServicio.html')  

def hacer_solicitud(url, params, numero_peticion, resultados, lock):
    try:
        url_con_parametros = url + '?' + urllib.parse.urlencode(params)
        print(f"Se ejecutará la petición {numero_peticion} a {url_con_parametros}")
        with urllib.request.urlopen(url_con_parametros, timeout=10) as response:  # Aumento del tiempo de espera a 10 segundos
            estado = response.status
            resultados.append((numero_peticion, url_con_parametros, estado))
            print(f"Peticion {numero_peticion}: Solicitud a {url_con_parametros} - Estado: {estado}")

            # Bloqueo para escribir en el archivo Excel de manera segura
            with lock:
                wb = Workbook()
                ruta= os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reporte_solicitudes.xlsx')
                print(ruta)
                sheet = wb.active
                for resultado in resultados:
                    sheet.append(resultado)
            
            
                wb.save("reporte_solicitudes.xlsx")

    except urllib.error.URLError as e:
        estado = f"Error al hacer la solicitud {numero_peticion}: {e.reason}"
        resultados.append((numero_peticion, url_con_parametros, estado))
        print(f"Error al hacer la solicitud {numero_peticion} a {url_con_parametros}: {e.reason}")
    except Exception as e:
        estado = f"Error al hacer la solicitud {numero_peticion}: {str(e)}"
        resultados.append((numero_peticion, url_con_parametros, estado))
        print(f"Error al hacer la solicitud {numero_peticion} a {url_con_parametros}: {str(e)}")

resultados = []
lock = threading.Lock()

def ejecutar_concurrente( num_hilos_simultaneos):
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_hilos_simultaneos) as executor:
        numero_peticion = 1
        for servicio in urls_parametros:
            for _ in range(num_hilos_simultaneos):
                executor.submit(hacer_solicitud, servicio['url'], servicio['params'], numero_peticion, resultados, lock)
                numero_peticion += 1