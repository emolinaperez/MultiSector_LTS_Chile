import os, os.path
import numpy as np
from time import time
import pandas as pd
import math as m

time_ini_1 = time()
# Se extraen las direccines de los archivos que ejectan el modelo de 
# generacion electrica a traves de GAMS
dr_modelo = os.path.dirname(os.path.realpath(__file__))
dr_pmr_model = os.path.dirname(dr_modelo)
dr_gams = os.path.dirname(dr_pmr_model)
dr_main = os.path.dirname(dr_gams)
dr_python = os.path.join(dr_main, "python")
dr_ed = os.path.join(dr_main, "experimental_design")
dr_data_input = os.path.join(dr_pmr_model, "data_input")
dr_data_output = os.path.join(dr_pmr_model, "data_output")

# Se importa la direccion de la carpeta experimental_design que contiene
# el CSV con los datos de resultados, esto mediante el comando dir_ed
# Se extrae el nombre de la ruta del archivo que contiene los resultados
results_ed = os.path.join(dr_ed, "experimental_design_multi_sector.csv")

###############################################################################
# Para editar los nombres de los archivos CSV de entrada y salida de GAMS
# se debe modiciar el nombre en esta seccion

# Datos de entrada al GAMS
# Archivo a contener los precios de los energeticos
dr_in_gams_energ = os.path.join(dr_data_input,
                                "data_precio_energeticos_escenarios.csv")
# Archivo a contener los costos de inversion de las tecnologias
dr_in_gams_inv = os.path.join(dr_data_input,
                              "data_costo_inversion_procesos_escenarios.csv")
# Archivo a contener la seleccion el csv que le dira a gams que escenario correr
dr_data_set_scen = os.path.join(dr_data_input,
                                "data_set_escenario_sel.csv")
# Achivo con la salida importate de GAMS
dr_data_out_gams = os.path.join(dr_data_output,
                                "solution_generation_sector.csv")
# Archivo a contener las salidas de las multples corridas de gams
dr_data_out_scen = os.path.join(dr_data_output,
                                "solution_generation_sector_scenarios.csv")
##############################################################################

# Se extrae en el dataframe los datos que se encuentran en el CSV.
df_scenarios = pd.read_csv(results_ed)

master_id = 'master_id'
year = 'year'
# Definicion de nombres para extraer los datos del experimental design
# Definicion de los precios de los energeticos
price_coal = 'fuel_price_coal'
price_gas = 'fuel_price_natural_gas'
price_diesel = 'fuel_price_diesel'
price_oil = 'fuel_price_fuel_oil'
# Definicion de los costos ded inversion
inv_cost_pv_solar = 'investment_cost_pv_solar'
inv_cost_csp_solar = 'investment_cost_csp_solar'
inv_cost_wind = 'investment_cost_wind'
inv_cost_geot = 'investment_cost_geothermal'
inv_cost_gas = 'investment_cost_natural_gas_cc'

##############################################################################
##############################################################################
# AQUI DEFINIR LOS NOMBRES DE LAS ENTRADAS DE GAMS

# Definicion de nombres para imprimir los datos del gams
# Definicion de los precios de los energeticos
price_coal_gams = 'carbon_generacion'
price_gas_gams = 'gas_natural_generacion'
price_diesel_gams = 'diesel_generacion'
price_oil_gams = 'fuel_oil'
# Definicion de los costos ded inversion
inv_cost_pv_solar_gams = 'generacion_solar_fv'
inv_cost_csp_solar_gams = 'generacion_solar_csp'
inv_cost_wind_gams = 'generacion_eolica'
inv_cost_geot_gams = 'generacion_geotermia'
inv_cost_gas_gams = 'generacion_gas_natural_cc'
##############################################################################
##############################################################################

# Se extraen las columnas del dataframe
df_master_id = df_scenarios[master_id].copy()
df_year = df_scenarios[year].copy()
# Se extraen las columnas con precios
df_price_coal = df_scenarios[price_coal].copy()
df_price_gas = df_scenarios[price_gas].copy()
df_price_diesel = df_scenarios[price_diesel].copy()
df_price_oil = df_scenarios[price_oil].copy()
# Se crean columnas de categoria de energetico para cada dataframe
df_cat_coal = pd.DataFrame([price_coal_gams for i in np.arange(len(df_year))])
df_cat_gas = pd.DataFrame([price_gas_gams for i in np.arange(len(df_year))])
df_cat_diesel = pd.DataFrame([price_diesel_gams for i in np.arange(len(df_year))])
df_cat_oil = pd.DataFrame([price_oil_gams for i in np.arange(len(df_year))])
# Se extraen las columnas con los costos de inversion
df_inv_cost_pv_solar = df_scenarios[inv_cost_pv_solar].copy()
df_inv_cost_csp_solar = df_scenarios[inv_cost_csp_solar].copy()
df_inv_cost_wind = df_scenarios[inv_cost_wind].copy()
df_inv_cost_geot = df_scenarios[inv_cost_geot].copy()
df_inv_cost_gas = df_scenarios[inv_cost_gas].copy()
# Se crean columnas de categoria de inversion para cada dataframe
df_cat_pv_solar = pd.DataFrame([inv_cost_pv_solar_gams
                                for i in np.arange(len(df_year))])
df_cat_csp_solar = pd.DataFrame([inv_cost_csp_solar_gams
                                 for i in np.arange(len(df_year))])
df_cat_wind = pd.DataFrame([inv_cost_wind_gams
                            for i in np.arange(len(df_year))])
