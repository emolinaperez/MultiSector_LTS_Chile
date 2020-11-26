import os, os.path
import numpy as np
import time
import pandas as pd
import setup_runs as sr
import sector_models as sm
import shutil



#initialize time
t0 = time.time()
#get initialization information
dict_init = sr.dict_init


###   READ IN SOME CSVs



# attribute file
df_attribute_master_id = pd.read_csv(sr.fp_csv_attribute_master)


###   READ IN EXPERIMENTAL DESIGN

print("Reading in experimental design from " + sr.fp_csv_experimental_design_msec + "...")
#read in experimental design
exp_design = pd.read_csv(sr.fp_csv_experimental_design_msec)
exp_design_single_val = pd.read_csv(sr.fp_csv_experimental_design_msec_single_vals)
#setup experimental design columns
exp_design_cols = list(set(exp_design.columns) | set(exp_design_single_val.columns))
exp_design_cols.sort()
#read in parameters and create a dictionary that maps field to sectors
params = pd.read_csv(sr.fp_csv_parameter_ranges)
#pull in master ids to run
df_masters_to_run = pd.read_csv(sr.fp_csv_experimental_design_msec_masters_to_run)
#reduce
exp_design = exp_design[exp_design["master_id"].isin(list(df_masters_to_run["master_id"]))].reset_index(drop = True)

#remove lever delta data
exp_design = exp_design[[x for x in exp_design.columns if not ("lever_delta_" in x)]]
exp_design_single_val = exp_design_single_val[[x for x in exp_design_single_val.columns if not ("lever_delta_" in x)]]
#function to expand single values out
def edsv_expand(n_row):
	#check columns
	cols = [x for x in list(exp_design_single_val.columns) if x not in exp_design.columns]
	n_cols = len(cols)
	
	if n_cols > 0:
		#expand out
		array_expand = np.array([np.array(exp_design_single_val)[0] for x in range(n_row)])
		#convert to data frae
		df_expand = pd.DataFrame(array_expand, columns = list(exp_design_single_val.columns))
	else:
		df_expand = pd.DataFrame([], columns = None)
		
	return(df_expand)
	
	

print("Generating wide experimental design (Time elapsed: " + str(np.round((time.time() - t0)/60, 2)) + " minutes)...")
#update experimental design
exp_design = pd.concat([exp_design, edsv_expand(len(exp_design))], axis = 1)
#sort
exp_design = exp_design.sort_values(by = ["master_id", "year"])



##  CHECK MAX

#exp_design["lever_waste_target_fraction_waste_sewage_treated"]
df_attribute_fields = pd.read_csv(sr.fp_csv_attribute_param_fields)
#dictionary of upper bounds
dict_field_caps = dict([tuple(x) for x in np.array(df_attribute_fields[["field", "max_val"]].dropna(subset = ["max_val"]))])
#loop over fields to check
for field in dict_field_caps.keys():
	#check for inclusion
	if field in exp_design.columns:
		print("Checking upper bounds for  " + str(field) + "...")
		#map to experimental design
		vec_field = np.array(exp_design[field])
		#get upper bound
		sup = float(dict_field_caps[field])
		#check for values that exceed the cap
		vec_field[np.where(vec_field > sup)] = sup
		#update
		exp_design[field] = vec_field
	

##  CHECK NORMALIZATION GROUPS

#ensure normalization in experimental design
norm_groups = params[["parameter", "normalize_group"]].drop_duplicates().dropna()
#all normalization groups
all_ng = list(set(norm_groups["normalize_group"]))
all_ng.sort()
#loop
for norm in all_ng:
	print("Checking normalization group " + str(int(norm)) + "...")
	#get fields
	fields_ng = list(norm_groups[norm_groups["normalize_group"] == norm]["parameter"])
	#remove from experimental design
	array_ng = np.array(exp_design[fields_ng])
	#get total
	tot_ng = sum(array_ng.transpose())
	#normalize
	array_ng = (array_ng.transpose()/tot_ng).transpose()
	#update
	array_ng = pd.DataFrame(array_ng, columns = fields_ng)
	#tack on
	exp_design = pd.concat([exp_design[[x for x in exp_design.columns if x not in fields_ng]], array_ng], axis = 1)




