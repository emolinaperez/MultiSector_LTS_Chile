import os, os.path
import pandas as pd
import numpy as np
import sys

###################################
#    START WITH INITIALIZATION    #
###################################

##  UNIX SIDE

#set the working directory
dir_cur = os.path.dirname(os.path.realpath(__file__))
#master directory
dir_model = os.path.dirname(dir_cur)
#reference files
dir_ref = os.path.join(dir_model, "ref")


#archive
dir_archive_runs = os.path.join(dir_model, "archive_runs")
#basline modeling directory (previously baseline modeling)
dir_bm = os.path.join(dir_ref, "baseline_future_transportation_parameters")
#experimental design and attribute tables
dir_ed = os.path.join(dir_model, "experimental_design")
#gams files
dir_gams = os.path.join(dir_model, "gams", "pmr")
#gams subdirectories
dir_gams_input = os.path.join(dir_gams, "data_input")
dir_gams_modelo = os.path.join(dir_gams, "modelo")
dir_gams_output = os.path.join(dir_gams, "data_output")
#output
dir_out = os.path.join(dir_model, "out")




##  PARALLELS

plt = sys.platform
#determine if parallels needs to be used
if plt[0:min(len(plt), 3)] != "win":
	#set parallels VM directory
	dir_ade = "/Volumes/[C] syme-j-PVM.hidden/Users/jsyme/Documents/Projects/SWCHE076-1000/ade_beta"
	#set platform
	analytical_platform = "unix"
else:
	#use current directory
	dir_ade = dir_model
	#set platform
	analytical_platform = "windows"
#reference files
dir_ref_ade = os.path.join(dir_ade, "ref")
#output
dir_out_ade = os.path.join(dir_ade, "out")
#experimental design
dir_ed_ade = os.path.join(dir_ade, "experimental_design")



####################################
#    CHECK REQUIRED DIRECTORIES    #
####################################

if not os.path.exists(dir_ref):
    print("Warning: path to reference parameter files " + dir_ref + " not found. Check that the directory exists and all parameter files are present.")


##########################################
#    GET DICTIONARIES FOR ATTRIBUTES     #
##########################################

#get initialization files by
file_strat = os.path.join(dir_ref, "attribute_strategy.csv")
#get data frame
df_strat = pd.read_csv(file_strat)
df_strat = df_strat[df_strat["include"] == 1]
#initialize dictionary of strategies
dict_strat = {}
dict_strat_id_to_strat = {}
dict_strat_ids = {}
#get columns to inlude in dictionary
fields_incl = [x for x in df_strat.columns if (x not in ["strategy", "include"])]
#iterate over rows
for i in range(0, len(df_strat)):
	if int(df_strat["include"].iloc[i]) == 1:
		#set scenario name
		strat = str(df_strat["strategy"].iloc[i])
		strat_id = int(df_strat["strategy_id"].iloc[i])
		#initialize temporary dictionary
		dict_tmp = {}
		#loop
		for field in fields_incl:
			dict_tmp.update({field: df_strat[field].iloc[i]})
		dict_strat.update({strat: dict_tmp.copy()})
		#add only id
		dict_strat_ids.update({strat: strat_id})
        #add to reverse dictionary
		dict_strat_id_to_strat.update({strat_id: strat})
	



#############################################
#    GET INITIALIZATION FILE INFORMATION    #
#############################################

#get initialization files
fp_ini_session = os.path.join(dir_model, "initialize_session.ini")
#read in session initialization
if os.path.exists(fp_ini_session):
	#read in
	with open(fp_ini_session) as f:
		list_init_session = f.readlines()
else:
	list_init_session = []

#join
list_init = list_init_session
#remove unwanted blank characters
for char in ["\n", "\t"]:
	list_init = [l.replace(char, "") for l in list_init]
#remove instances of blank strings
list_init = list(filter(lambda x: (x != "") and ("#" in x) == False, list_init))
list_init = list(filter(lambda x: (x[0] != "["), list_init))
#split strings
dict_init = [l.split(":") for l in list_init]
#convert to dictionary
dict_init = dict(dict_init)
#convert numeric values
for key in dict_init.keys():
	if dict_init[key].isnumeric():
		num = float(dict_init[key])
		if num == int(num):
			dict_init[key] = int(num)
		else:
			dict_init[key] = num



########################
#    SOME VARIABLES    #
########################

#model years to save off
output_model_years = [int(x) for x in dict_init["model_years"].split(",")]
#dictionary
		


