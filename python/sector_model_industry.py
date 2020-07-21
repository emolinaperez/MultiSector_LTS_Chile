import pandas as pd
import numpy as np


#####################################
#    INDUSTRY - PROCESS EMISSIONS   #
#####################################
    
def sm_industrial(df_in, dict_gdp_field):
    #initialize output dictionary
	dict_out = {}
	vec_total_emit = 0.
	#gdp based
	for prod in ["carburo", "cal", "vidrio", "industry_at_large"]:
		if prod != "industry_at_large":
			field_emit = "emissions_industry_indproc_" + prod + "_MT_co2e"
		else:
			field_emit = "emissions_industry_indproc_general_use_MT_co2e"
		field_gdp = dict_gdp_field[prod]
		field_factor = prod + "_kt_co2e_per_million_usd"
		#update emissions
		vec_emit = np.array(df_in[field_gdp])*np.array(df_in[field_factor])/1000
		#add to total
		vec_total_emit = vec_total_emit + vec_emit
		#update dictionary
		dict_out.update({field_emit: vec_emit})
	
	#cement
	prod = "cemento"
	field_emit = "emissions_industry_indproc_" + prod + "_MT_co2e"
	field_prod = "production_industry_" + prod + "_KT"
	field_gdp = dict_gdp_field[prod]
	field_factor = prod + "_kt_co2e_per_kt_prod"
	field_prod_factor = prod + "_kt_prod_per_million_usd"
	#estimate production
	vec_prod = np.array(df_in[field_prod_factor])*np.array(df_in[field_gdp])
	#calculate emissions
	vec_emit = vec_prod*np.array(df_in[field_factor])/1000
	#add to total
	vec_total_emit = vec_total_emit + vec_emit

	#update emissions
	dict_out.update({
		field_prod: vec_prod,
		field_emit: vec_emit,
		"emissions_industry_indproc_total_MT_co2e": vec_total_emit
	})

	#return
	return dict_out


