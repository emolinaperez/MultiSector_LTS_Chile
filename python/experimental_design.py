import setup_runs as sr
import os, os.path
import pandas as pd
import numpy as np
import pyDOE as pyd

#export files?
export_ed_files_q = True



##########################################
###                                    ###
###    GENERATE EXPERIMENTAL DESIGN    ###
###                                    ###
##########################################

print("Starting build of components for experimental design.")


#number of lhs samples
n_lhs = sr.dict_init["n_lhs"]
#set baseline strategy
strat_baseline = 0#[x for x in sr.dict_strat.keys() if sr.dict_strat[x]["strategy_id"] == 0][0]

###   SOME ATTRIBUTE TABLES
df_attribute_design_id = pd.read_csv(sr.fp_csv_attribute_design)
#reduce
df_attribute_design_id = df_attribute_design_id[df_attribute_design_id["include"] == 1]
#get time series id
df_attribute_time_series_id = pd.read_csv(sr.fp_csv_attribute_time_series)


print("Check: export_ed_files_q = " + str(export_ed_files_q))
print("Check: n_lhs = " + str(n_lhs))

    


#################################
#    MULTI SECTOR COMPONENTS    #
#################################

#read in uncertainty table for additional sectors
parameter_table_additional_sectors = pd.read_csv(sr.fp_csv_parameter_ranges)
#reduce
parameter_table_additional_sectors = parameter_table_additional_sectors[parameter_table_additional_sectors["type"].isin(["incertidumbre", "accion"])]
#add field
parameter_table_additional_sectors["variable_name_lower"] = [x.lower().replace(" ", "_") for x in list(parameter_table_additional_sectors["parameter"])]
#fill nas and set to integer
parameter_table_additional_sectors["parameter_constant_q"] = parameter_table_additional_sectors["parameter_constant_q"].fillna(0)
parameter_table_additional_sectors["parameter_constant_q"] = np.array(parameter_table_additional_sectors["parameter_constant_q"]).astype(int)
#initialize available groups
groups_norm = set([int(x) for x in parameter_table_additional_sectors["normalize_group"] if not np.isnan(x)])

###   NORMALIZATION GROUP IDS

group_id = parameter_table_additional_sectors[["type", "parameter", "normalize_group"]].drop_duplicates()
#build normalize group and lever group ids (for deltas)
norm_vec = []

if len(groups_norm) > 0:
	#starting point for new group
	ind_group = max(groups_norm) + 1
else:
	ind_group = 1
	
#loop over rows
for i in range(0, len(group_id)):
    #get current group
    group_cur = group_id["normalize_group"].iloc[i]
    #test for NaN
    if np.isnan(group_cur):
        norm_vec = norm_vec + [ind_group]
        #next iteration
        ind_group += 1
    else:
        norm_vec = norm_vec + [int(group_cur)]

#add to group_id data frame
group_id["norm_group_id"] = norm_vec
group_id = group_id.reset_index(drop = True)


###   LEVER GROUP IDS

#temporary data frame to build lever group id with
group_id_tmp = group_id[["type", "norm_group_id"]].drop_duplicates()
group_id_tmp = group_id_tmp[group_id_tmp["type"].isin(["Accion", "accion"])]
group_id_tmp["lever_group_id"] = range(1, len(group_id_tmp) + 1)
if "lever_group_id" not in group_id.columns:
    group_id = pd.merge(group_id, group_id_tmp[["norm_group_id", "lever_group_id"]], how = "left", left_on = ["norm_group_id"], right_on = ["norm_group_id"])
#reduce
group_id = group_id[["parameter", "type", "norm_group_id", "lever_group_id"]]
#replace nas
group_id = group_id.fillna({"lever_group_id": -1})
#integer
group_id["lever_group_id"] = [int(x) for x in list(group_id["lever_group_id"])]
#merge in
group_id  = pd.merge(group_id, parameter_table_additional_sectors[["parameter", "variable_name_lower"]], how = "left", left_on = ["parameter"], right_on = ["parameter"])
group_id = group_id.drop_duplicates()
group_id = group_id[["parameter", "type", "variable_name_lower", "norm_group_id", "lever_group_id"]]


###   MERGE BACK IN TO PTAS AND CLEAN NAMES/DATA

#set merge fields and merge
fields_merge = list(set(parameter_table_additional_sectors.columns).intersection(set(group_id.columns)))
parameter_table_additional_sectors = pd.merge(parameter_table_additional_sectors, group_id, how = "left", left_on = fields_merge, right_on = fields_merge)
#fields to extract
fields_ext = [x for x in parameter_table_additional_sectors if (x not in ["normalize_group"])]
#clean the data frame
parameter_table_additional_sectors = parameter_table_additional_sectors[fields_ext]
parameter_table_additional_sectors = parameter_table_additional_sectors.dropna(axis = 1)
#dictionary to rename
dict_ptas_rename = dict([[x, x.lower().replace(" ", "_")] for x in parameter_table_additional_sectors.columns])
#set type
parameter_table_additional_sectors = parameter_table_additional_sectors.rename(columns = dict_ptas_rename)

#parameters to index
fields_add_sec_all_vals = ["strategy_id", "type", "parameter", "sector", "norm_group_id", "lever_group_id"]
#get parameter years that are defined
param_years_add_sec = [float(x) for x in parameter_table_additional_sectors.columns if x.replace(".", "").isnumeric()]
param_years_add_sec = [int(x) for x in param_years_add_sec if (int(x) == x)]
print("\n\nparam_years_add_sec:")
print(param_years_add_sec)
print(parameter_table_additional_sectors.columns)
print("\n\n")
#initialize for all parameters
all_vals_add_sec = {
    "param_years": param_years_add_sec,
    "future_id": list(range(1, n_lhs + 1)),
    "design_id": list(df_attribute_design_id["design_id"]),
    "time_series_id": list(set(df_attribute_time_series_id["time_series_id"]) & set(parameter_table_additional_sectors["time_series_id"]))
}
#sort some
all_vals_add_sec["time_series_id"].sort()

#loop
for field in fields_add_sec_all_vals:
    #set the field name
    str_field = field.lower().replace(" ", "_")
    #
    if field in ["lever_group_id", "norm_group_id"]:
        set_field = set([x for x in parameter_table_additional_sectors[field] if x > 0])
    else:
        set_field = set(parameter_table_additional_sectors[field])
    #update the dictionary
    all_vals_add_sec.update({str_field: set_field})

    
    
    