############################
#    ADD SOME FUNCTIONS    #
############################

#
def data_to_wide(df_in, field_wide_by, field_value, fields_index, clean_names_q = True):
	#get unique value
	unique_vals = list(set(df_in[field_wide_by]))
	#reduce data set
	df_in_wide = df_in[fields_index].copy()
	df_in_wide = df_in_wide.drop_duplicates()
	#fields to merge on
	fields_merge = fields_index
	#loop
	for val in unique_vals:
		df_tmp = df_in[df_in[field_wide_by] == val]
		#clean up the names?
		if clean_names_q:
			#get new name
			field_new = val.lower().replace(" ", "_")
		else:
			field_new = val
		#update column names
		df_tmp = df_tmp.rename(columns = {field_value: field_new})
		#reduce
		df_tmp = df_tmp[fields_index + [field_new]]
		#merge in
		df_in_wide = pd.merge(df_in_wide, df_tmp, how = "left", left_on = fields_merge, right_on = fields_merge)
	#return
	return df_in_wide
	
	
	
def sigmoid(x, m, b):
    return 1/(1 + np.e**(m - x/b))



#basic function for building dictionary
def build_dict(df_in):
	#output dictionary
	return dict([tuple(df_in.iloc[i]) for i in range(len(df_in))])


#
def build_mix_vec(m, b, w_sigm = 0.75, type = "sigmoid"):

    #number of years for mixing
	n_year = 32
	x = range(0, n_year + 1)
    
	if type == "sigmod":
		y = [w_sigm*sigmoid(i, m, b) + (1 - w_sigm)*i/n_year for i in x]
        #normalize to acheive 1 in 2050
		y = np.array(y)/max(y)
	elif type == "linear":
		y = [i/n_year for i in x]
		
    #update and return
	vec_mix = list([0 for i in range(35 - n_year)]) + list(y)

	return np.array(vec_mix)



#vector for mixing
def build_linear_mix_vec(tuple_year, tuple_year_range):

	#set years to start (at 0) and finish (at 1)
	y_0 = min(tuple_year)
	y_1 = max(tuple_year)
	
	#get length of all years in index
	n_years_mix = y_1 - y_0
	n_years_ind = max(tuple_year_range) - min(tuple_year_range) + 1
	#set new vector
	vec = (np.array(range(tuple_year_range[0], tuple_year_range[1] + 1)) - y_0)/n_years_mix
	vec = np.array([max(min(x, 1), 0) for x in vec])

	return vec
	
#function for calculating differences
def do_df_diff(df_in, df_master, additional_fm = [], field_year = "year"):
	#fields to include as scenario
	fields_scen = ["design_id", "time_series_id", "strategy_id", "future_id"]
	fields_scen_all = ["master_id"] + fields_scen
	#fill in nas
	df_in = df_in.dropna(subset = (["master_id", field_year] + additional_fm)).fillna(float(0)).reset_index(drop = True)
	#merge in applicable data from master?
	fm_master = [x for x in fields_scen if x not in df_in.columns]
	#merge in?
	if len(fm_master) > 0:
		df_in_diff = pd.merge(df_in, df_master[["master_id"] + fm_master], how = "left", on = ["master_id"])
	else:
		df_in_diff = df_in
	#split between base and controled futures
	df_in_diff_base = df_in_diff[(df_in_diff["strategy_id"] == 0) & (df_in_diff["design_id"] == 0)]
	df_in_diff_cont = df_in_diff[df_in_diff["strategy_id"] != 0]
	#remove strategy from base
	df_in_diff_base = df_in_diff_base[[x for x in df_in_diff_base.columns if (x not in ["master_id", "strategy_id", "design_id"])]]

	#get data fields
	fields_data_diff = [x for x in df_in_diff.columns if (x not in (fields_scen_all + [field_year] + additional_fm))]
	#dictionary to rename base fields
	dict_rename_base = dict([[x, ("base_scen_" + x)] for x in fields_data_diff])
	#update
	df_in_diff_base = df_in_diff_base.rename(columns = dict_rename_base)
	#set baseline scenario data fields name
	fields_data_diff_base = [dict_rename_base[x] for x in fields_data_diff]

	#fields to merge in
	fields_scen_merge = list((set(fields_scen) - set({"strategy_id", "design_id"})) | set({field_year}) | set(additional_fm))
	#merge in baseline
	df_in_diff_cont = pd.merge(df_in_diff_cont, df_in_diff_base, how = "left", on = fields_scen_merge).reset_index(drop = True).fillna(float(0))
	#get difference (Strat - Base)
	array_diff =  np.array(df_in_diff_cont[fields_data_diff]) - np.array(df_in_diff_cont[fields_data_diff_base])
	#convert to data frame
	df_diff = pd.DataFrame(array_diff, columns = fields_data_diff)
	#update array out
	df_in_diff = pd.concat([df_in_diff_cont[fields_scen_all + [field_year] + additional_fm], df_diff], axis = 1).sort_values(by = ["master_id", field_year])
	#ensure integer ids
	for field in fields_scen_all:
		df_in_diff[field] = np.array(df_in_diff[field]).astype(int)
		
	return df_in_diff
	

