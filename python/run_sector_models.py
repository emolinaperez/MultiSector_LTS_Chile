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

#read in baseline waste data
df_waste_baseline = pd.read_csv(sr.fp_csv_waste_baseline_data)
#adjust
df_waste_baseline["total_population"] = np.array(df_waste_baseline["poblacion_milliones"]*(10**6)).astype(int)
df_waste_baseline["va_industry"] = df_waste_baseline["gdp_ind"]
#remove
df_waste_baseline = df_waste_baseline[[x for x in df_waste_baseline.columns if x not in ["poblacion_miliones", "gdp_ind"]]]

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
#fields used to join baseline waste data (pre-2015) with future scenarios for SDRD projections
fields_waste_sdrd = [x for x in df_waste_baseline.columns if (x in exp_design_cols)]
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

#reduce baseline waste data file
df_waste_baseline = df_waste_baseline[df_waste_baseline["year"] < min(model_years)]
#fields to use for merging in sector data frames
fields_id_for_df_merges = ["master_id", "year"]




################################
###                          ###
###    ENERGY & BUILDINGS    ###
###                          ###
################################

print("Building buildings results...")
# RUN MODEL
df_buildings = sm.sm_buildings(exp_design)
df_buildings = pd.DataFrame(df_buildings)
#fields to add to extraction (also for ordering)
fields_df_bui = list(df_buildings.columns)
#loop
for field in fields_id_for_df_merges:
	df_buildings[field] = np.array(exp_design[field])
df_buildings = df_buildings[fields_id_for_df_merges + fields_df_bui]




################################
###                          ###
###    INDUSTRIAL PROCESS    ###
###                          ###
################################

print("Building industrial results...")
#map product to field to use
dict_gdp_field = {
    "cal": "va_ccv_ind",
    "cemento": "va_ccv_ind",
    "vidrio": "va_manufacturing",
    "carburo": "va_manufacturing",
    "industry_at_large": "va_industry"
}
# RUN MODEL
df_industrial = sm.sm_industrial(exp_design, dict_gdp_field)
df_industrial = pd.DataFrame(df_industrial)
#fields to add to extraction (also for ordering)
fields_df_ind = list(df_industrial.columns)
#loop
for field in fields_id_for_df_merges:
	df_industrial[field] = np.array(exp_design[field])
#reorder
df_industrial = df_industrial[fields_id_for_df_merges + fields_df_ind]




#########################
###                   ###
###    AGRICULTURE    ###
###                   ###
#########################

print("Building agriculture results...")
##  ADD IN CROPLAND
str_id_ag = "_yield_tonnes_ha"
all_ag = [x.replace(str_id_ag, "") for x in exp_design.columns if str_id_ag in x]
#get fractional columns
fields_frac_ag = ["frac_lu_" + x for x in all_ag]
#add to experimental design for use in
exp_design["frac_lu_cropland"] = exp_design[fields_frac_ag].sum(axis = 1)

##  RUN MODEL
df_agriculture = sm.sm_agriculture(exp_design, all_ag, sr.area_cr)
#convert to dataframe
df_agriculture = pd.DataFrame(df_agriculture)
#fields to add to extraction (also for ordering)
fields_df_ag = list(df_agriculture.columns)
#loop
for field in fields_id_for_df_merges:
	df_agriculture[field] = np.array(exp_design[field])
#reorder
df_agriculture = df_agriculture[fields_id_for_df_merges + fields_df_ag]




#######################
###                 ###
###    LIVESTOCK    ###
###                 ###
#######################

print("Building livestock results...")
#get all available livestock classes
str_ls_id = "_manure_ef_c1_gg_co2e_head"
all_ls = [x.replace(str_ls_id, "") for x in exp_design.columns if str_ls_id in x]
# RUN MODEL
df_livestock = sm.sm_livestock(exp_design, all_ls)
#convert to dataframe
df_livestock = pd.DataFrame(df_livestock)
#fields to add to extraction (also for ordering)
fields_df_ls = list(df_livestock.columns)
#loop
for field in fields_id_for_df_merges:
	df_livestock[field] = np.array(exp_design[field])
#reorder
df_livestock = df_livestock[fields_id_for_df_merges + fields_df_ls]