###################################
#    GENERATE ATTRIBUTE TABLES    #
###################################

###   RUN ID
df_attribute_run_id_0 = [(x, y) for x in sr.df_strat["strategy_id"] for y in ([0] + all_vals_add_sec["future_id"])]
df_attribute_run_id = pd.DataFrame(df_attribute_run_id_0)
df_attribute_run_id = df_attribute_run_id.rename(columns = {0: "strategy_id", 1: "future_id"})
df_attribute_run_id["run_id"] = range(0, len(df_attribute_run_id))
df_attribute_run_id = df_attribute_run_id[["run_id", "strategy_id", "future_id"]]

if export_ed_files_q:
	#note/export
	print("Exporting run_id attribute to " + sr.fp_csv_attribute_runs)
	df_attribute_run_id.to_csv(sr.fp_csv_attribute_runs, index = None)

###   MASTER ID
df_attribute_master_id = [[x] + [y] + list(z) for x in all_vals_add_sec["design_id"] for y in all_vals_add_sec["time_series_id"] for z in df_attribute_run_id_0]
df_attribute_master_id = pd.DataFrame(df_attribute_master_id)
df_attribute_master_id = df_attribute_master_id.rename(columns = {0: "design_id", 1: "time_series_id", 2: "strategy_id", 3: "future_id"})
fields_df_attribute_master_id = list(df_attribute_master_id.columns)
df_attribute_master_id["master_id"] = list(range(0, len(df_attribute_master_id)))
df_attribute_master_id = df_attribute_master_id[["master_id"] + fields_df_attribute_master_id]
df_attribute_master_id = pd.merge(df_attribute_master_id, df_attribute_run_id, how = "left", on = ["strategy_id", "future_id"])
#fields to order by
fields_ord_dfm = ["master_id", "design_id", "time_series_id", "run_id", "strategy_id", "future_id"]
#reorder
df_attribute_master_id = df_attribute_master_id[fields_ord_dfm].sort_values(by = fields_ord_dfm)

if export_ed_files_q:
	#note/export
	print("Exporting master_id attribute to " + sr.fp_csv_attribute_master)
	#export
	df_attribute_master_id.to_csv(sr.fp_csv_attribute_master, index = None, encoding = "UTF-8")
	#export for gams
	df_attribute_master_id_gams = df_attribute_master_id[["master_id"]].copy().rename(columns = {"master_id": "Escenarios"})
	df_attribute_master_id_gams.to_csv(sr.fp_csv_gams_data_set_escenarios, index = None, encoding = "UTF-8")
	del df_attribute_master_id_gams



#############################
#    GENERATE LHS MATRIX    #
#############################

print("Generating LHS Matrix...")
print("")
#dimensions
p_add_sec = len(all_vals_add_sec["parameter"])
n_add_sec_levers = len(all_vals_add_sec["lever_group_id"])
#generate latin hypercube sample
matrix_lhs = pyd.lhs(p_add_sec + n_add_sec_levers, samples = n_lhs)
#vector for delineating sub-matrices
vec_submat_lhs = [0, p_add_sec, n_add_sec_levers]
#set vector of submatrix index
vec_submat_lhs_names = ["add_sec", "levers"]

##  set names for additional sectors
dict_names_add_sec = [x.lower().replace(" ", "_") for x in all_vals_add_sec["parameter"]]
dict_names_add_sec.sort()
dict_names_add_sec = [[x, dict_names_add_sec[x]] for x in range(0, len(dict_names_add_sec))]
dict_names_add_sec = dict(dict_names_add_sec)

##  set names for lever groups
dict_names_levers = ["lever_group_" + str(x) for x in list(all_vals_add_sec["lever_group_id"])]
dict_names_levers = [[x, dict_names_levers[x]] for x in range(0, len(dict_names_levers))]
dict_names_levers = dict(dict_names_levers)

#initialize the fields for data frames
dict_submat_lhs_fields = {
    "add_sec": dict_names_add_sec,
    "levers": dict_names_levers
}
#setup the output file paths
dict_submat_file_paths = {
    "add_sec": sr.fp_csv_lhs_table_multi_sector,
    "levers": sr.fp_csv_lhs_table_levers
}

#initialize
dict_submat_lhs = {}
#break off components
for i in range(0, len(vec_submat_lhs) - 1):
    #set the field name for the dictionary
    nm = vec_submat_lhs_names[i]
    #check
    if i > -1:
        #get the indeces
        p0 = sum(vec_submat_lhs[0:(i + 1)])
    else:
        p0 = 0
    #set upper limit
    p1 = sum(vec_submat_lhs[0:(i + 2)])
    #temporary dataframe
    df_tmp = pd.DataFrame(matrix_lhs[:, p0:p1], index = None)
    #add name field
    if dict_submat_lhs_fields[nm] != None:
        df_tmp = df_tmp.rename(columns = dict_submat_lhs_fields[nm])
        #set names
        nms = list(df_tmp.columns)
        #add run id
        df_tmp["future_id"] = all_vals_add_sec["future_id"]
        #reorder
        df_tmp = df_tmp[["future_id"] + nms]
    #update dictionary
    dict_submat_lhs.update({nm: df_tmp})

    #export raw lhs data
    if export_ed_files_q:
		#note/export
        print("Exporting LHS for " + nm + " to " + dict_submat_file_paths[nm])
        df_tmp.to_csv(dict_submat_file_paths[nm], index = None)

##  SET SOME NAMES
fields_ed_add_sec = dict_submat_lhs["add_sec"].columns
fields_ordered_parameters = [x for x in fields_ed_add_sec if x != "future_id"]
#get parameters that are not ramped—they are constant across all years
all_constant_params = set(parameter_table_additional_sectors[parameter_table_additional_sectors["parameter_constant_q"] == 1]["parameter"])
all_constant_params = list(all_constant_params)
all_constant_params.sort()
#get indices
indices_fop_all_constant_params = [fields_ordered_parameters.index(x) for x in all_constant_params]


#################################################################
###                                                           ###
###    GENERATE EXPERIMENTAL DESIGN FOR ADDITIONAL SECTORS    ###
###                                                           ###
#################################################################

###############################
#    GENERATE LEVER DELTAS    #
###############################