# FUNCTION FOR READING INIS

def read_ini(fp_ini):
	#read in session initialization
	if os.path.exists(fp_ini):
		#read in
		with open(fp_ini) as f:
			list_init = f.readlines()
	else:
		list_init = []

	#remove unwanted blank characters
	for char in ["\n", "\t"]:
		list_init = [l.replace(char, "") for l in list_init]
	#remove instances of blank strings
	list_init = list(filter(lambda x: (x != "") and ("#" in x) == False, list_init))
	list_init = list(filter(lambda x: (x[0] != "["), list_init))
	#split strings
	dict_init = [l.split(":") for l in list_init]
	#convert to dictionary
	dict_init = dict(dict_init)
	#convert numeric values
	for key in dict_init.keys():
		if dict_init[key].isnumeric():
			num = float(dict_init[key])
			if num == int(num):
				dict_init[key] = int(num)
			else:
				dict_init[key] = num
	
	#return the dictionary
	return dict_init
			

# FUNCTION FOR READING ARCHIVE DATA

def get_archive_run(fp_in, archive_run):
	#set the archive directory
	dir_arch = os.path.join(dir_archive_runs, archive_run)
	#ensure it's been unzipped and exists
	if os.path.exists(dir_arch):
		fp_read = os.path.join(dir_arch, os.path.basename(fp_in))
		#read the data set
		if os.path.exists(fp_read):
			out = pd.read_csv(fp_read)
		else:
			print("File '" + os.path.basename(fp_in) + "' not found in '" + dir_arch + "'.")
			out = None
	else:
		print("Archive directory '" + dir_arch + "' not found.")
		out = None

	return out
	
	
# FUNCTION FOR DISPLAYING LIST OUTPUT

def print_list_output(list_in, header):
	print("\n"*3 + "#"*30 + "\n" + header + ":\n" + (("\t%s\n")*len(list_in))%tuple(list_in) + "#"*30 + "\n"*3)


#############################
#    SET FULL FILE PATHS    #
#############################

##  CSV FILES

