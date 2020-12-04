import os, os.path
import numpy as np
import time
import pandas as pd
import math
import setup_runs as sr

time_ini_1 = time.time()

#read master id attribute and masters to run
df_attribute_master = pd.read_csv(sr.fp_csv_attribute_master)
df_masters_to_run = pd.read_csv(sr.fp_csv_experimental_design_msec_masters_to_run_gams)

#list of all masters
all_masters = list(df_attribute_master["master_id"])
#list of all master ids to run
all_masters_run = list(df_masters_to_run["master_id"])
all_masters_run.sort()


##############################################################################
# Se comienza a desarrollar las iteraciones por escenarios

#initialize the grouped dataframe?
init_df_out = True
#set dictionary for renaming columns
dict_rename = {
	"agno": "year",
	"emission": (sr.dict_sector_to_abv["electricity"] + "-emissions_total-mtco2e"),
	"CAPEX": (sr.dict_sector_to_abv["electricity"] + "-costs_total_capex-UNITSHERE"),
	"OPEX": (sr.dict_sector_to_abv["electricity"] + "-costs_total_opex-UNITSHERE")
}

#get hydrology info
df_ed_hyd = pd.read_csv(sr.fp_csv_gams_data_hidrologias_escenarios)
#convert to dictionary
dict_ed_hyd = sr.build_dict(df_ed_hyd[["Escenario", "Escenario_Hidrologico"]])

for m in all_masters_run:
	#get index
	i = all_masters.index(m)
	
	##  export scenario information for gams

	# scenario to run (for investment/price)
	data_set_scen = pd.DataFrame([[m]], columns = ["Escenario"])
	data_set_scen.to_csv(sr.fp_csv_gams_data_set_scen, index = False, header = True, encoding = "UTF-8")
	
	# hydrology to run
	hydro_id = int(dict_ed_hyd[m])
	data_set_hydro_id = pd.DataFrame([[hydro_id]], columns = ["ID_Hidro"])
	data_set_hydro_id.to_csv(sr.fp_csv_gams_data_hidrologias_simulacion, index = False, header = True, encoding = "UTF-8")
	
	
	print("\n" + "#"*30 + "\n###\n###    EMPEZANDO master_id " + str(m) + "\n###\n" + "#"*30 + "\n")
	# Con la seleccion de escenario lista se procede a ejecutar el archivo de GAMS
	time_1 = time.time()

	#remove existing solution so that next iteration can run
	if os.path.exists(sr.fp_csv_gams_solution_generation_sector):
		os.remove(sr.fp_csv_gams_solution_generation_sector)
	#remove the gdx for setting the scenario
	fp_gdx_rmv = sr.fp_csv_gams_data_set_scen.replace(".csv", ".gdx")
	if os.path.exists(fp_gdx_rmv):
		os.remove(fp_gdx_rmv)
		
	#set command
	cmd_gams = "gams " + sr.fp_gams_modelo
	#execute
	os.system(cmd_gams)
	
	time.sleep(1)
	 
	time_2 = time.time()
	time_gams = time_2 - time_1
	time_horas = math.floor(time_gams/3600)
	time_minutos = math.floor((time_gams%3600)/60)
	time_segundos = math.floor((time_gams%3600)%60)
	print("  Tiempo de ejecucion Modelo PMR GAMS:", time_horas ,
		  "horas", time_minutos, "minutos", time_segundos, "segundos")
	
	# Se lee la salida que entrega el GAMS al correr
	data_out_gams_i = pd.read_csv(sr.fp_csv_gams_solution_generation_sector)
	data_out_gams_i = data_out_gams_i.rename(columns = dict_rename)
	fields_ord_i = list(data_out_gams_i.columns)
	# Se crea una columna que contendra en numero de escenario al quecorresponden los desultados
	data_out_gams_i["master_id"] = [m for x in range(len(data_out_gams_i))]
	
	data_out_gams_i = data_out_gams_i[["master_id"] + fields_ord_i]
	# Despues de Ejecutar el programa se almacenan los resultados, dependiendo de si se encuentra la primera iteracion, se conservan los header y sino se importan los resultados sin el header con la funcion concat().
	if init_df_out:
		#set header
		fields_ord = list(data_out_gams_i.columns)
		#write output
		data_out_gams_i.to_csv(sr.fp_csv_output_multi_sector_pmr, index = None, encoding = "UTF-8")
		#turn off
		init_df_out = False
	else:
		#order appropriately and append to output file
		data_out_gams_i = data_out_gams_i[fields_ord]
		data_out_gams_i.to_csv(sr.fp_csv_output_multi_sector_pmr, mode = "a", header = False, index = False, encoding = "UTF-8")

	print("\n" + "#"*30 + "\n###\n###    SE TERMINE master_id " + str(m) + "\n###\n" + "#"*30 + "\n")

time_ini_2 = time.time()
time_scenarios = time_ini_2 - time_ini_1
time_horas = math.floor(time_scenarios/3600)
time_minutos = math.floor((time_scenarios%3600)/60)
time_segundos = math.floor((time_scenarios%3600)%60)
print(" ")
print("Tiempo de ejecucion de todos los Escenarios:", time_horas ,
	  "horas", time_minutos,
	  "minutos", time_segundos, "segundos")
	  