print("Starting generation of lever deltas.")
print("")
##  START BUY BUILDING LONG TABLE OF TRANSFORMED LHS SAMPLES

dsl = dict_submat_lhs["levers"].copy()
dsl = pd.wide_to_long(dsl, i = ["future_id"], j = "lever_group_id", stubnames = "lever_group_")
dsl = dsl.reset_index()
dsl = dsl.rename(columns = {"lever_group_": "lhs_val"})
#data frame out
df_ld_lhs_transformed = []
#loop over design id
for did in all_vals_add_sec["design_id"]:
    #get applicable data
    dict_data = df_attribute_design_id[df_attribute_design_id["design_id"] == did].to_dict()
    #initialize
    lhs_out = dsl.copy()
    #get key for to_dict
    key = list(dict_data["vary_lever_deltas"].keys())[0]
    #get range of values
    vec_vals = np.array(lhs_out["lhs_val"])
    #set header for Future 0
    df_fut_0 = pd.DataFrame([[did, 0, x, 1] for x in all_vals_add_sec["lever_group_id"]], columns = ["design_id", "future_id", "lever_group_id", "lhs_val"])
    #check on varying
    if dict_data["vary_lever_deltas"][key] == 1:
        #transform
        m = float(dict_data["linear_transform_ld_m"][key])
        b = float(dict_data["linear_transform_ld_b"][key])
        #thresholds
        thresh_min = float(dict_data["min_lever_deltas"][key])
        thresh_max = float(dict_data["max_lever_deltas"][key])
        #transformation
        def linear_transform(x):
            return max(min(m*x + b, thresh_max), thresh_min)
        #updated vals
        vec_vals = list(map(linear_transform, vec_vals))
    else:
        #set the deltas to 1
        vec_vals = [1.0 for x in range(len(vec_vals))]
    #update in data frames
    lhs_out["lhs_val"] = vec_vals
    lhs_out["design_id"] = [did for x in range(len(vec_vals))]
    #update
    lhs_out = pd.concat([df_fut_0, lhs_out[["design_id", "future_id", "lever_group_id", "lhs_val"]]])
    #add
    df_ld_lhs_transformed = df_ld_lhs_transformed + [lhs_out]
#convert to dataframee
df_ld_lhs_transformed = pd.concat(df_ld_lhs_transformed)


##  THEN, GO BY STRATEGY TO BUILD DELTAS

print("Starting build of deltas by time series/strategy...")
print("")
#set strategies to build deltas for
strat_lever_deltas = [x for x in all_vals_add_sec["strategy_id"] if x != strat_baseline]
#temporary reduction
ptas_ld = parameter_table_additional_sectors[parameter_table_additional_sectors["lever_group_id"] > 0]

#merge field for generate lever deltas
fields_merge_ld = ["variable_name_lower", "lever_group_id"]
#set extraction fields by type
extraction_fields_ld = fields_merge_ld + [str(x) for x in param_years_add_sec]

#dictionary of lever deltas by strategy
dict_ld = {}
#fields to extract and use in transpose
fields_ext_ld = fields_ordered_parameters
#initialize
df_ld_shaped = []
#loop over time series ids
for ts_id in all_vals_add_sec["time_series_id"]:
	#get baseline data frame
	df_base = ptas_ld[(ptas_ld["strategy_id"] == strat_baseline) & (ptas_ld["time_series_id"] == ts_id)].copy()
	#reduce
	df_base = df_base[extraction_fields_ld]
	
	#loop over strategies to generate lever deltas by included years
	for strat in strat_lever_deltas:
		#get strategy id
		strat_id = int(strat)#int(sr.dict_strat_ids[strat])
		#get sub data frame
		df_strat = ptas_ld[(ptas_ld["strategy_id"] == strat) & (ptas_ld["time_series_id"] == ts_id)].copy()
		df_strat = df_strat[extraction_fields_ld]
		#data fields
		fields_data = [x for x in extraction_fields_ld if (x not in fields_merge_ld)]
		#get column rename
		dict_rename_df_strat = dict([[str(x), str(strat) + "_" + str(x)] for x in fields_data])
		#update
		df_strat = df_strat.rename(columns = dict_rename_df_strat)
		#merge in
		df_strat = pd.merge(df_strat, df_base, how = "inner", left_on = fields_merge_ld, right_on = fields_merge_ld)
		#set new lever delta fields
		fields_ld = []
		#generate subtraction
		for fd in fields_data:
			field_0 = fd
			field_s = str(strat) + "_" + str(fd)
			field_ld = "ld_" + field_s
			fields_ld = fields_ld + [field_ld]
			#parse out and get difference
			df_strat_tmp = df_strat[[field_0, field_s]].diff(axis = 1)
			#update
			df_strat[field_ld] = df_strat_tmp[field_s]
		#reduce
		df_strat = df_strat[fields_merge_ld + fields_ld]
		#merge in
		df_strat = pd.merge(df_strat, df_ld_lhs_transformed, how = "outer", left_on = ["lever_group_id"], right_on = ["lever_group_id"])
		#build new data
		df_deltas_adj = (np.array(df_strat[fields_ld]).transpose() * np.array(df_strat["lhs_val"])).transpose()
		df_deltas_adj = pd.DataFrame(df_deltas_adj, columns = fields_ld)
		#re-initialize
		df_strat = df_strat[["design_id", "future_id"] + fields_merge_ld]
		df_strat = pd.concat([df_strat, df_deltas_adj], axis = 1, sort = False)
		#update
		dict_ld.update({strat: df_strat})
		
		# BUILD RESHAPED VALUE
		
		#loop over design/future
		for did in list(df_strat["design_id"].unique()):
			for fut in list(df_strat["future_id"].unique()):
				df_tmp = df_strat[(df_strat["design_id"] == did) & (df_strat["future_id"] == fut)].copy()
				df_tmp = df_tmp[["variable_name_lower"] + fields_ld]
				#fields to add
				fields_new = list(df_tmp["variable_name_lower"])
				#new data frame
				df_tmp = pd.DataFrame(np.array(df_tmp[fields_ld]).transpose(), columns = fields_new)
				#add year
				df_tmp["year"] = param_years_add_sec
				#add design id and future
				df_tmp["design_id"] = [did for x in range(len(df_tmp))]
				df_tmp["future_id"] = [fut for x in range(len(df_tmp))]
				df_tmp["strategy_id"] = [strat_id for x in range(len(df_tmp))]
				df_tmp["time_series_id"] = [ts_id for x in range(len(df_tmp))]
				#order
				df_tmp = df_tmp[["design_id", "time_series_id", "strategy_id", "future_id", "year"] + fields_new]
				#update
				df_ld_shaped = df_ld_shaped + [df_tmp]
			#notify of completed reshape
			print("Reshaping of LHS table complete for design_id: " + str(did) + ", time_series_id: " + str(ts_id) + ", strategy_id: " + str(strat))

