import os, os.path
import numpy as np
import pandas as pd
import setup_runs as sr


#############################
###                       ###
###    BUILD PRIM FILE    ###
###                       ###
#############################

#restore from archive?
restore_from_archive_q = True
#set the name
archive_name = "Chile_sector_package_2021_02_20_full_package"

if restore_from_archive_q:
    print("\n\n" + "#"*30 + "\n###\n###    NOTE: BUILDING PRIM FROM ARCHIVE '" + archive_name + "'...\n###\n" + "#"*30 + "\n\n")

#initialize dictionary of categories
dict_field_type = {"master_id": "key"}
#results information
dict_fp_results = {
    "python": sr.fp_csv_output_multi_sector,
    "analytica": sr.fp_csv_output_multi_sector_analytica,
    "gams": sr.fp_csv_output_multi_sector_pmr
}
dict_results = {}
#read in
for k in dict_fp_results.keys():
    #set file path
    if restore_from_archive_q:
        df_tmp = sr.get_archive_run(dict_fp_results[k], archive_name)
    else:
        df_tmp = pd.read_csv(dict_fp_results[k])
    
    df_tmp = df_tmp.rename(columns = {"Agno": "year", "agno": "year"})
    dict_results.update({k: df_tmp.copy()})

#default to ignore parameters (sometimes "full" packages don't have an integrated parameter sheet set)
use_params_q = False
#experimental design
if restore_from_archive_q:
    df_ed = sr.get_archive_run(sr.fp_csv_experimental_design_msec, archive_name)
    
    if os.path.exists(sr.get_archive_data_path(sr.fp_csv_parameter_ranges, archive_name)):
        df_params = sr.get_archive_run(sr.fp_csv_parameter_ranges, archive_name)
        use_params_q = True
else:
    df_ed = pd.read_csv(sr.fp_csv_experimental_design_msec)
    if os.path.exists(sr.fp_csv_parameter_ranges):
        df_params = pd.read_csv(sr.fp_csv_parameter_ranges)
        use_params_q = True



##  CHECK FOR TRAJGROUPS THAT NEED TO BE DROPPED

if use_params_q:
    fields_drop = list(df_params[df_params["trajgroup_no_vary_q"] == 1]["parameter"].unique())
    fields_drop = list(set([x for x in fields_drop if ("trajgroup_" in x) and ("-lhs" in x)]))
else:
    fields_drop = []
sr.print_list_output(fields_drop, "fields_drop")
#drop resulting values
df_ed = df_ed[[x for x in df_ed.columns if x not in fields_drop]]
    
    

#get maximum year
year_max = max(df_ed["year"])
#initialize prim data frame
fields_ed_id = ["master_id", "design_id", "strategy_id", "time_series_id"]
fields_ed_dat = [x for x in df_ed.columns if (x not in fields_ed_id) and ("_id" not in x) and (x != "year")]

#update dictionary
for field in fields_ed_id:
    if field != "master_id":
        dict_field_type.update({field: "filter"})
#initialize
df_prim = df_ed[(df_ed["year"] == year_max) & (df_ed["design_id"].isin([1, 3]))][fields_ed_id + fields_ed_dat]
#drop fields that don't vary
fields_keep = []
for field in fields_ed_dat:
    if len(set(df_prim[field])) > 1:
        fields_keep.append(field)
        #update dictionary
        dict_field_type.update({field: "input"})
#reduce the prim file
df_prim = df_prim[fields_ed_id + fields_keep]

print("Merging in:\n")
#then, loop over results to merge in
for k in dict_results.keys():
    print("\t" + str(k) + " to prim file;\n")
    #get dataframe and output dictionary
    df_tmp = dict_results[k]
    fields_ext = [x for x in df_tmp.columns if ("emissions_total" in x)]
    #update field type dictionary
    dict_ext = dict([[x, "output"] for x in fields_ext])
    dict_field_type.update(dict_ext)
    #reduce and merge
    df_tmp = df_tmp[df_tmp["year"] == year_max][["master_id"] + fields_ext]
    df_prim = pd.merge(df_prim, df_tmp, how = "inner", on = ["master_id"])

#get final masters
masters_keep = df_prim["master_id"].unique()
#loop to re-export
for k in dict_fp_results.keys():
    df_tmp = dict_results[k]
    df_tmp = df_tmp[df_tmp["master_id"].isin(masters_keep)].reset_index(drop = True)
    #export
    df_tmp.to_csv(dict_fp_results[k], index = None, encoding = "UTF-8")


##  BUILD ATTRIBUTE FILE

def set_def(x):
    if dict_field_type[x] == "filter":
        return "all"
    else:
        return ""

#initialize
df_attribute_field = [[x, x.replace("_", " "), dict_field_type[x], set_def(x), 1] for x in dict_field_type.keys()]
#dataframe
df_attribute_field = pd.DataFrame(df_attribute_field, columns = ["field_name", "field_display_name", "field_prim_type", "field_filter_default", "include"])
#convert to integer
df_attribute_field["include"] = np.array(df_attribute_field["include"]).astype(int)
    

################
#    EXPORT    #
################

print("\nExporting prim files...\n")

fp_out_attribute = sr.fp_csv_prim_field_attribute
fp_out_data = sr.fp_csv_prim_input_data
#export directly to arhive?
if restore_from_archive_q:
    fp_out_attribute = os.path.join(sr.dir_archive_runs, archive_name, os.path.basename(fp_out_attribute))
    fp_out_data = os.path.join(sr.dir_archive_runs, archive_name, os.path.basename(fp_out_data))
    
#attribute file
df_attribute_field.to_csv(fp_out_attribute, index = None, encoding = "UTF-8")
#input data
df_prim.to_csv(fp_out_data, index = None, encoding = "UTF-8")


print("Prim file(s) generation complete.")

