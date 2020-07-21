import pandas as pd
import numpy as np

################################
#    AGRICULTURAL EMISSIONS    #
################################

def sm_agriculture(df_in, all_ag, area):
  	
	#initialize dict of output
	dict_out = {}
	#initialize total
	vec_total_emit = 0.
	#gdp based
	for ag in all_ag:
		#idenfity some fields
		field_area = "frac_lu_" + ag
		field_ef = ag + "_kg_co2e_ha"
		#emission total fields
		field_emit = "emissions_agriculture_" + ag + "_MT_co2e"
		#update total emissions (gg co2e)
		vec_emit = area*(np.array(df_in[field_area])*np.array(df_in[field_ef])*(10**(-6))).astype(float)
		#conver to MT
		vec_emit = vec_emit/1000
		
		#add to dictionary
		dict_out.update({
			field_emit: vec_emit
			#field_cost: vec_cost
		})
		#update
		vec_total_emit = vec_total_emit + vec_emit
	
	#test emissions
	vec_test_emit = np.ones(len(vec_total_emit)) * 0.95
	#add to dictionary
	dict_out.update({"emissions_agriculture_crops_total_MT_co2e": vec_total_emit})
	dict_out.update({"alpha_field_out": vec_test_emit})
    #return
	return dict_out