if len(df_ld_shaped) > 0:
	#convert to wide frame
	df_ld_shaped = pd.concat(df_ld_shaped)
	#rename
	df_ld_shaped = df_ld_shaped.rename(columns = dict([[x, "ld_" + x] for x in fields_new]))
    
    
##  CREATE RAMP VECTORS FOR UNCERTAINTY

y_0 = int(sr.dict_init["add_sec_variation_start_year"]) - 1
y_1 = max(param_years_add_sec)
y_base = min(param_years_add_sec)
vec_ramp_unc = sr.build_linear_mix_vec((y_0, y_1), (y_base, y_1))
#sr.build_mix_vec(0, 0, 0, "linear")#np.array([max(min((y - y_0)/(y_1 - y_0), 1), 0) for y in param_years_add_sec])
vec_ramp_base = 1 - vec_ramp_unc


##  BUILD BASIC PERCENTAGE CHANGE MATRIX


#for ts_id in all_vals_add_sec["time_series_id"]:
df_ed_baseline = parameter_table_additional_sectors[(parameter_table_additional_sectors["strategy_id"] == strat_baseline) & (parameter_table_additional_sectors["time_series_id"] == 0)].copy()
df_ed_base = df_ed_baseline[extraction_fields_ld].copy()
df_ed_add_sec = dict_submat_lhs["add_sec"]
#initialize array (in order of ext fields)
array_ed_add_sec = np.array(df_ed_add_sec[fields_ordered_parameters])
#order output array
df_max_min = pd.merge(pd.DataFrame(fields_ordered_parameters, columns = ["variable_name_lower"]), df_ed_baseline[["variable_name_lower", "min_2050", "max_2050"]], how = "left", left_on = ["variable_name_lower"], right_on = ["variable_name_lower"])
#generate transformed values of uncertainty
array_ed_add_sec_trans = array_ed_add_sec * np.array(df_max_min["max_2050"]) + (1 - array_ed_add_sec) * np.array(df_max_min["min_2050"])
#add in future 0 (0 change = 100%)
array_ed_add_sec_trans = np.concatenate([np.ones((1, array_ed_add_sec_trans.shape[1])), array_ed_add_sec_trans])
#set data frame of baseline percentage changes
df_perc_change_unc = []
#build outcome matrix
for i in range(len(param_years_add_sec)):
	y = param_years_add_sec[i]
	frac_base = vec_ramp_base[i]
	frac_unc = vec_ramp_unc[i]
	#build weighted array
	array_tmp = np.ones(array_ed_add_sec_trans.shape)*(frac_base) + array_ed_add_sec_trans*(frac_unc)
	#NOTE: FOR CONSTANT PARAMS, GET RID OF "RAMP"
	array_tmp[:, indices_fop_all_constant_params] = array_ed_add_sec_trans[:, indices_fop_all_constant_params].copy()
	#convert to data frame
	df_tmp = pd.DataFrame(array_tmp, columns = fields_ordered_parameters)
	#add year
	df_tmp["year"] = [int(y) for x in range(len(df_tmp))]
	df_tmp["future_id"] = [0] + list(df_ed_add_sec["future_id"])
	#df_tmp["time_series_id"] = [ts_id for x in range(len(df_tmp))]
	#organize
	df_tmp = df_tmp[["future_id", "year"] + fields_ordered_parameters]
	#update
	df_perc_change_unc = df_perc_change_unc + [df_tmp]
#build master
df_perc_change_unc = pd.concat(df_perc_change_unc)
df_perc_change_unc = df_perc_change_unc.sort_values(by = ["future_id", "year"])


##  BUILD DATA FRAME BASIS FOR EXPERIMENTAL DESIGN FILE

print("Building data frame basis for experimental design file...")
print("")

if len(df_ld_shaped) > 0:
	#fields that are in the LD matrix
	fields_ld_data = [x for x in df_ld_shaped.columns if (x.replace("ld_", "") in fields_ordered_parameters)]
	
	#print("\n"*8 + "#"*30)
	#print("\nSUCCESS\n\n")
	#print(df_ld_shaped)
	#print("\n\n" + "#"*30 + "\n"*8)
else:
	fields_ld_data = []
