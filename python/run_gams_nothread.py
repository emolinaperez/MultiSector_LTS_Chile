import os, os.path
import numpy as np
import time
import pandas as pd
import math
import setup_runs as sr
import multiprocessing as mp

time_ini_1 = time.time()

#read master id attribute and masters to run
df_attribute_master = pd.read_csv(sr.fp_csv_attribute_master)
df_masters_to_run = pd.read_csv(sr.fp_csv_experimental_design_msec_masters_to_run_gams)

#list of all masters
all_masters = list(df_attribute_master["master_id"])
#list of all master ids to run
all_masters_run = list(df_masters_to_run["master_id"])
#all_masters_run.sort()


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




if sr.parallel_exec_gams_q:


	###   RUN PARALLEL SMP
	
	#########################################
	###                                   ###
	###    BUILD PARALLELIZATION FILES    ###
	###                                   ###
	#########################################

	#read in games file
	f_gams = open(sr.fp_gams_modelo, "r")
	str_list_gams = f_gams.readlines()


	##  get data frames

	#get lines to remove
	df_rm_lines = pd.read_csv(sr.fp_csv_gams_parallel_support_lines_to_remove)
	#string replacements
	df_par_sreps = pd.read_csv(sr.fp_csv_gams_parallel_support_string_replacements)
	#get hydrology ids by master id
	df_hidro = pd.read_csv(sr.fp_csv_gams_data_hidrologias_escenarios)


	##  build dictionaries

	#dictionary to map line numbers to strings to replace
	dict_par_sreps = sr.build_dict(df_par_sreps[["line_num", "string_replace"]])
	#dictionary to map master ids to hydrology id
	dict_master_to_hidro = sr.build_dict(df_hidro[["Escenario", "Escenario_Hidrologico"]])


	##  1. REPLACE LINES SPECIFIED

	print("\n(1) Replacing lines in " + sr.fp_gams_modelo + " for template to enable parallelization...\n")
	for l in dict_par_sreps.keys():
		if l < len(str_list_gams):
			#set the string to insert
			str_insert = str(dict_par_sreps[l])
			#check for appendage
			if dict_par_sreps[l][-2:] != "\n":
				str_appendage = "\n"
			else:
				str_appendage = ""
				
			#update list
			str_list_gams[int(l) - 1] = str_insert + str_appendage
			
			
	##  2. REMOVE LINES

	print("(2) Removing unneeded lines in gams template...\n")
	#initialize the set of lines to
	set_rm_lines = []

	# (a) loop over indexing csv to remove lines
	vec_lines = df_rm_lines["line_comment_0"]
	#loop over indexing csv
	for i in range(len(df_rm_lines)):
		str_lines = str(df_rm_lines["line_comment_0"].iloc[i])
		
		if str_lines.isnumeric():
			rml = [int(str_lines) - 1]
		else:
			#assume it's a range
			rml = str_lines.split("-")
			#initialize ranging
			rml_tmp = []
			#check for numeric
			for k in range(len(rml)):
				if rml[k].isnumeric():
					rml_tmp.append(int(rml[k]))
			#set range
			rml = list(range(min(rml_tmp) - 1, max(rml_tmp)))
		
		#update
		set_rm_lines = set_rm_lines + rml
	#convert to set
	set_rm_lines = set(set_rm_lines)
	

	# (b) loop over all lines to remove calls to csv2gdx
	str_flag_drop = "$call csv2gdx"
	#new file to run in gams as a preprocessor (not in parallel)
	new_file_calls = []

	for i in range(len(str_list_gams)):
		#the line
		str_line = str(str_list_gams[i])
		#is the flag there?
		if str_line[0:min(len(str_flag_drop), len(str_line))] == str_flag_drop:
			#add to the new file
			new_file_calls.append(str_line)
			#and add to the set of lines to drop
			set_rm_lines = set_rm_lines | set({i})
			
	#write output to new gams
	f_gdx = open(sr.fp_gams_pmr_prerun_gdx_build, "w")
	f_gdx.writelines(new_file_calls)
	f_gdx.close()

	#get lines to keep
	set_kp_lines = list(set(range(len(str_list_gams))) - set_rm_lines)
	set_kp_lines.sort()
	#reduce gams template
	str_list_gams = [str_list_gams[i] for i in set_kp_lines]


	##  3. INDEX LINES THAT CONTAIN ID REPLACEMENT STRINGS

	print("(3) Indexing lines with strings to replace...\n")
	#initialize dictionary of indicies for lines that have ids
	dict_ind_lines_repl_vars = {"hydro_id": [], "master_id": [], "fp_output": []}

	for i in range(len(str_list_gams)):
		#the line
		str_line = str(str_list_gams[i])
		#then, check if it needs to be indexed
		for id_type in dict_ind_lines_repl_vars.keys():
			str_check = "##" + id_type + "##"
			if str_check in str_line:
				print(i)
				tmp_vec = dict_ind_lines_repl_vars[id_type]
				#update the list in the dictionary
				dict_ind_lines_repl_vars.update({id_type: tmp_vec + [int(i)]})


	##  4. BUILD FUNCTION TO EXECUTE ON EACH NODE

	print("\n(4) Constructing function to execute on each core...\n")
	#set dictionary for renaming columns
	dict_rename = {
		"agno": "year",
		"emission": (sr.dict_sector_to_abv["electricity"] + "-emissions_total-mtco2e"),
		"CAPEX": (sr.dict_sector_to_abv["electricity"] + "-costs_total_capex-UNITSHERE"),
		"OPEX": (sr.dict_sector_to_abv["electricity"] + "-costs_total_opex-UNITSHERE")
	}
	
	#set initial time
	t0 = time.time()
	#define the function to run on each core
	def run_gams(m_id, dict_line_repls = dict_ind_lines_repl_vars, fp_gams = sr.fp_exec_gams):
		
		#local path on OS X: fp_gams = "/Applications/GAMS30.3/GAMS Terminal.app/Contents/MacOS/gams"
		
		print("\nRunning:\n\tmaster_id:\t" + str(m_id) + "\n\tprocess id:\t" + str(os.getpid()) + "\n\n")
		#get template to work withand write
		tmp = str_list_gams.copy()
		#set filename for output from gams
		fp_out_gams = sr.fp_csv_gams_solution_generation_sector.replace(".csv", ("-" + str(m_id) + ".csv"))
		
		#set dictionary of ids
		dict_vars = {
			"master_id": int(m_id),
			"hydro_id": int(dict_master_to_hidro[int(m_id)]),
			"fp_output": fp_out_gams
		}

		# replace ids with integer values
		for id_type in dict_line_repls.keys():
			if id_type in dict_vars.keys():
				#get lines
				for k in dict_line_repls[id_type]:
					str_rep = "##" + id_type + "##"
					#update template with real id
					tmp[k] = tmp[k].replace(str_rep, str(dict_vars[id_type]))
		
		# write to output
		fp_out = os.path.join(sr.dir_gams_modelo, "pmr_model-" + str(m_id) + ".gms")
		#set writer
		f = open(fp_out, "w")
		f.writelines(tmp)
		f.close()
		
		
		# execute command
		cmd = "\"" + fp_gams + "\" \"" + fp_out + "\" o=/dev/null lo=1 lf=/dev/null"
		#cmd = "echo test"
		#execute
		rv = os.system(cmd)
		
		print("PMR complete for master_id = " + str(m_id) + ". Reading output...")
		#read output
		if os.path.exists(sr.fp_csv_gams_solution_generation_sector):
			#get results
			df_results = pd.read_csv(sr.fp_csv_gams_solution_generation_sector)
			#ordered fields
			fields_ord = list(df_results.columns)
			#add master id
			df_results["master_id"] = [m_id for i in range(len(df_results))]
			#reorder and rename
			df_results = df_results[["master_id"] + fields_ord].rename(columns = dict_rename)
			
			#get time and print output
			time_elapsed = round(time.time() - t0, 2)
			
			print("PMR run master_id = " + str(m_id) + " complete.\nTotal time elapsed (checkpoint 4): " + str(time_elapsed))
			
			#return output data
			return df_results
		else:
			return -99
			
	#define the function to run on each core (threading)
	def run_gams_thread(workspace, checkpoint, m_id_list, list_lock, io_lock, dict_line_repls = dict_ind_lines_repl_vars, fp_gams = sr.fp_exec_gams):
		
		#local path on OS X: fp_gams = "/Applications/GAMS30.3/GAMS Terminal.app/Contents/MacOS/gams"
		
		print("\nRunning:\n\tmaster_id:\t" + str(m_id) + "\n\tprocess id:\t" + str(os.getpid()) + "\n\n")
		#get template to work withand write
		tmp = str_list_gams.copy()
		#set filename for output from gams
		fp_out_gams = sr.fp_csv_gams_solution_generation_sector.replace(".csv", ("-" + str(m_id) + ".csv"))
		
		#set dictionary of ids
		dict_vars = {
			"master_id": int(m_id),
			"hydro_id": int(dict_master_to_hidro[int(m_id)]),
			"fp_output": fp_out_gams
		}

		# replace ids with integer values
		for id_type in dict_line_repls.keys():
			if id_type in dict_vars.keys():
				#get lines
				for k in dict_line_repls[id_type]:
					str_rep = "##" + id_type + "##"
					#update template with real id
					tmp[k] = tmp[k].replace(str_rep, str(dict_vars[id_type]))
		
		# write to output
		fp_out = os.path.join(sr.dir_gams_modelo, "pmr_model-" + str(m_id) + ".gms")
		#set writer
		f = open(fp_out, "w")
		f.writelines(tmp)
		f.close()
		
		
		# execute command
		cmd = "\"" + fp_gams + "\" \"" + fp_out + "\" o=/dev/null lo=1 lf=/dev/null"
		#cmd = "echo test"
		#execute
		rv = os.system(cmd)
		
		print("PMR complete for master_id = " + str(m_id) + ". Reading output...")
		#read output
		if os.path.exists(sr.fp_csv_gams_solution_generation_sector):
			#get results
			df_results = pd.read_csv(sr.fp_csv_gams_solution_generation_sector)
			#ordered fields
			fields_ord = list(df_results.columns)
			#add master id
			df_results["master_id"] = [m_id for i in range(len(df_results))]
			#reorder and rename
			df_results = df_results[["master_id"] + fields_ord].rename(columns = dict_rename)
			
			#get time and print output
			time_elapsed = round(time.time() - t0, 2)
			
			print("PMR run master_id = " + str(m_id) + " complete.\nTotal time elapsed (checkpoint 4): " + str(time_elapsed))
			
			#return output data
			return df_results
		else:
			return -99

		
	##  5. EXECUTE IN PARALLEL, COLLECT OUTPUT, AND WRITE OUTPUT


	#change the working directory to gams
	os.chdir(sr.dir_gams_modelo)
	#all_masters_run = list(range(16))
	iters = all_masters_run
	
	# execute prerun
	
	print("Building GDX files...")
	
	cmd = sr.fp_exec_gams + " \"" + sr.fp_gams_pmr_prerun_gdx_build + "\" o=/dev/null lo=1 lf=/dev/null"
	cm_gdx = os.system(cmd)
	
	print("GDX files complete.")
	
	
	print("\n"*2 + "#"*30 + "#"*3 + "###\tStarting parallel execution" + "#"*3 + "#"*30 + "\n"*2)
	
	if __name__ == "__main__":

		with mp.Pool(processes = os.cpu_count()) as pool:
			#k = pool.starmap(gams_test, iters)
			list_pool = pool.map(run_gams, iters)
		#set output and sort
		df_out = pd.concat(list_pool, axis = 0)
		df_out = df_out.sort_values(by = ["master_id"]).reset_index(drop = True)
		#write output
		df_out.to_csv(sr.fp_csv_output_multi_sector_pmr, index = None, encoding = "UTF-8")
			