###################################
#    GET SOME OTHER PARAMETERS    #
###################################
	
#set all fields in the design
all_fields = exp_design_cols
#all years
all_year = list(exp_design["year"].unique())
all_year.sort()
#all futures
all_future = list(exp_design["future_id"].unique())
all_future.sort()
#all strategies
all_strat = list(exp_design["strategy_id"].unique())
all_strat.sort()
#all designs
all_design = list(exp_design["design_id"].unique())
all_design.sort()
#all time series
all_time_series = list(exp_design["time_series_id"].unique())
all_time_series.sort()
#all master ids
all_master = list(exp_design["master_id"].unique())
all_master.sort()
#all sectors and associated information information
params_svn = params[["sector", "parameter"]]
params_svn = params_svn.drop_duplicates()
all_sectors = list(params_svn["sector"].unique())
#get model years
model_years = sr.output_model_years
#initialize sector field dictionary
dict_sector_field = {}
#update the dictionaruy with fields
for sec in all_sectors:
	tmp_df = params_svn[(params_svn["sector"] == sec)]
	#get fields associated with it
	fields = [x.replace(" ", "_").lower() for x in tmp_df["parameter"]]
	#update
	dict_sector_field.update({sec: fields})

#fields to use for merging in sector data frames
fields_id_for_df_merges = ["master_id", "year"]
#sort the experimental design appropriately
exp_design = exp_design.sort_values(by = fields_id_for_df_merges)



###############################
###                         ###
###    LOOP OVER SECTORS    ###
###                         ###
###############################

dict_sector_functions = {
	"commercial": sm.sm_commercial,
	"industry_and_mining": sm.sm_industry_and_mining,
	"public": sm.sm_public,
	"residential": sm.sm_residential,
	"transport": sm.sm_transport
}


##  ADD DICTIONARY OF DATA TO MERGE FOR EACH SECTOR (IF APPLICABLE)

# Transportation correction for econometric model
df_tmp_correction_for_pib_peso_traj = pd.read_csv(sr.fp_csv_tmp_correction_for_pib_peso_traj)
#get baseline data from experimental design
df_tmp_correction_for_pib_peso_traj = pd.merge(df_tmp_correction_for_pib_peso_traj, exp_design[exp_design["master_id"] == 0][["year", "pib"]].copy(), how = "left", on = ["year"]).reset_index(drop = True)
#add scalar and string name
str_pib_scalar = "pib_scalar_transpiort"
df_tmp_correction_for_pib_peso_traj[str_pib_scalar] = np.array(df_tmp_correction_for_pib_peso_traj["pib_peso"])/np.array(df_tmp_correction_for_pib_peso_traj["pib"])
df_tmp_correction_for_pib_peso_traj = df_tmp_correction_for_pib_peso_traj[["year", str_pib_scalar]]
#data to merge in
dict_sector_merge = {
	"industry_and_mining": df_tmp_correction_for_pib_peso_traj,
	"transport": df_tmp_correction_for_pib_peso_traj,
	"commercial": df_tmp_correction_for_pib_peso_traj
}


##  EXECUTE LOOP OVER SECTORS

#sectors to run over (in order)
sectors_run = list(dict_sector_functions)
sectors_run.sort()