######################
###                ###
###    LAND USE    ###
###                ###
######################


##  INITIALIZE SOME DATA

print("Building land use results...")
#get all fractions
str_id_lu = "frac_lu_"
all_lu = ["cropland"] + [x.replace(str_id_lu, "") for x in params[params["sector"] == "land_use"]["parameter"].unique() if str_id_lu in x]
#id for forests
str_id_forest = "frac_lu_"
#add in forest information
all_forest = [x.replace(str_id_lu, "") for x in params[params["sector"] == "forest"]["parameter"].unique() if str_id_lu in x]
#all conversion classes
str_id_lu_conv = "_conv_to_"
all_lu_conv = [x.split(str_id_lu_conv)[1].replace("_area_ha", "") for x in exp_design.columns if str_id_lu_conv in x]
# RUN MODEL
df_land_use = sm.sm_land_use(exp_design, all_lu, all_forest, all_lu_conv, (len(all_master), len(all_year)), sr.area_cr, sr.use_lu_diff_for_conv_q)
#convert to dataframe
df_land_use = pd.DataFrame(df_land_use)
#fields to add to extraction (also for ordering)
fields_df_lu = list(df_land_use.columns)
#loop
for field in fields_id_for_df_merges:
	df_land_use[field] = np.array(exp_design[field])
#reorder
df_land_use = df_land_use[fields_id_for_df_merges + fields_df_lu]






###################
###             ###
###    WASTE    ###
###             ###
###################


print("Building waste results...")

t1 = time.time()
##  SOME BASIC INITIALIZATION

str_master = "master_id"

######################################################
#    NORMALIZE PROPORTIONAL GROUPINGS TO SUM TO 1    #
######################################################

#dictionary of grouping types substrings to signify normalization
dict_prop_groups = {"typo_de_ar": "frac_ar_", "typo_de_sdrd": "frac_typo_de_sdrd_", "typo_de_residuo_en_sdrd": "sdrd_frac_"}
#renormalize for groups
for grouping in list(dict_prop_groups.keys()):
    #get substring
    substr_identifier = str(dict_prop_groups[grouping])
    #get all columns associated with proportion of waste sent to different landfill types given it's sent to a landfil
    fields_group = [x for x in list(exp_design.columns) if (substr_identifier in x)]
    #get totals
    fields_group_totals = list(exp_design[fields_group].sum(axis = 1))
    #renormalize to ensure summation to 1
    for field in fields_group:
        exp_design[field] = exp_design[field]/fields_group_totals
    

#######################################################################################
#    GET AVERAGE METHANE CORRECTION FACTOR (based on theory, we only need average)    #
#######################################################################################

#get substring
substr_identifier = str(dict_prop_groups["typo_de_sdrd"])
#get all columns associated with proportion of waste sent to different landfill types given it's sent to a landfil
fields_group = [x for x in list(exp_design.columns) if (substr_identifier in x)]
#initialize vector of average mfc
vec_mcf = [0 for x in range(len(exp_design))]
vec_mcf_dwb = [0 for x in range(len(df_waste_baseline))]
#renormalize to ensure summation to 1
for field in fields_group:
    #split to get mfc for projections
    mcf = (field.split("_")[-1])
    mcf = float(mcf.replace("mcf", ""))
    #update
    vec_mcf = vec_mcf + mcf*exp_design[field]
    #add for baseline
    vec_mcf_dwb = vec_mcf_dwb + mcf*df_waste_baseline[field]
    
#new field for mean mcf
field_mean_mcf = "mean_mcf_sdrd"
#add it to waste file
exp_design[field_mean_mcf] = vec_mcf
df_waste_baseline[field_mean_mcf] = vec_mcf_dwb
#get reduced data
exp_design_waste = exp_design[[str_master, "year"] + dict_sector_field["all"] + dict_sector_field["waste"] + [field_mean_mcf]]


################################################
#    INITIALIZE SOME PARAMETERS BEFORE LOOP    #
################################################



#initialize baseline year data fram
df_base_years = pd.DataFrame({"year": list(range(min(model_years), max(model_years) + 1))})

###   DENOTE SOME SETS

