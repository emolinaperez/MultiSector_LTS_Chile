import pandas as pd
import numpy as np


###################
#    LIVESTOCK    #
###################

def sm_livestock(df_in, all_ls):

	#initialize output dictionary
	dict_out = {}
	#initialize total emissions by type
	vec_total_emit_man = 0.0
	vec_total_emit_fer = 0.0
	vec_total_emit = 0.0
	#gdp based
	for lsc in all_ls:
		#idenfity some fields
		field_count = lsc
		#get emissions factors fields
		field_ef_f = lsc + "_fermentation_ef_c1_gg_co2e_head"
		field_ef_m = lsc + "_manure_ef_c1_gg_co2e_head"
		#emission total fields
		field_emit_f = "emissions_livestock_" + lsc + "_fermentation_MT_co2e"
		field_emit_m = "emissions_livestock_" + lsc + "_manure_MT_co2e"
		#update emissions by type for this livestock class
		vec_emit_man = np.array(df_in[field_count])*np.array(df_in[field_ef_m]).astype(float)/1000
		vec_emit_fer = np.array(df_in[field_count])*np.array(df_in[field_ef_f]).astype(float)/1000
		#update totals by type
		vec_total_emit_man = vec_total_emit_man + vec_emit_man
		vec_total_emit_fer = vec_total_emit_fer + vec_emit_fer
		#add to dictionary
		dict_out.update({
			field_emit_f: vec_emit_fer,
			field_emit_m: vec_emit_man
		})
	
	#update total emissions for livestock
	vec_total_emit = vec_total_emit_man + vec_total_emit_fer
	#add to dictionary
	dict_out.update({
		"emissions_livestock_fermentation_MT_co2e": vec_total_emit_fer,
		"emissions_livestock_manure_MT_co2e": vec_total_emit_man,
		"emissions_livestock_total_MT_co2e": vec_total_emit
	})

	#return
	return dict_out

