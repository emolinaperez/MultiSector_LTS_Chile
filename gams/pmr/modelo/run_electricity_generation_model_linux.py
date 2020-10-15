'''
Centro de Energia, Facultad de Ciencias Fisicas y Matematicas, U.de Chile
Septiembre 2020
Modelo PMR
'''

import subprocess

def main():
    print('Ejecutando MODELO PMR')
    subprocess.call(["gams","modelo_energetico_PMR_20200916.gms"])
    subprocess.call(["python3","Procesamiento_Salidas_PMR.py"])
if __name__ == '__main__':
     main()