dict_sector_returns = {}
#id fields to include in results
fields_results_id = ["master_id", "year"]
#initialize results
results = [exp_design[fields_results_id].copy()]
#loop over each sector to build
for sector in sectors_run:
	
	#get sector abbreviation
	sector_abv = sr.dict_sector_to_abv[sector]
	
	if sector in dict_sector_merge.keys():
		#get fields
		fm = list(set(exp_design.columns) & set(dict_sector_merge[sector].columns))
		#merge in data and sort (same ordering as exp_design)
		df_ed = pd.merge(exp_design, dict_sector_merge[sector], how = "left", on = fm).sort_values(by = fields_id_for_df_merges).reset_index(drop = True)
		df_ed = df_ed.sort_values(by = fields_id_for_df_merges)
	else:
		df_ed = exp_design
		
	print("\nBuilding " + str(sector) + " results...")
	# RUN MODEL
	df_sector_out = pd.DataFrame(dict_sector_functions[sector](df_ed, sr.dict_sector_to_abv))
	#add to the output
	results.append(df_sector_out)
	
	dict_sector_returns.update({
		sector: {
			"data_frame": df_sector_out,
			"fields_dat": list(df_sector_out.columns)
		}
	})
	

#merge
results = pd.concat(results, axis = 1)
#data fields
fields_extract = list(set(results.columns) - set(fields_results_id))
fields_extract.sort()
#reduce
results = results[results["year"].isin(sr.output_model_years)]
#update extraction fields
fields_extract = ["master_id", "year"] + fields_extract
#re-order columns
results = results[fields_extract]

##  BUILD BASE YEAR FILE
results_by = results[results["year"] == (int(sr.dict_init["add_sec_variation_start_year"]) - 1)]



#############################################################
###                                                       ###
###    COPY IN BAU FROM DESIGN_ID = 0 TO OTHER DESIGNS    ###
###                                                       ###
#############################################################
 
#get all designs
all_designs = list(set(exp_design["design_id"]))
all_designs.sort()
#get all time/run tuples included in the baseline design
tmp_ed = exp_design[(exp_design["design_id"] == 0) & (exp_design["strategy_id"] == 0)]
tr_tuples_in_baseline_design = set([tuple(x) for x in np.array(tmp_ed[["time_series_id", "run_id"]])])
#dictionary to store needed tuples in
df_design_tr_tuples = []

#loop to determine which T/R combos have to be copied from the baseline design to
for did in [x for x in all_designs if x > 0]:
	#temporary subset
	tmp_cloud = exp_design[exp_design["design_id"] == did]
	#check for strategy
	tmp_tuples = set([tuple(x) for x in np.array(tmp_cloud[tmp_cloud["strategy_id"] == 0][["time_series_id", "run_id"]])])
	#vals that have to be copied over from
	copy_tuples = tr_tuples_in_baseline_design - tmp_tuples
	#convert to data frame
	copy_tuples = pd.DataFrame(np.array([x for x in list(copy_tuples)]).astype(int), columns = ["time_series_id", "run_id"])
	#sort
	copy_tuples = copy_tuples.sort_values(by = ["time_series_id", "run_id"]).reset_index(drop = True)
	#add design id
	copy_tuples["design_id"] = [did for x in range(len(copy_tuples))]
	
	df_design_tr_tuples.append(copy_tuples)

if len(df_design_tr_tuples) > 0:
	df_design_tr_tuples = pd.concat(df_design_tr_tuples, axis = 0)
	
	


#########################
#    EXECUTE THE COPY   #
#########################

print("Starting copy of BAU from design_id = 0 to other design_ids...")