#get set of all waste types for RSO
substr_identifier = str("rso_doc_")
#get all columns associated with proportion of waste sent to different landfill types given it's sent to a landfil
all_waste_sdrd = [x.replace(substr_identifier, "") for x in list(exp_design.columns) if (substr_identifier in x)]

#get set of aguas residuales
substr_identifier = dict_prop_groups["typo_de_ar"]
#get all columns associated with proportion of waste sent to different landfill types given it's sent to a landfil
all_ares = [x.replace(substr_identifier, "") for x in list(exp_design.columns) if (substr_identifier in x)]

###   ASSUMPTIONS FROM IPCC MODEL
#fraction of DOC dissimilated
doc_f = 0.5
#average delay time + 7; month of reaction start. Assume that all waste deposited in year T does not begin emitting until Jan 1 in year T + 1
doc_m = 13
#fraction of gas released that is methane (CHECK THIS IN DP PLAN 2012—GIVEN AS 0.465)
frac_gas_f = 0.5


####################
#    BEGIN LOOP    #
####################


#get all gasses that could be looped over for burned waste
all_gasses = list(sr.dict_gas_to_co2e.keys())
all_gasses.sort()
#fields for intersection
fields_int = list(set(df_waste_baseline.columns) & set(exp_design.columns))
fields_int.sort()
fields_int = ["year"] + [x for x in fields_int if x != "year"]
#initialize data frame?
initializeDFQ = True

#notify of timinmg
print("Starting waste loop  (Time elapsed: " + str(np.round((time.time() - t0)/60, 2)) + " minutes)...")

#TEMPORARY reduced
master_run_base = list(exp_design[exp_design["future_id"] == 0]["master_id"].unique())
master_run_base.sort()

#loop over each design
for master_id in all_master:
    #build temporary data frame
    dat_waste = exp_design_waste[exp_design_waste[str_master] == master_id]
    #fields to extract
    ext_fields_dw = [x for x in dat_waste.columns if not (x in [str_master])]
    #join in to expand years out
    dat_waste = pd.merge(df_base_years, dat_waste[fields_int], on = "year", how = "left")
    dat_waste = dat_waste.sort_values(by = ["year"])
    #fill in missing values using linear interpolation
    dat_waste = dat_waste.interpolate()

    #dictionay to map proportions of sewage waste to ar treatment type
    dict_ar_proportions = {}
    #loop to build
    for art in all_ares:
        #update waste proportions of rso by type
        field = str(dict_prop_groups["typo_de_ar"]) + art
        #update dat waste to use 0s
        dat_waste = dat_waste.fillna({field: 0})
        dict_ar_proportions.update({art: dat_waste[field]})

    #set dictionary of waste proportions of sdrd
    dict_sdrd_waste_props = {}
    dict_sdrd_mcf = {}
    #loop over waste types to update dictionary
    for wt in all_waste_sdrd:
        #update waste proportions dictionary and mcf
        if not wt == "industrial":
            dict_sdrd_mcf.update({wt: dat_waste[field_mean_mcf]})
            #update waste proportions of rso by type
            field = str(dict_prop_groups["typo_de_residuo_en_sdrd"]) + wt
            dict_sdrd_waste_props.update({wt: dat_waste[field]})
        else:
            #all industrial waste heads to rellenos sanitarios, hence mcf of 1
            dict_sdrd_mcf.update({wt: [1 for x in range(0, len(dat_waste))]})

    #get data frame
    df_wt = sm.sm_waste(
        dat_waste[fields_int],
        df_waste_baseline[fields_int],
        all_gasses,
        all_waste_sdrd,
        all_ares,
        dict_prop_groups,
        doc_m,
        doc_f,
        frac_gas_f,
        sr.dict_gas_to_co2e,
        #map populations to fields
        {"population": "total_population", "gdp_ind": "va_industry"},
        #set of compost
        set({"alimiento", "jardin"})
    )

    #get header
    fields_ord = list(df_wt.columns)
    #add run and design id
    df_wt[str_master] = master_id
    #reorder
    fields_ord = [str_master] + fields_ord
    df_wt = df_wt[fields_ord]

    #notify
    if (master_id%1000) == 0:
        print("Waste model for master_id: " + str(master_id) + " complete  (Time elapsed: " + str(np.round((time.time() - t0)/60, 2)) + " minutes)")

    #update
    if initializeDFQ:
        df_wt_master = df_wt
        initializeDFQ = False
    else:
        fields_wt = list(df_wt_master.columns)
        df_wt_master = pd.concat([df_wt_master, df_wt[fields_wt]])