else:

	###   RUN LINEARLY
	
	# read in the file
	f_gams = open(sr.fp_gams_modelo, "r")
	str_list_gams = f_gams.readlines()
	
	# (a) loop over all lines to remove calls to csv2gdx
	str_flag_drop = "$call csv2gdx"
	#new file to run in gams as a preprocessor (not in parallel)
	new_file_calls = []
	
	#initialize the set of lines to drop
	set_rm_lines = set({})
	#strings to ignore
	ignore_flags = ["data_set_escenario_sel.csv", "data_hidrologias_simulacion.csv"]
	
	for i in range(len(str_list_gams)):
		#the line
		str_line = str(str_list_gams[i])
		#is the flag there?
		if str_line[0:min(len(str_flag_drop), len(str_line))] == str_flag_drop:
			#default to dropping the gdx call
			proceed_q = True
			#check the flags to ignore
			for fl in ignore_flags:
				if fl in str_line:
					proceed_q = False
			
			if proceed_q:
				#add to the new file
				new_file_calls.append(str_line)
				#and add to the set of lines to drop
				set_rm_lines = set_rm_lines | set({i})
			
	#write output to new gams
	f_gdx = open(sr.fp_gams_pmr_prerun_gdx_build, "w")
	f_gdx.writelines(new_file_calls)
	f_gdx.close()

	#get lines to keep
	set_kp_lines = list(set(range(len(str_list_gams))) - set_rm_lines)
	set_kp_lines.sort()
	#reduce gams template
	str_list_gams = [str_list_gams[i] for i in set_kp_lines]
	
	#write cleaned files
	if os.path.exists(sr.fp_gams_modelo_nogdxcall):
		os.remove(sr.fp_gams_modelo_nogdxcall)
	#write to output
	f_gams_new = open(sr.fp_gams_modelo_nogdxcall, "w")
	f_gams_new.writelines(str_list_gams)
	f_gams_new.close()
	
	
	#run GDX build
	print("Building GDX files...")
	cmd = sr.fp_exec_gams + " \"" + sr.fp_gams_pmr_prerun_gdx_build + "\" o=/dev/null lo=1 lf=/dev/null"
	cm_gdx = os.system(cmd)
	print("GDX files complete.")
	
	#change working directory
	os.chdir(sr.dir_gams_modelo)
	
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
		cmd_gams = "gams " + sr.fp_gams_modelo_nogdxcall
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
	  