#a commong field vector for merging
fields_trd = ["time_series_id", "run_id", "design_id"]
#initialize outputs
append_ed = [exp_design]
append_out = [results]
#loop over additional designs
for did_other in [x for x in all_designs if x != 0]:
	#get dataframe of design tr tuples that have to be copied over for the given time series id
	df_tmp_to_copy = df_design_tr_tuples[df_design_tr_tuples["design_id"] == did_other][["time_series_id", "run_id"]]
	#add in design_id (set to baseline)
	df_tmp_to_copy["design_id"] = [0 for x in range(len(df_tmp_to_copy))]
	#merge in ed
	df_ed_tmp_to_copy = pd.merge(df_tmp_to_copy, exp_design, how = "left", on = fields_trd)
	#get master ids of interest
	df_master_tmp_to_copy = pd.merge(df_tmp_to_copy, df_attribute_master_id[["master_id"] + fields_trd], how = "left", on = fields_trd)
	#merge in output
	df_out_tmp_to_copy = pd.merge(df_master_tmp_to_copy, results, how = "left", on = ["master_id"])

	#check length
	if len(df_ed_tmp_to_copy) > 0:
		print("Copying baseline strategy (0) data from design 0 for design " + str(did_other) + "...")
		#add in design id
		df_ed_tmp_to_copy["design_id"] = [did_other for x in range(len(df_ed_tmp_to_copy))]
		df_out_tmp_to_copy["design_id"] = [did_other for x in range(len(df_out_tmp_to_copy))]
		#remove master id
		df_out_tmp_to_copy = df_out_tmp_to_copy[[x for x in df_out_tmp_to_copy.columns if x != "master_id"]]
		df_ed_tmp_to_copy = df_ed_tmp_to_copy[[x for x in df_ed_tmp_to_copy.columns if x != "master_id"]]
		#extraction fields to merge on
		fem = fields_trd
		#merge in master
		df_ed_tmp_to_copy = pd.merge(df_ed_tmp_to_copy, df_attribute_master_id[["master_id"] + fem], how = "left", on = fem)
		df_out_tmp_to_copy = pd.merge(df_out_tmp_to_copy, df_attribute_master_id[["master_id"] + fem], how = "left", on = fem)
		#set names
		df_ed_tmp_to_copy = df_ed_tmp_to_copy[exp_design.columns]
		df_out_tmp_to_copy = df_out_tmp_to_copy[results.columns]

		#append to design copy
		append_ed.append(df_ed_tmp_to_copy)
		append_out.append(df_out_tmp_to_copy)

exp_design = pd.concat(append_ed, axis = 0)
results = pd.concat(append_out, axis = 0)





##################################
###                            ###
###    BUILD GAMS DATA FILE    ###
###                            ###
##################################


#get total demand
results["all-electricity_total_demand-gwh"] = results[[x for x in results.columns if ("electricity_total_demand" in x)]].sum(axis = 1)
#reduce to total demand
df_demand = results[["master_id", "year", "all-electricity_total_demand-gwh"]].copy().rename(columns = {"all-electricity_total_demand-gwh": "Total", "year": "Year"})

# Se leen los archivos CSV y se guardan como dataframes
df_duration = pd.read_csv(sr.fp_csv_gams_data_duration)
df_distr_bloq = pd.read_csv(sr.fp_csv_gams_distribution_by_bloq)
df_distr_bus = pd.read_csv(sr.fp_csv_gams_shared_by_bus)
#clean
df_distr_bus = df_distr_bus.rename(columns = {"Agno": "Year"})
#get
all_master = list(df_demand["master_id"].unique())
all_master.sort()
# Se define como parametro la cantidad de annos
years = len(df_demand["Year"].unique())
# Se extraen los nombres de las barras
bus_1 = df_distr_bus.iloc[0][0]
bus_2 = df_distr_bus.iloc[1][0]
# Se filtra el dataframe que contiene los porcentajes de distribucion de la demanda entre las barras en un dataframe por barra
df_distr_bus_1 = df_distr_bus[df_distr_bus["Bus"] == bus_1].reset_index(drop = True)
df_distr_bus_2 = df_distr_bus[df_distr_bus["Bus"] == bus_2].reset_index(drop = True)