fields_ldparams_data = [x.replace("ld_", "") for x in fields_ld_data]
fields_nonldparams_data = [x for x in fields_ordered_parameters if (x not in fields_ldparams_data)]
#initialize output data frame
df_out = []
#loop over time series
for ts_id in all_vals_add_sec["time_series_id"]:
	#get baseline for each time series
	df_ed_baseline = parameter_table_additional_sectors[(parameter_table_additional_sectors["strategy_id"] == strat_baseline) & (parameter_table_additional_sectors["time_series_id"] == ts_id)].copy()
	df_ed_base = df_ed_baseline[extraction_fields_ld].copy()
	#set column headers
	fields_df_ed = list(df_ed_base["variable_name_lower"])
	df_ed_base = df_ed_base.transpose().loc[[str(x) for x in param_years_add_sec],:]
	df_ed_base = df_ed_base.rename(columns = dict([[list(df_ed_base.columns)[x], fields_df_ed[x]] for x in range(len(fields_df_ed))]))
	df_ed_base["year"] = [int(x) for x in df_ed_base.index]
	
	#loop over design ids
	for did in all_vals_add_sec["design_id"]:
		#get applicable data
		dict_data = df_attribute_design_id[df_attribute_design_id["design_id"] == did].to_dict()
		#get key for to_dict
		key = list(dict_data["vary_lever_deltas"].keys())[0]
		#experimental design merge table
		df_ed_merge = df_attribute_master_id[(df_attribute_master_id["time_series_id"] == ts_id) & (df_attribute_master_id["design_id"] == did)]
		list_ed_merge = []
		cols = [x for x in df_ed_merge.columns] + ["year"]
		for y in param_years_add_sec:
			df_tmp = df_ed_merge.copy()
			df_tmp["year"] = [int(y) for x in range(len(df_tmp))]
			df_tmp = df_tmp[cols]
			list_ed_merge = list_ed_merge + [df_tmp]
		#convert
		df_ed_merge = pd.concat(list_ed_merge)
        #add in
		df_ed_merge = pd.merge(df_ed_merge, df_ed_base, how = "outer", left_on = ["year"], right_on = ["year"])
        #renaming dictionary
		dict_rnm = dict([x, "perc_" + x] for x in fields_ordered_parameters)
        #breakout fields
		fields_percs = [dict_rnm[x] for x in fields_ordered_parameters]
            
        #check if percentages need to be accounted for
		if dict_data["vary_uncertainties"][key] == 1:
			df_tmp = df_perc_change_unc
			#rename to columns
			df_tmp = df_tmp.rename(columns = dict([x, "perc_" + x] for x in fields_ordered_parameters))
			df_ed_merge = pd.merge(df_ed_merge, df_tmp, how = "left", left_on = ["future_id", "year"], right_on = ["future_id", "year"])
			#id fields to breakout on
			fields_id = [x for x in df_ed_merge.columns if (x not in fields_percs) and (x not in fields_ordered_parameters)]
			#seprate out
			df_ed_merge_ids = df_ed_merge[fields_id]
			#convert to product array—has headers fields_ordered_parameters
			array_design = np.array(df_ed_merge[fields_percs]) * np.array(df_ed_merge[fields_ordered_parameters])
		else:
			#id fields to breakout on
			fields_id = [x for x in df_ed_merge.columns if (x not in fields_ordered_parameters)]
			#seprate out
			df_ed_merge_ids = df_ed_merge[fields_id]
			#reduce the design
			array_design = np.array(df_ed_merge[fields_ordered_parameters])
		#update
		df_ed_merge = pd.concat([df_ed_merge_ids, pd.DataFrame(array_design, columns = fields_ordered_parameters)], axis = 1, sort = False)
		
		#check if lever delta needs to be brought in
		#if dict_data["vary_lever_deltas"][key] == 1:
		
		# ADD IN LEVER DELTAS
		
		if len(df_ld_shaped) > 0:
			#fields to merge on
			fields_merge_ld = list(set(df_ed_merge.columns) & set(df_ld_shaped.columns))
		else:
			fields_merge_ld = []
			
		if len(fields_merge_ld) > 0:
			#merge in lever deltas
			df_ed_merge = pd.merge(df_ed_merge, df_ld_shaped, how = "left", left_on = fields_merge_ld, right_on = fields_merge_ld)
		#split out
		df_ed_merge_ids = df_ed_merge[fields_id + fields_nonldparams_data]
		#add in lever deltas
		array_design = np.array(df_ed_merge[fields_ldparams_data]) + np.array(np.array(df_ed_merge[fields_ld_data].fillna(0)))
		#concatenate
		df_ed_merge = pd.concat([df_ed_merge_ids, pd.DataFrame(array_design, columns = fields_ldparams_data)], axis = 1, sort = False)
		
		#reduce
		df_ed_merge = df_ed_merge[df_ed_merge["strategy_id"].isin(all_vals_add_sec["strategy_id"])]
		#sort
		df_ed_merge = df_ed_merge.sort_values(by = ["master_id", "year"])
		#clear index
		df_ed_merge = df_ed_merge.reset_index(drop = True)
		#order
		df_ed_merge = df_ed_merge[fields_id + fields_ordered_parameters]

		if len(df_out) == 0:
			#add to output list
			df_out = df_out + [df_ed_merge]
		else:
			df_out = df_out + [df_ed_merge[df_out[0].columns]]
		
		print("Data frame for time_series_id: " + str(ts_id) + ", design_id: " + str(did) + " complete.")
		print("")
#build output dataframe
df_out = pd.concat(df_out, axis = 0)
#set ordering
fields_id = [x for x in df_out.columns if "_id" in x]
fields_dat = [x for x in df_out.columns if (x not in (fields_id + ["year"]))]
df_out = df_out[fields_id + ["year"] + fields_dat]

#
cols_to_export = []
#loop over columns to check values (this is inefficient)
for col in df_out.columns:
	if "_id" not in col:
		if len(set(df_out[col].unique())) == 1:
			cols_to_export.append(col)
#convert to single values
df_out_singles = df_out[cols_to_export].drop_duplicates()
#reduce
df_out = df_out[[x for x in df_out.columns if x not in cols_to_export]]



#################################################################################################
###                                                                                           ###
###    DO MIXING TRACJETORIES FOR THOSE SPECIFIED WITH "trajmax", "trajmin", and "trajmix"    ###
###                                                                                           ###
#################################################################################################

#get string identifier
substr_max = "trajmax"
substr_min = "trajmin"
substr_mix = "trajmix"
#get parameters that should be mixed
params_mix_loop = [x.replace(substr_mix + "_", "") for x in df_out.columns if (x[0:min(len(x), len(substr_mix))] == substr_mix)]
#some notifcation
print("\nparams_mix_loop:\n")
print(("\t%s\n"*len(params_mix_loop))%tuple(params_mix_loop))
print("\n")

#parameters to eliminate
fields_drop = []

#loop over parameters to ensure all required fields are available; if present, calculate new field
for x in params_mix_loop:
	x_max = (substr_max + "_" + x)
	x_min = (substr_min + "_" + x)
	x_mix = (substr_mix + "_" + x)
	#add to fields to eliminate
	fields_drop = fields_drop + [x_max, x_min, x_mix]
	#get veector of mixing fractions
	vec_mix = np.array(df_out[x_mix])
	#default to both existing
	max_q = True
	min_q = True
	#parameters not found
	missing_params = []
	
	#get upper bound trajectory
	if (x_max in df_out.columns):
		traj_max = np.array(df_out[x_max])
	elif (x_max in df_out_singles.columns):
		traj_max = float(df_out_singles[x_max].iloc[0])
	else:
		max_q = False
		missing_params = missing_params + [x_max]
		
	#get lower bound trajectory
	if (x_min in df_out.columns):
		traj_min = np.array(df_out[x_min])
	elif (x_min in df_out_singles.columns):
		traj_min = float(df_out_singles[x_min].iloc[0])
	else:
		min_q = False
		missing_params = missing_params + [x_min]
	
	#build data frame
	if min_q & max_q:
		#get min/max trajectories, build new parameter
		df_out[x] = traj_max*vec_mix + traj_min*(1 - vec_mix)
	else:
		#params not found
		print("\nDropping " + x + " from df_out:\n" + ("\tParameter '%s' not found.\n"*len(missing_params))%tuple(missing_params) + "\n")