# ATTRIBUTES
fp_csv_attribute_cost_group = os.path.join(dir_ref, "attribute_cost_group.csv")
fp_csv_attribute_design = os.path.join(dir_ref, "attribute_design.csv")
fp_csv_attribute_future = os.path.join(dir_ed, "attribute_future.csv")
fp_csv_attribute_ghg = os.path.join(dir_ref, "attribute_ghg.csv")
fp_csv_attribute_master = os.path.join(dir_ed, "attribute_master.csv")
fp_csv_attribute_param_fields = os.path.join(dir_ref, "attribute_msec_fields.csv")
fp_csv_attribute_pyparams = os.path.join(dir_ref, "attribute_pyparams.csv")
fp_csv_attribute_runs = os.path.join(dir_ed, "attribute_runs.csv")
fp_csv_attribute_sector = os.path.join(dir_ref, "attribute_sector.csv")
fp_csv_attribute_strategy = os.path.join(dir_ref, "attribute_strategy.csv")
fp_csv_attribute_summing_group = os.path.join(dir_ref, "attribute_summing_group.csv")
fp_csv_attribute_time_series = os.path.join(dir_ref, "attribute_time_series.csv")
# SOME GAMS CSVS
fp_csv_gams_data_duration = os.path.join(dir_gams_input, "data_duracion.csv")
fp_csv_gams_distribution_by_bloq = os.path.join(dir_gams_input, "data_dem_distr_total_bloque.csv")
fp_csv_gams_shared_by_bus = os.path.join(dir_gams_input, "data_dem_distr_total_barra.csv")
fp_csv_gams_data_costo_inversion_procesos_escenarios = os.path.join(dir_gams_input, "data_costo_inversion_procesos_escenarios.csv")
fp_csv_gams_data_demanda_electrica_escenarios = os.path.join(dir_gams_input, "data_demanda_electrica_escenarios.csv")
fp_csv_gams_data_demanda_electrica_escenarios_base = os.path.join(dir_gams_input, "data_demanda_electrica_escenarios_base.csv")
fp_csv_gams_data_hidrologias = os.path.join(dir_gams_input, "data_hidrologias.csv")
fp_csv_gams_data_hidrologias_escenarios = os.path.join(dir_gams_input, "data_hidrologias_escenarios.csv")
fp_csv_gams_data_hidrologias_planificacion = os.path.join(dir_gams_input, "data_hidrologias_planificacion.csv")
fp_csv_gams_data_hidrologias_simulacion = os.path.join(dir_gams_input, "data_hidrologias_simulacion.csv")
fp_csv_gams_data_precio_energeticos_escenarios = os.path.join(dir_gams_input, "data_precio_energeticos_escenarios.csv")
fp_csv_gams_data_set_escenarios = os.path.join(dir_gams_input, "data_set_escenarios.csv")
fp_csv_gams_data_set_scen = os.path.join(dir_gams_input, "data_set_escenario_sel.csv")
fp_csv_gams_solution_generation_sector = os.path.join(dir_gams_output, "solution_generation_sector.csv")
# GAMS PARALLELIZATION SUPPORT REFRENCE FILES
fp_csv_gams_parallel_support_lines_to_remove = os.path.join(dir_ref, "gams_parallel_support-lines_to_remove.csv")
fp_csv_gams_parallel_support_string_replacements = os.path.join(dir_ref, "gams_parallel_support-string_replacements.csv")
# OTHER CSVS
fp_csv_analytica_metrics_to_save = os.path.join(dir_ref, "analytica_metrics_to_save.csv")
fp_csv_attribute_fuel = os.path.join(dir_ref, "attribute_fuel.csv")
fp_csv_attribute_technology = os.path.join(dir_ref, "attribute_technology.csv")
fp_csv_distance_results_transport = os.path.join(dir_ref, "Distance_Results_Transport.csv")
fp_csv_experimental_design = os.path.join(dir_ed, "experimental_design.csv")
fp_csv_experimental_design_msec = os.path.join(dir_ed, "experimental_design_multi_sector.csv")
fp_csv_experimental_design_msec_diff = os.path.join(dir_ed, "experimental_design_multi_sector_diff.csv")
fp_csv_experimental_design_msec_masters_to_run = os.path.join(dir_ed, "experimental_design_multi_sector_masters_to_run.csv")
fp_csv_experimental_design_msec_masters_to_run_gams = os.path.join(dir_ed, "experimental_design_multi_sector_masters_to_run_gams.csv")
fp_csv_experimental_design_msec_single_vals = os.path.join(dir_ed, "experimental_design_multi_sector_single_vals.csv")
fp_csv_experimental_design_cloud = os.path.join(dir_ed, "experimental_design_cloud.csv")
fp_csv_experimental_design_transportation = os.path.join(dir_ed, "experimental_design_transportation.csv")
fp_csv_failed_runs = os.path.join(dir_out, "failed_runs.csv")
fp_csv_failed_instances = os.path.join(dir_out, "failed_instances.csv")
fp_csv_fields_keep_experimental_design_multi_sector = os.path.join(dir_ref, "fields_keep-experimental_design_multi_sector.csv")
fp_csv_output_field_types = os.path.join(dir_ref, "output_field_types.csv")
fp_csv_lhs_table_multi_sector = os.path.join(dir_ed, "lhs_samples_multi_sector.csv")
fp_csv_lhs_table_levers = os.path.join(dir_ed, "lhs_samples_levers.csv")
fp_csv_map_parameter_to_gams = os.path.join(dir_ref, "map_parameter_to_gams.csv")
fp_csv_output_multi_sector = os.path.join(dir_out, "output_multi_sector_python.csv")
fp_csv_output_multi_sector_base_year = os.path.join(dir_out, "output_multi_sector-base_year.csv")
fp_csv_output_multi_sector_diff = os.path.join(dir_out, "output_multi_sector-diff_from_base_strategy.csv")
fp_csv_output_multi_sector_analytica = os.path.join(dir_out, "output_multi_sector_analytica.csv")
fp_csv_output_multi_sector_pmr = os.path.join(dir_out, "output_multi_sector_pmr.csv")
fp_csv_parameter_ranges = os.path.join(dir_ref, "parameter_ranges.csv")
fp_csv_parameter_ranges_for_analytica_base = os.path.join(dir_ref, "parameter_ranges_for_analytica_base.csv")
fp_csv_prim_field_attribute = os.path.join(dir_out, "prim-attribute_field.csv")
fp_csv_prim_input_data = os.path.join(dir_out, "prim-input_data.csv")
fp_csv_ranges_for_decarb_drivers = os.path.join(dir_out, "ranges_for_decarb_drivers.csv")
fp_csv_ranges_vals_for_decarb_drivers = os.path.join(dir_out, "ranges_values_for_decarb_drivers.csv")
fp_csv_waste_baseline_data = os.path.join(dir_ref, "waste_baseline_data.csv")