#build master id
df_master_id = df_demand[["master_id", "Year"]].copy()
##  BUILD DEMAND BY BUS
fields_index = ["master_id", "Year"]
df_demand_by_bus = df_distr_bus.copy()
#merge in total demand
df_demand_by_bus = pd.merge(df_demand, df_demand_by_bus, how = "outer", on = ["Year"])
# Se multiplican las columnas de la demanda total con la columna del dataframe con los porcentajes por barras y se colocan en la columna del dataframme
df_demand_by_bus["valor"] = np.array(df_demand_by_bus["Shared_by_bus"])*np.array(df_demand_by_bus["Total"])
df_demand_by_bus = df_demand_by_bus[fields_index + ["Bus", "valor"]].sort_values(by = fields_index)

#get duration by block
df_duration = df_duration.rename(columns = {"Agno": "Year"})
df_distr_bloq = df_distr_bloq.merge(df_duration, on = ["Year", "Etapa", "Bloque"], how = "left")
#get all demand data merged
df_data_demanda = pd.merge(df_demand_by_bus, df_distr_bloq, how = "outer", on = ["Year", "Bus"]).rename(columns = {"valor": "Demanda_Barra_Agno"})

# Se obtienen las columnas que son la multiplicacion de otras columnas
df_data_demanda["Potencia_Bloque"] = 1000*np.array(df_data_demanda["Distribucion_Bloque"]) * np.array(df_data_demanda["Distribucion_Etapa"]) * np.array(df_data_demanda["Demanda_Barra_Agno"])/np.array(df_data_demanda["Duracion"])
df_gams_demands = df_data_demanda[["master_id", "Bus", "Year", "Etapa", "Bloque", "Potencia_Bloque"]]
df_gams_demands = df_gams_demands.rename(columns = {"master_id":"Escenario", "Bus":"Barra", "Year":"Agno", "Potencia_Bloque":"Demanda"})





###################################
###                             ###
###    BUILD DIFFERENCE FILE    ###
###                             ###
###################################

print("Building difference file...")
#fields to include as scenario
fields_scen = ["design_id", "time_series_id", "strategy_id", "future_id"]
fields_scen_all = ["master_id"] + fields_scen
#merge in applicable data from master
results_diff = pd.merge(results, df_attribute_master_id[fields_scen_all], how = "left", on = ["master_id"])
#split between base and controled futures
results_diff_base = results_diff[(results_diff["strategy_id"] == 0) & (results_diff["design_id"] == 0)]
results_diff_cont = results_diff[results_diff["strategy_id"] != 0]
#remove strategy from base
results_diff_base = results_diff_base[[x for x in results_diff_base.columns if (x not in ["master_id", "strategy_id", "design_id"])]]

#get data fields
fields_data_diff = [x for x in results_diff.columns if (x not in fields_scen_all + ["year"])]
#dictionary to rename base fields
dict_rename_base = dict([[x, ("base_scen_" + x)] for x in fields_data_diff])
#update
results_diff_base = results_diff_base.rename(columns = dict_rename_base)
#set baseline scenario data fields name
fields_data_diff_base = [dict_rename_base[x] for x in fields_data_diff]

#fields to merge in
fields_scen_merge = list((set(fields_scen) - set({"strategy_id", "design_id"})) | set({"year"}))
#merge in baseline
results_diff_cont = pd.merge(results_diff_cont, results_diff_base, how = "left", on = fields_scen_merge).reset_index(drop = True)
#get difference (Strat - Base)
array_diff =  np.array(results_diff_cont[fields_data_diff]) - np.array(results_diff_cont[fields_data_diff_base])
#convert to data frame
df_diff = pd.DataFrame(array_diff, columns = fields_data_diff)
#update array out
results_diff = pd.concat([results_diff_cont[fields_scen_all + ["year"]], df_diff], axis = 1).sort_values(by = ["master_id", "year"])



##  EXPORT DATA

# main file
print("Writing results to " + sr.fp_csv_output_multi_sector + " (Time elapsed: " + str(np.round((time.time() - t0)/60, 2)) + " minutes)...")
#export
results.to_csv(sr.fp_csv_output_multi_sector, index = False, encoding = "utf-8")