#reduce df_out
df_out = df_out[[x for x in df_out.columns if (x not in fields_drop)]]





######################################
###                                ###
###    GENERATE GDP GROWTH RATE    ###
###                                ###
######################################

print("\nBuilding growth rate...")
#get gdp and years
pib = np.array(df_out["pib"])
yrs = np.array(df_out["year"])

#get differences to use to take as root of growth rate
yr_diff = yrs[1:] - yrs[0:(len(yrs) - 1)]
#get growth rate in pib
gr_pib_raw = pib[1:]/pib[0:(len(pib) - 1)] - 1
#set the exponents
vec_exp = np.array([max(1/x, 1) for x in yr_diff])
gr_pib = gr_pib_raw**vec_exp
#get position of negative elements
ind_new_years = [i for i, x in enumerate(yr_diff) if x == min(yr_diff)]
ind_new_years_ext = [i + 1 for i in ind_new_years]
#update
np.put(gr_pib, ind_new_years, gr_pib_raw[ind_new_years_ext])
#add initial growth rate
gr_pib = np.concatenate([np.array([gr_pib[0]]), gr_pib])
#add to output dataframe
df_out["gr_pib"] = gr_pib

print("Growth rate complete.\n")





###############################
###                         ###
###    EXPORT GAMS FILES    ###
###                         ###
###############################

##  PRICE AND INVESTMENT COST

#set ids for different data frames
dict_dfs_exp = {
    "inversion": {"substr": "investment", "exp_path": sr.fp_csv_gams_data_costo_inversion_procesos_escenarios},
    "precio": {"substr": "fuel_price", "exp_path": sr.fp_csv_gams_data_precio_energeticos_escenarios}
}
#loop
for k in list(dict_dfs_exp.keys()):
    #get substring id
    substr_id = str(dict_dfs_exp[k]["substr"])
    #get sub data frame
    df_sub = df_out[["master_id", "year"] + [x for x in df_out.columns if (x in sr.dict_map_params_to_params_gams.keys()) and (x[0:min(len(x), len(substr_id))] == substr_id)]].copy()
    #rename
    df_sub = df_sub.rename(columns = sr.dict_map_params_to_params_gams)
    #conver to long and rename
    df_sub = pd.melt(df_sub, ["master_id", "year"]).rename(columns = {"master_id": "Escenario", "year": "Agno", "variable": "Energeticos", "value": "Precio"})
    #notify
    print("Exporting GAMS " + str(k) + " file to: " + dict_dfs_exp[k]["exp_path"] + "...\n")
    #export
    df_sub.to_csv(dict_dfs_exp[k]["exp_path"], encoding = "UTF-8", index = None)


##  HYDROLOGICAL

# Read data hydrology indices from pmr data input
df_data_hydro = pd.read_csv(sr.fp_csv_gams_data_hidrologias)
#sort to ensure we can just take highest row that is less than or equal to prob
df_data_hydro = df_data_hydro.sort_values(by = ["Probabilidad_Excedencia"]).reset_index(drop = True)
#hydrologies from the experimental design
df_ed_hyd = df_out[df_out["year"] == 2050][["master_id", "hydrology_exceedance_probability"]].copy().reset_index(drop = True)
#initialize
hydrological_scenarios = np.zeros(len(df_ed_hyd)).astype(int)
#loop to overwrite the scenarios
for i in range(len(df_ed_hyd)):
    prob = float(df_ed_hyd["hydrology_exceedance_probability"].iloc[i])
    tmp = np.where(df_data_hydro["Probabilidad_Excedencia"] >= prob)
    #get the associated hydro id
    hydro_id = int(df_data_hydro["ID_Hidro"].iloc[min(tmp[0])])
    #overwrite
    hydrological_scenarios[i] = hydro_id
#add to data frame
df_ed_hyd["Escenario_Hidrologico"] = hydrological_scenarios
df_ed_hyd = df_ed_hyd[["master_id", "Escenario_Hidrologico"]].rename(columns = {"master_id": "Escenario"})
#notify
print("Exporting GAMS hydrology file to: " + sr.fp_csv_gams_data_hidrologias_escenarios + "...\n")
#export data to data_input
df_ed_hyd.to_csv(sr.fp_csv_gams_data_hidrologias_escenarios, index = False, encoding = "UTF-8")






###################################
###                             ###
###    BUILD DIFFERENCE FILE    ###
###                             ###
###################################

print("Building experimental design difference file...")
#build difference file
exp_design_diff = sr.do_df_diff(df_out, df_attribute_master_id, [], "year")
#update run id to integer
exp_design_diff["run_id"] = np.array(exp_design_diff["run_id"]).astype(int)


#write output
if export_ed_files_q:
	print("Writing output to " + sr.fp_csv_experimental_design_msec + "...")
	print("")
	#note/export
	print("Exporting additional sectors experimental design to " + sr.fp_csv_experimental_design_msec)
	#export experimental design and associated files
	df_out.to_csv(sr.fp_csv_experimental_design_msec, index = None)
	df_out_singles.to_csv(sr.fp_csv_experimental_design_msec_single_vals, index = None)
	exp_design_diff.to_csv(sr.fp_csv_experimental_design_msec_diff, index = None)
	#reduce and write to table for parameter values of interest
	ed = df_out[(df_out["time_series_id"] == 0) & (df_out["year"].isin([min(sr.output_model_years), max(sr.output_model_years)])) & (df_out["future_id"] == 0) & (df_out["design_id"] == 0)]
	ed = ed.transpose().reset_index(drop = False).rename(columns = {"index": "parameter"})



	##  DEFAULT SET TO RUN
	
	df_master_exp = pd.concat([
		#design 0
		df_attribute_master_id[(df_attribute_master_id["design_id"] == 0) & (df_attribute_master_id["strategy_id"] > 0)],
		#design 1
		df_attribute_master_id[(df_attribute_master_id["design_id"] == 1) & (df_attribute_master_id["strategy_id"] > 0)]
	])
	
	#temp overwrite
	df_master_exp = df_attribute_master_id[(df_attribute_master_id["design_id"] == 0)]
	#set gams vals
	df_master_exp_gams = df_master_exp[df_master_exp["strategy_id"] > 0]
	#export
	df_master_exp[["master_id"]].to_csv(sr.fp_csv_experimental_design_msec_masters_to_run, index = None, encoding = "UTF-8")
	df_master_exp_gams[["master_id"]].to_csv(sr.fp_csv_experimental_design_msec_masters_to_run_gams, index = None, encoding = "UTF-8")