##  TEMPORARY CSVS
fp_csv_tmp_correction_for_pib_peso_traj = os.path.join(dir_ref, "tmp_correction_for_pib_peso_traj.csv")

##  GAMS FILE
fp_gams_modelo = os.path.join(dir_gams_modelo, "modelo_energetico_PMR_20201201.gms")
fp_gams_modelo_nogdxcall = os.path.join(dir_gams_modelo, "modelo_energetico_PMR_20201201_nogdxcall.gms")
fp_gams_pmr_prerun_gdx_build = os.path.join(dir_gams_modelo, "pmr_prerun_gdx_build.gms")

##  EXCEL
fp_xlsx_parameter_correlation_matrices = os.path.join(dir_out, "parameter_correlation_matrices.xlsx")

##  EXECUTABLES
fp_exec_gams = str(dict_init["path_gams"])
#check...
if not os.path.exists(fp_exec_gams):
	print("WARNING: gams executable '" + fp_exec_gams + "' not found.")

##############################
#    SOME BOOLEAN QUERIES    #
##############################

# GENERAL BOOLEANS

integrate_analytica_q = False
#check system
if plt[0:min(len(plt), 3)] != "win":
	#check existence
	if os.path.exists(dir_ade):
		#integrate the analytica models a parallels structure?
		integrate_analytica_q = (str(dict_init["integrate_analytica_q"]).lower() == "true")
else:
	integrate_analytica_q = True
	print("\n"*10 + "YAY ANALYTICA" + "\n"*10)
#use landuse difference for conversion?
use_lu_diff_for_conv_q = (str(dict_init["use_lu_diff_for_conv_q"]).lower() == "true")
#use parallel execution of gams?
parallel_exec_gams_q = (str(dict_init["parallel_exec_gams_q"]).lower() == "true")

#read in lhs tables? also default to false
read_lhs_tables_q = False
#check paths
if (str(dict_init["read_lhs_tables_q"]).lower() == "true"):
	#check for path
	if os.path.exists(fp_csv_lhs_table_multi_sector) and os.path.exists(fp_csv_lhs_table_levers):
		read_lhs_tables_q = True

#run tornado design?
tornado_q = (str(dict_init["experimental_mode"]).lower() == "tornado")

##############################
#    SOME ADDITIONAL DATA    #
##############################

#build dictionary of sector abbreviations
df_attribute_sector = pd.read_csv(fp_csv_attribute_sector)
dict_sector_to_abv = build_dict(df_attribute_sector[["sector", "sector_abbreviation"]])
	
#build dictionary of summing group units
df_attribute_summing_group = pd.read_csv(fp_csv_attribute_summing_group)
dict_summing_group_to_unit = build_dict(df_attribute_summing_group[["summing_group", "unit"]])

#build dictionary mapping sampled parameters to gams parameters
df_map_param_to_pg = pd.read_csv(fp_csv_map_parameter_to_gams)
dict_map_params_to_params_gams = build_dict(df_map_param_to_pg[["parameter", "parameter_gams"]])
	


##########################################
#    CHECK OTHER DIRECTORIES AND FILES   #
##########################################

# CREATE OUTPUT DIRECTORY
if not os.path.exists(dir_out):
    os.makedirs(dir_out, exist_ok = True)

# INITIALIZE FAILED CASES CSV
if not os.path.exists(fp_csv_failed_runs):
    dfc = pd.DataFrame({"run_id": []})
    dfc.to_csv(fp_csv_failed_runs, index = None)