# difference file
print("Writing results_diff to " + sr.fp_csv_output_multi_sector_diff + " (Time elapsed: " + str(np.round((time.time() - t0)/60, 2)) + " minutes)...")
#export
results_diff.to_csv(sr.fp_csv_output_multi_sector_diff, index = False, encoding = "utf-8")

# base year file
print("Writing results_by to " + sr.fp_csv_output_multi_sector_base_year + " (Time elapsed: " + str(np.round((time.time() - t0)/60, 2)) + " minutes)...")
#export
results_by.to_csv(sr.fp_csv_output_multi_sector_base_year, index = False, encoding = "utf-8")

# gams demand file
print("Writing df_gams_demands to " + sr.fp_csv_gams_data_demanda_electrica_escenarios + " (Time elapsed: " + str(np.round((time.time() - t0)/60, 2)) + " minutes)...")
#export
df_gams_demands.to_csv(sr.fp_csv_gams_data_demanda_electrica_escenarios, index = False, encoding = "UTF-8")


print("Done with python models. Total time elapsed: " + str(np.round((time.time() - t0)/60, 2)) + " minutes)")



###################################
###                             ###
###    RUN ANALYTICA MODELS?    ###
###                             ###
###################################

if sr.integrate_analytica_q:
	#to run using parallels
	if sr.analytical_platform == "unix":
		print("\n\nRunning integrated model...")
		
		cmd = "prlctl exec \"syme-j-PVM\" cmd /c \"C:\\Users\\jsyme\\AppData\\Local\\Programs\\Python\\Python37\\python.exe C:\\Users\\jsyme\\Documents\\Projects\\SWCHE076-1000\\ade_beta\\python\\run_analytica.py\""
		os.system(cmd)
		
		#collect output
		dict_files_copy_in = {
			sr.dir_out_ade: [sr.fp_csv_output_multi_sector_analytica]
		}
		
		#copy over
		for dc in dict_files_copy_in.keys():
			#get files to copy
			files_copy = dict_files_copy_in[dc]
			
			print("Copying files from Parallels at " + dc + " :")
			
			for fc in files_copy:
				fp_old = os.path.join(dc, os.path.basename(fc))
				#copy over
				cmd_cp = "cp \"" + fp_old + "\" \"" + fc + "\""
				#execute
				os.system(cmd_cp)
				#noftify
				print("\t\nCopied " + fp_old + " to " + fc)
			print("")
	else:
		print("ADD IN WINDOWS SIDE COMMANDS")
		
	print("Analytica done.")




####################################
###                              ###
###    CREATE PACKAGE TO PASS    ###
###                              ###
####################################

#get date
str_date = time.strftime("%Y_%m_%d", time.gmtime())
#create package name
dir_package = sr.dict_init["tar_base_name"] + "_" + str_date
#set export directory
dir_tmp_export = os.path.join(sr.dir_out, dir_package)
#check existence
if (os.path.exists(dir_tmp_export)) == True:
	#clear out the directory
	shutil.rmtree(dir_tmp_export)
#make the directory anew
os.makedirs(dir_tmp_export, exist_ok = True)

#dictionary of keep fields
dict_fields_keep_export = {}
#get reduced experimental design data to export
if os.path.exists(sr.fp_csv_fields_keep_experimental_design_multi_sector):
	fields_keep_ed = pd.read_csv(sr.fp_csv_fields_keep_experimental_design_multi_sector)
	#fill na
	fields_keep_ed = fields_keep_ed.fillna(0)
	#update types
	for field in [x for x in fields_keep_ed.columns if x != "field"]:
		fields_keep_ed[field] = np.array(fields_keep_ed[field]).astype(int)
		#string to add to dictionary
		str_dict = field.lower().replace("include_", "").replace("_file", "")
		#extraction fields
		fields_ext = list(fields_keep_ed[fields_keep_ed[field] == 1]["field"])
		#check for values in the experimental design that are not specified, and default to include them
		fields_not_included = list(set(exp_design.columns) - set(fields_keep_ed[field]))
		#add in
		fields_ext = fields_ext + fields_not_included
		#update
		dict_fields_keep_export.update({str_dict: fields_ext})