######################################################################
###                                                                ###
###    BUILD CHANGE FACTORS FILE FOR FILLING OUT DECARB_DRIVERS    ###
###                                                                ###
######################################################################

#############################
#    PROPORTIONAL CHANGE    #
#############################

print("Starting export of proportional change ranges file to " + sr.fp_csv_ranges_for_decarb_drivers)
if False:
	#add in special fields
	df_out["households"] = np.round(np.array(df_out["total_population"]).astype(float)/np.array(df_out["occ_rate"]).astype(float)).astype(int)
	#set
	fields_append = set({"households"})
else:
	fields_append = set({})
#fields id
fields_id = [x for x in df_out.columns if "_id" in x or x == "year"]
fields_data = [x for x in df_out.columns if x not in fields_id]
#get baseline vector
vec_base = np.array(df_out[(df_out["master_id"] == 0) & (df_out["year"] == 2015)][fields_data])[0]
vec_base[np.where(vec_base == 0)] = np.nan
#last year
df_futs_ly = df_out[(df_out["year"] == 2050) & (df_out["design_id"] == 1)].copy().reset_index(drop = True)
#get array that divides
array_futs = np.array(df_futs_ly[fields_data])/vec_base - 1
#convert to data frame
df_futs = pd.concat([df_futs_ly[fields_id], pd.DataFrame(array_futs, columns = fields_data)], axis = 1)
#get nominal
df_futs_nom = df_futs[(df_futs["future_id"] == 0) & (df_futs["time_series_id"] == 0)]

#columns to keep
fields_keep = ["strategy_id"] + fields_data#[x for x in df_futs.columns if x not in ["master_id", "run_id", "Design." "future_id"]]


##  NOMINAL

df_futs_nom = df_futs_nom[fields_keep]
#add in id column
df_futs_nom["metric_type"] = ["nominal" for x in range(len(df_futs_nom))]
df_futs_nom["metric_ord"] = [0 for x in range(len(df_futs_nom))]

##  MIN

#get column agg dictionary
dict_agg = dict([[x, "min"] for x in df_futs.columns])
#gt minimum data frame
df_futs_min = df_futs.groupby(["strategy_id"]).agg(dict_agg)
df_futs_min = df_futs_min[fields_keep].reset_index(drop = True)
#add in id column
df_futs_min["metric_type"] = ["min" for x in range(len(df_futs_min))]
df_futs_min["metric_ord"] = [1 for x in range(len(df_futs_min))]


##  MAX

#get column agg dictionary
dict_agg = dict([[x, "max"] for x in df_futs.columns])
#gt minimum data frame
df_futs_max = df_futs.groupby(["strategy_id"]).agg(dict_agg)
df_futs_max = df_futs_max[fields_keep].reset_index(drop = True)
#add in id column
df_futs_max["metric_type"] = ["max" for x in range(len(df_futs_max))]
df_futs_max["metric_ord"] = [2 for x in range(len(df_futs_max))]


##  JOIN

#ordering fields
fields_ord = ["strategy_id", "metric_type", "metric_ord"] + fields_data
#join
df_ed_xl_ranges = pd.concat([df_futs_nom[fields_ord], df_futs_min[fields_ord], df_futs_max[fields_ord]], axis = 0)

#order
df_ed_xl_ranges = df_ed_xl_ranges.sort_values(by = ["strategy_id", "metric_ord"]).reset_index(drop = True)
df_ed_xl_ranges = df_ed_xl_ranges[["strategy_id", "metric_type"] + fields_data]
df_ed_xl_ranges = df_ed_xl_ranges.transpose().reset_index().rename(columns = {"index": "field"})

#new names
dict_new_names = {}
#rows
row_strat = df_ed_xl_ranges[df_ed_xl_ranges["field"] == "strategy_id"]
row_met = df_ed_xl_ranges[df_ed_xl_ranges["field"] == "metric_type"]
#parameters to keep
set_keep_params = set(fields_data) | fields_append
#loop
for i in [x for x in df_ed_xl_ranges.columns if x != "field"]:
    #get vals from rows
    st = sr.dict_strat_id_to_strat[int(row_strat[i].iloc[0])]
    met = str(row_met[i].iloc[0])
    field_new = st + "_" + met
    #update
    dict_new_names.update({i: field_new})
#rename and reduce
df_ed_xl_ranges = df_ed_xl_ranges[df_ed_xl_ranges["field"].isin(set_keep_params)].rename(columns = dict_new_names)
#write output
df_ed_xl_ranges.to_csv(sr.fp_csv_ranges_for_decarb_drivers, index = None)



#####################
#    REAL VALUES    #
#####################

#get vals for everything non zero
df_futs_lynz = df_futs_ly[df_futs_ly["future_id"] > 0].copy()
df_futs_lyz = df_futs_ly[(df_futs_ly["future_id"] == 0) & (df_futs_ly["time_series_id"] == 0)].copy()

##  2015 BASE

df_base_2015 = df_out[(df_out["master_id"] == 0) & (df_out["year"] == 2015)][fields_keep].copy()
#add in the id columns
df_base_2015["metric_type"] = ["base" for x in range(len(df_base_2015))]
df_base_2015["metric_ord"] = [0 for x in range(len(df_base_2015))]


##  NOMINAL

#add in id column
df_futs_lyz["metric_type"] = ["nominal" for x in range(len(df_futs_lyz))]
df_futs_lyz["metric_ord"] = [0 for x in range(len(df_futs_lyz))]


##  MIN