print("Starting generation of output data frame...")


##  SET INFORMATION FOR MERGES

fields_merge = ["master_id", "year"]
#initialize results
results = exp_design[fields_merge].copy()
#fields to extract
fields_extract = []


##  MERGE AGRICULTURE

print("Joining agriculture to results...")
#merge with indsutrial output
results = pd.merge(results, df_agriculture, on = fields_merge, how = "inner")
#get fields to add to extraxction fields
ext_fields_agriculture = [x for x in df_agriculture.columns if not (x in fields_merge)]
#add in to extraction fields
fields_extract = fields_extract + ext_fields_agriculture


##  MERGE LAND USE

print("Joining land use to results...")
#merge with indsutrial output
results = pd.merge(results, df_land_use, on = fields_merge, how = "inner")
#get fields to add to extraxction fields
ext_fields_land_use = [x for x in df_land_use.columns if not (x in fields_merge)]
#add in to extraction fields
fields_extract = fields_extract + ext_fields_land_use


##  MERGE LIVESTOCK

print("Joining livestock to results...")
#merge with indsutrial output
results = pd.merge(results, df_livestock, on = fields_merge, how = "inner")
#get fields to add to extraxction fields
ext_fields_livestock = [x for x in df_livestock.columns if not (x in fields_merge)]
#add in to extraction fields
fields_extract = fields_extract + ext_fields_livestock


##  MERGE BUILDINGS

print("Joining buildings to results...")
#merge with indsutrial output
results = pd.merge(results, df_buildings, on = fields_merge, how = "inner")
#get fields to add to extraxction fields
ext_fields_buildings = [x for x in df_buildings.columns if not (x in fields_merge)]
#add in to extraction fields
fields_extract = fields_extract + ext_fields_buildings



##  MERGE INDUSTRIAL

print("Joining industrial to results...")
#merge with indsutrial output
results = pd.merge(results, df_industrial, on = fields_merge, how = "inner")
#get fields to add to extraxction fields
ext_fields_industrial = [x for x in df_industrial.columns if not (x in fields_merge)]
#add in to extraction fields
fields_extract = fields_extract + ext_fields_industrial


##  MERGE WASTE

print("joining waste to results...")
#merge with df_wt_master
results = pd.merge(results, df_wt_master, on = fields_merge, how = "inner")
#get fields to add to extraxction fields
ext_fields_dfwt = [x for x in df_wt_master.columns if not (x in fields_merge)]
#add in to extraction fields
fields_extract = fields_extract + ext_fields_dfwt


##  ADD SOME SUMMARY FIELDS

fm = ["master_id", "year"]
#fields to aggregate over for summaries
dict_total_fields = {
    "industry": ["emissions_industry_energy_input_MT_co2e", "emissions_industry_indproc_total_MT_co2e"],
    "agriculture": ["emissions_agriculture_crops_total_MT_co2e", "emissions_agriculture_energy_input_MT_co2e"]
}
#loop to add on
for sec in dict_total_fields.keys():
    #new total field
    field_new = "emissions_" + str(sec) + "_total_MT_co2e"
    #add in some summaries
    results[field_new] = results[dict_total_fields[sec]].sum(axis = 1)
    #add to extraction fields
    fields_extract = fields_extract + [field_new]
#sort
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



##  CREATE PACKAGE TO PASS

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


#get reduced experimental design data to export
if os.path.exists(sr.fp_csv_fields_keep_experimental_design_multi_sector):
	fields_keep_ed = pd.read_csv(sr.fp_csv_fields_keep_experimental_design_multi_sector)
	#fill na
	fields_keep_ed = fields_keep_ed.fillna(0)
	#dictionary of keep fields
	dict_fields_keep_export = {}
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


print("Done. Total time elapsed: " + str(np.round((time.time() - t0)/60, 2)) + " minutes)")


