import os, os.path
import numpy as np
import pandas as pd
import setup_runs as sr


#############################
###                       ###
###    BUILD PRIM FILE    ###
###                       ###
#############################


#initialize dictionary of categories
dict_field_type = {"master_id": "key"}
#results files
dict_results = {
	"python": pd.read_csv(sr.fp_csv_output_multi_sector),
	"analytica": pd.read_csv(sr.fp_csv_output_multi_sector_analytica),
	"gams": pd.read_csv(sr.fp_csv_output_multi_sector_pmr).rename(columns = {"agno": "year"})
}
#experimental design
df_ed = pd.read_csv(sr.fp_csv_experimental_design_msec)
#get maximum year
year_max = max(df_ed["year"])

#initialize prim data frame
fields_ed_id = ["master_id", "strategy_id"]
fields_ed_dat = [x for x in df_ed.columns if (x not in fields_ed_id) and ("_id" not in x) and (x != "year")]

#update dictionary
for field in fields_ed_id:
	if field != "master_id":
		dict_field_type.update({field: "filter"})
#initialize
df_prim = df_ed[(df_ed["year"] == year_max) & (df_ed["design_id"] == 0)][fields_ed_id + fields_ed_dat]
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
#attribute file
df_attribute_field.to_csv(sr.fp_csv_prim_field_attribute, index = None, encoding = "UTF-8")
#input data
df_prim.to_csv(sr.fp_csv_prim_input_data, index = None, encoding = "UTF-8")


print("Prim file(s) generation complete.")