#get column agg dictionary
dict_agg = dict([[x, "min"] for x in df_futs_lynz.columns])
#gt minimum data frame
df_futs_lynz_min = df_futs_lynz.groupby(["strategy_id"]).agg(dict_agg)
df_futs_lynz_min = df_futs_lynz_min[fields_keep].reset_index(drop = True)
#add in id column
df_futs_lynz_min["metric_type"] = ["min" for x in range(len(df_futs_lynz_min))]
df_futs_lynz_min["metric_ord"] = [1 for x in range(len(df_futs_lynz_min))]


##  MAX

#get column agg dictionary
dict_agg = dict([[x, "max"] for x in df_futs_lynz.columns])
#gt minimum data frame
df_futs_lynz_max = df_futs_lynz.groupby(["strategy_id"]).agg(dict_agg)
df_futs_lynz_max = df_futs_lynz_max[fields_keep].reset_index(drop = True)
#add in id column
df_futs_lynz_max["metric_type"] = ["max" for x in range(len(df_futs_lynz_max))]
df_futs_lynz_max["metric_ord"] = [2 for x in range(len(df_futs_lynz_max))]


##  JOIN

#ordering fields
fields_ord = ["strategy_id", "metric_type", "metric_ord"] + fields_data
#join
df_ed_xl_ranges_vals = pd.concat([df_base_2015[fields_ord], df_futs_lyz[fields_ord], df_futs_lynz_min[fields_ord], df_futs_lynz_max[fields_ord]], axis = 0)
#order
df_ed_xl_ranges_vals = df_ed_xl_ranges_vals.sort_values(by = ["strategy_id", "metric_ord"]).reset_index(drop = True)
df_ed_xl_ranges_vals = df_ed_xl_ranges_vals[["strategy_id", "metric_type"] + fields_data]
df_ed_xl_ranges_vals = df_ed_xl_ranges_vals.transpose().reset_index().rename(columns = {"index": "field"})

#new names
dict_new_names = {}
#rows
row_strat = df_ed_xl_ranges_vals[df_ed_xl_ranges_vals["field"] == "strategy_id"]
row_met = df_ed_xl_ranges_vals[df_ed_xl_ranges_vals["field"] == "metric_type"]
#parameters to keep
set_keep_params = set(fields_data) | fields_append
#loop
for i in [x for x in df_ed_xl_ranges_vals.columns if x != "field"]:
    #get vals from rows
    st = sr.dict_strat_id_to_strat[int(row_strat[i].iloc[0])]
    met = str(row_met[i].iloc[0])
    field_new = st + "_" + met
    #update
    dict_new_names.update({i: field_new})
#rename and reduce
df_ed_xl_ranges_vals = df_ed_xl_ranges_vals[df_ed_xl_ranges_vals["field"].isin(set_keep_params)].rename(columns = dict_new_names)


##  APPEND SOME AGGREGATE INFO

fields_ord_out = list(df_ed_xl_ranges_vals.columns)
#classify
all_crops_perm = ["bananas", "coffee", "fruits", "pina", "palm_oil"]
all_crops_ann = ["others", "rice", "sugar_cane", "vegetables"]
#string ids for agg
dict_str_ids = {
    "crops": "_yield_tonnes_ha",
    "crops_annual": all_crops_ann,
    "crops_perennial": all_crops_perm,
    "forest": "_conv_to_cropland_area_ha",
    "forest_primary": "_primary_forest_conv_to_cropland_area_ha",
    "forest_secondary": "_secondary_forest_conv_to_cropland_area_ha"
}
dict_all = {}
df_append = [df_ed_xl_ranges_vals]
for nm in dict_str_ids.keys():
    if type(dict_str_ids[nm]) == str:
        all_vals = list(set([x.replace(dict_str_ids[nm], "") for x in df_ed_xl_ranges_vals["field"] if dict_str_ids[nm] in x]))
        #add back in
        if nm in ["forest_primary", "forest_secondary"]:
            #string appendage
            str_append = nm.replace("forest_", "") + "_forest"
            all_vals = [(x + "_" + str_append) for x in all_vals]
        all_vals.sort()
    else:
        all_vals = dict_str_ids[nm]
    #add to dictionary
    dict_all.update({nm: all_vals})
    #add land use
    all_vals = ["frac_lu_" + x for x in all_vals]
    #get subdf
    df_sub = df_ed_xl_ranges_vals[df_ed_xl_ranges_vals["field"].isin(all_vals)]
    #fields to extract
    fields_ext = [x for x in df_sub.columns if x != "field"]
    
    if len(df_sub) > 0:
    	#array
    	array_sub = (sum(np.array(df_sub[fields_ext]))*sr.area_cr).astype(int)
    	#update
    	df_sub = pd.concat([pd.DataFrame({"field": [nm]}), pd.DataFrame([array_sub], columns = fields_ext)], axis = 1)
    #append
    df_append.append(df_sub[fields_ord_out])
df_ed_xl_ranges_vals_full = pd.concat(df_append, axis = 0)


##  WRITE OUTPUT
df_ed_xl_ranges_vals.to_csv(sr.fp_csv_ranges_vals_for_decarb_drivers, index = None)


#notify
print("Export of ranges files complete.")


###
#
###

#copy to windows directory
if sr.integrate_analytica_q:
	#check system
	if sr.analytical_platform == "unix":
		#set files to copy
		dict_files_copy = {
			sr.dir_ed_ade: [
				sr.fp_csv_attribute_master,
				sr.fp_csv_experimental_design_msec,
				sr.fp_csv_experimental_design_msec_single_vals,
				sr.fp_csv_experimental_design_msec_masters_to_run
			],
			
			sr.dir_ref_ade: [
				sr.fp_csv_attribute_pyparams
			]
		}
		
		
		#copy over
		for dc in dict_files_copy.keys():
			#get files to copy
			files_copy = dict_files_copy[dc]
			
			print("Copying files to Parallels at " + dc + " :")
			
			for fc in files_copy:
				fn = os.path.basename(fc)
				fp_new = os.path.join(dc, fn)
				#copy over
				cmd_cp = "cp \"" + fc + "\" \"" + fp_new + "\""
				#execute
				os.system(cmd_cp)
				#noftify
				print("\t\nCopied " + fc + " to " + fp_new)
			
			print("")
			
		print("Copying complete.")
			

print("Analytica done.")



print("Experimental design generation complete.")

    
    
     
    



    
    


    


