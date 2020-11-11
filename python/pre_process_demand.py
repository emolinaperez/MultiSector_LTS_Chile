'''
Centro de Energia, Facultad de Ciencias Fisicas y Matematicas, U.de Chile
Octubre 2020
Rutina para preprocesar demanda electrica y crear datos de entrada de modelo PMR
'''

import os, os.path
import numpy as np
from time import time
import pandas as pd
import math as m

time_ini_1 = time()

##############################COMIENZO########################################

# Se extraen las direcciones de las distintas carpetas de la implementacion
dir_main = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
dir_gams = os.path.join(dir_main, "gams")
dir_out = os.path.join(dir_main, "out")
dir_pmr_model = os.path.join(dir_gams, "pmr")
dir_data_input = os.path.join(dir_pmr_model, "data_input")

# Se extraen las direcciones de los distintos archivos CSV a utilizar
dir_data_duration = os.path.join(dir_data_input, "data_duracion.csv")
dir_distribution_by_bloq = os.path.join(dir_data_input, "data_dem_distr_total_bloque.csv")
dir_shared_by_bus = os.path.join(dir_data_input, "data_dem_distr_total_barra.csv")
dir_demand = os.path.join(dir_out, "electric_demand_sectors.csv")

# Archivo a contener las salidas del pre-procesamiento
dir_out = os.path.join(dir_data_input,"data_demanda_electrica_escenarios.csv")

# Se leen los archivos CSV y se guardan como dataframes
df_duration = pd.read_csv(dir_data_duration)
df_distr_bloq = pd.read_csv(dir_distribution_by_bloq)
df_distr_bus = pd.read_csv(dir_shared_by_bus)
df_demand = pd.read_csv(dir_demand)

# Se define como parametro la cantidad de annos
years = 36
# Se extraen los nombres de las barras
bus_1 = df_distr_bus.iloc[0][0]
bus_2 = df_distr_bus.iloc[1][0]
# Se extraen los escenarios existentes en un arreglo numpy borrando las filas 
# repetidas
scenarios = np.array(df_demand['master_id'])
scenarios = np.unique(scenarios)

# Se crea la columna de suma total de la demanda.
np_total = np.ones(len(df_demand['master_id']))
for i in np.arange(0,len(np_total)):
    np_total[i] = df_demand.iloc[i,np.arange(2,16)].sum()
df_demand['Total'] = np_total

#np_year_bus = np.array(df_distr_bus['Agno'])
#first_scen = df_demand['master_id'].min()
#last_scen = df_demand['master_id'].max()
df_master_id = df_demand[['master_id', 'year']].copy()

# Se renombra la columna del año
df_master_id = df_master_id.rename(columns={'year':'Year'})

# Se filtra el dataframe que contiene los porcentajes de distribucion de la
# demanda entre las barras en un dataframe por barra
df_distr_bus_1 = df_distr_bus[df_distr_bus['Bus'] == 
                              bus_1].reset_index(drop=True)
df_distr_bus_2 = df_distr_bus[df_distr_bus['Bus'] ==
                              bus_2].reset_index(drop=True)

# Se multiplican el dataframe de cada barra para que tenga la misma cantidad
# de datos que la demanda a la salida de experimental_design
df_distr_bus_1_scen = pd.concat([df_distr_bus_1]*(m.floor(len(
    df_demand)/years)), ignore_index=True)
df_distr_bus_2_scen = pd.concat([df_distr_bus_2]*(m.floor(len(
    df_demand)/years)), ignore_index=True)

# Se construye el dataframe con las demandas distribuidas por barras
df_demand_by_bus = df_master_id

# Se multiplican las columnas de la demanda total con la columna del dataframe
# con los porcentajes por barras y se colocan en la columna del dataframme
# que contiene la demanda separada por barras 
df_demand_by_bus[bus_1] = df_demand['Total'] * df_distr_bus_1_scen[
    'Shared_by_bus']
df_demand_by_bus[bus_2] = df_demand['Total'] * df_distr_bus_2_scen[
    'Shared_by_bus']