else:
	#update types
	for f_type in ["all", "diff"]:
		#set field
		field = "include_" + f_type + "_file"
		#string to add to dictionary
		str_dict = field.lower().replace("include_", "").replace("_file", "")
		#extraction fields
		fields_ext = list(exp_design.columns)
		#update
		dict_fields_keep_export.update({str_dict: fields_ext})


#file path out for experimental design
fp_ed_out = os.path.join(dir_tmp_export, os.path.basename(sr.fp_csv_experimental_design_msec))
#notify
print("Exporting reduced experimental design to " + fp_ed_out + "...")
#get columns to keep
fields_ext = dict_fields_keep_export["all"]
#ensure availability
fields_ext = [x for x in fields_ext if x in exp_design.columns]
#write out experimental design (reduced)
exp_design[exp_design["year"].isin(sr.output_model_years)][fields_ext].to_csv(fp_ed_out, index = None, encoding = "UTF-8")


#file path out for experimental design differences
fp_ed_diff_out = os.path.join(dir_tmp_export, os.path.basename(sr.fp_csv_experimental_design_msec_diff))
#notify
print("Reading, reducing, and exporting experimental design differences to " + fp_ed_diff_out + "...")
#pull in difference design
exp_design_diff = pd.read_csv(sr.fp_csv_experimental_design_msec_diff)
#get columns to keep
fields_ext = dict_fields_keep_export["diff"]
#ensure availability
fields_ext = [x for x in fields_ext if x in exp_design_diff.columns]
#reduce
exp_design_diff = exp_design_diff[exp_design_diff["year"].isin(sr.output_model_years)][fields_ext]
#write to output
exp_design_diff.to_csv(fp_ed_diff_out, index = None, encoding = "UTF-8")


#files to copy in
list_files_copy = [
	sr.fp_csv_output_multi_sector,
	sr.fp_csv_output_multi_sector_base_year,
	sr.fp_csv_output_multi_sector_diff,
	sr.fp_csv_attribute_master,
	sr.fp_csv_attribute_runs
]
#add in analytica output?
if sr.integrate_analytica_q:
	if os.path.exists(sr.fp_csv_output_multi_sector_analytica):
		print("Found " + sr.fp_csv_output_multi_sector_analytica + "... adding to copy files.\n")
		list_files_copy = list_files_copy + [sr.fp_csv_output_multi_sector_analytica]
	
#loop
for fp in list_files_copy:
	#new file path out
	fp_out = os.path.join(dir_tmp_export, os.path.basename(fp))
	#print
	print("Copying " + fp + " to " + fp_out + "...")
	#copy over
	shutil.copy(fp, fp_out)
#new package
fp_package_compressed = os.path.join(sr.dir_out, dir_package + ".tar.gz")
#build tar
if os.path.exists(fp_package_compressed):
	#remove it if so
	os.remove(fp_package_compressed)
#set script execution to generate new tarball—IMPORTANT:COPYFILE_DISABLE=1 *MUST* BE SET TO 1 TO ELIMINATE ERRONEOUS FILES IN THE EXTRACTION
print("Compressing " + dir_tmp_export + " to  " + fp_package_compressed + "...\n\n")
#get current directory
dir_current = os.getcwd()
#change working directory
os.chdir(sr.dir_out)
#tarball command
comm_tar = "COPYFILE_DISABLE=1 tar -cvzf \"" + fp_package_compressed + "\" " + dir_package
#run
os.system(comm_tar)
#remove temporary copy
shutil.rmtree(dir_tmp_export)
#change back
os.chdir(dir_current)