df_cat_geot = pd.DataFrame([inv_cost_geot_gams
                            for i in np.arange(len(df_year))])
df_cat_gnl = pd.DataFrame([inv_cost_gas_gams
                           for i in np.arange(len(df_year))])

# Une los Dataframes de precios y luego de costos utilizando diccionarios
# Primeramente se crea la forma del archivo de energeticos que recibe gams
df_data_price_coal = pd.DataFrame({'Escenario':df_master_id, 'Agno':df_year,
                        'Energeticos':df_cat_coal[0], 'Precio':df_price_coal})
df_data_price_gas = pd.DataFrame({'Escenario':df_master_id, 'Agno':df_year,
                        'Energeticos':df_cat_gas[0], 'Precio':df_price_gas})
df_data_price_diesel = pd.DataFrame({'Escenario':df_master_id, 'Agno':df_year,
                        'Energeticos':df_cat_diesel[0], 
                        'Precio':df_price_diesel})
df_data_price_oil = pd.DataFrame({'Escenario':df_master_id, 'Agno':df_year,
                        'Energeticos':df_cat_oil[0], 'Precio':df_price_oil})
# Luego se concatenan los dataframes
df_data_price = pd.concat([df_data_price_coal, df_data_price_gas,
                           df_data_price_diesel, df_data_price_oil])
# Primeramente se crea la forma del archivo de energetics que recibe gams
df_data_inv_pv_solar = pd.DataFrame({'Escenario':df_master_id, 'Agno':df_year,
                        'Energeticos':df_cat_pv_solar[0], 
                        'Precio':df_inv_cost_pv_solar})
df_data_inv_csp_solar = pd.DataFrame({'Escenario':df_master_id, 'Agno':df_year,
                        'Energeticos':df_cat_csp_solar[0], 
                        'Precio':df_inv_cost_csp_solar})
df_data_inv_wind = pd.DataFrame({'Escenario':df_master_id, 'Agno':df_year,
                        'Energeticos':df_cat_wind[0], 
                        'Precio':df_inv_cost_wind})
df_data_inv_geot = pd.DataFrame({'Escenario':df_master_id, 'Agno':df_year,
                        'Energeticos':df_cat_geot[0], 
                        'Precio':df_inv_cost_geot})
df_data_inv_gas = pd.DataFrame({'Escenario':df_master_id, 'Agno':df_year,
                        'Energeticos':df_cat_gnl[0], 
                        'Precio':df_inv_cost_gas})
# Luego se concatenan los dataframes
df_data_inv = pd.concat([df_data_inv_pv_solar, df_data_inv_csp_solar,
                         df_data_inv_wind, df_data_inv_geot, 
                         df_data_inv_gas])

# Los dataframes recien creado se exportan a los archivos CSV en la carpeta
# que contiene los archivos de input de GAMS
df_data_inv.to_csv(dr_in_gams_inv, index=False)
df_data_price.to_csv(dr_in_gams_energ, index=False)

# Se extraen los numeros de los escenarios presentes en los resultados
first_scen = df_master_id.min()
last_scen = df_master_id.max()



##############################################################################
# Se comienza a desarrollar las iteraciones por escenarios
for i in np.arange(first_scen, last_scen+1):
#for i in np.arange(first_scen, 3+1):
    # Primeramente se crea el dataframe que le dira al GAMS que escenario 
    # seleccionar
    data_set_scen = pd.DataFrame(['Escenario_Seleccionado',i])
    data_set_scen.to_csv(dr_data_set_scen, index=False, header=False)
    
    print('Ejecutando Escenario ', i)
    
    # Con la seleccion de escenario lista se procede a ejecutar el archivo 
    # de GAMS
    time_1 = time()
    print('  Ejecutando GAMS del Escenario ', i)
    
    import run_electricity_generation_model_win
    run_electricity_generation_model_win.main()
     
    time_2 = time()
    time_gams = time_2 - time_1
    time_horas = m.floor(time_gams/3600)
    time_minutos = m.floor((time_gams%3600)/60)
    time_segundos = m.floor((time_gams%3600)%60)
    print("  Tiempo de ejecucion Modelo PMR GAMS:", time_horas ,
          "horas", time_minutos, "minutos", time_segundos, "segundos")
    
    # Se lee la salida que entrega el GAMS al correr
    data_out_gams_i = pd.read_csv(dr_data_out_gams)
    
    # Se crea una columna que contendra en numero de escenario al que
    # corresponden los desultados
    data_out_gams_i.insert(0,'Escenario',i)
    # Despues de Ejecutar el programa se almacenan los resultados, dependiendo
    # de si se encuentra la primera iteracion, se conservan los header y sino
    # se importan los resultados sin el header con la funcion concat().
    if i==0:
        data_out_gams = data_out_gams_i
    else:
        data_out_gams = pd.concat([data_out_gams, data_out_gams_i])

# El fataframe a la salida del bucle contendra todos lo resultados de la
# ruina que ejecuto gams enumerados segun el escenario
data_out_gams.to_csv(dr_data_out_scen, index=False)

time_ini_2 = time()
time_scenarios = time_ini_2 - time_ini_1
time_horas = m.floor(time_scenarios/3600)
time_minutos = m.floor((time_scenarios%3600)/60)
time_segundos = m.floor((time_scenarios%3600)%60)
print(" ")
print("Tiempo de ejecucion de todos los Escenarios:", time_horas , 
      "horas", time_minutos,
      "minutos", time_segundos, "segundos")