##############################################################################
# Se procesara el dataframe df_distr_bloq para que contenga la duracion de los
# bloques (contenidos en data_duration) en otra columna
df_duration = df_duration.rename(columns = {'Agno':'Year'})
df_distr_bloq_int = df_distr_bloq.merge(
    df_duration, on=['Year', 'Etapa', 'Bloque'], how='left')
df_distr_bloq = df_distr_bloq_int
##############################################################################

# Ahora se multiplica la cantidad de datos en df_distr_bloq de tal forma que
# coincida con la cantidad de escenarios
for i in scenarios:
    # Se crea una copia para ir iterando sobre ella
    df_distr_bloq_scen_i = df_distr_bloq.copy()
    # Se crea una columna que contendra en numero de escenario al que
    # corresponden los desultados
    df_distr_bloq_scen_i.insert(0,'master_id',i)
    if i==0:
        df_distr_bloq_scen = df_distr_bloq_scen_i
    else:
        df_distr_bloq_scen = pd.concat([df_distr_bloq_scen, 
                                        df_distr_bloq_scen_i])

# Se filtran los datos en funcion de las barras para poder buscarlas en forma
# especifica en el otro dataframe
df_filt_bloq_SIC = df_distr_bloq_scen[df_distr_bloq_scen['Bus']=='SEN_SIC']
df_filt_bloq_SING = df_distr_bloq_scen[df_distr_bloq_scen['Bus']=='SEN_SING']

# Se mezclan los dataframes n funcion del master_id y el Year tanto para los
# datos filtrados del SIC y el SING
df_distr_bloq_scen_SIC = df_filt_bloq_SIC.merge(
    df_demand_by_bus[['master_id', 'Year', 'SEN_SIC']], 
    on=['master_id', 'Year'], how='left')
# Se renombra la columna del SIC para poder concatenarse con los datos del SING
df_data_demanda_1 = df_distr_bloq_scen_SIC.rename(
    columns={'SEN_SIC':'Demanda_Barra_Año'})
                       
df_distr_bloq_scen_SING = df_filt_bloq_SING.merge(
    df_demand_by_bus[['master_id', 'Year', 'SEN_SING']], 
    on=['master_id', 'Year'], how='left')
df_data_demanda_2 = df_distr_bloq_scen_SING.rename(
    columns={'SEN_SING':'Demanda_Barra_Año'})

# Se unen los datos de las demandas para construir un solo dataframe
df_data_demanda = pd.concat([df_data_demanda_1, df_data_demanda_2])

# Se obtienen las columnas que son la multiplicacion de otras columnas
df_data_demanda['Demanda_Barra_Año_Etapa'] = df_data_demanda[
    'Distribucion_Etapa'] * df_data_demanda['Demanda_Barra_Año']

df_data_demanda['Demanda_Barra_Año_Etapa_Bloque'] = df_data_demanda[
    'Distribucion_Bloque'] * df_data_demanda['Demanda_Barra_Año_Etapa']

df_data_demanda['Potencia_Bloque'] = (df_data_demanda[
    'Demanda_Barra_Año_Etapa_Bloque']*1000)/df_data_demanda['Duracion']

# Se renombran las salidas para hacerlas de un cierto formato
out = df_data_demanda[['master_id', 'Bus','Year', 'Etapa', 
                       'Bloque', 'Potencia_Bloque']] 
out = out.rename(columns={'master_id':'Escenario', 'Bus':'Barra', 
                              'Year':'Agno', 'Potencia_Bloque':'Demanda'})

out.to_csv(dir_out, index=False)

##############################FINAL###########################################

time_ini_2 = time()
time_scenarios = time_ini_2 - time_ini_1
time_horas = m.floor(time_scenarios/3600)
time_minutos = m.floor((time_scenarios%3600)/60)
time_segundos = m.floor((time_scenarios%3600)%60)
print(" ")
print("Tiempo de ejecucion de todos los Escenarios:", time_horas , 
      "horas", time_minutos,
      "minutos", time_segundos, "segundos")
