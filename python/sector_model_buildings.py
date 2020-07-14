import pandas as pd
import numpy as np


###################
#    BUILDINGS    #
###################

def sm_buildings(df_in):

	
	#dictionary of fields to apply scalar to
	all_builds = ["agriculture", "commercial", "industry", "residential"]
	#dictionary to map sectors to shorthand
	dict_shorthand = dict([[x, x[0:3]] for x in all_builds])
	
	
	#output dictionary
	dict_out = {}
	#gdp based
	for build in list(set(all_builds) - {"residential"}):
		
		if build == "commercial":
			field_emit = "emissions_buildings_stationary_MT_co2e_com"
		else:
			field_emit = "emissions_" + build + "_energy_input_MT_co2e"
		#add in livestock
		if build == "agriculture":
			additional_gdp = np.array(df_in["va_livestock"])
		else:
			additional_gdp = float(0)
			
		#update field for energy consumption
		field_energy_demand_elec = "energy_consumption_electricity_PJ_" + dict_shorthand[build]
		field_energy_demand_nonelec = "energy_consumption_non_electricity_PJ_" + dict_shorthand[build]
		#some components
		field_dem_fac = build + "_df_pj_per_million_gdp"
		field_factor = build + "_ef_kt_co2e_per_pj"
		field_elec_frac = build + "_frac_electric"
		field_va = "va_" + build
		#energy demand
		dem_ener = (np.array(df_in[field_va]) + additional_gdp)*np.array(df_in[field_dem_fac])
		frac_elec = np.array(df_in[field_elec_frac])
		vec_out = (1 - frac_elec)*dem_ener*np.array(df_in[field_factor])
		#convert to megatons
		vec_out = vec_out/1000
		#
		dict_out.update({
			field_emit: vec_out,
			field_energy_demand_elec: frac_elec*dem_ener,
			field_energy_demand_nonelec: (1 - frac_elec)*dem_ener
		})
		
	# RESIDENTIAL
	build = "residential"
	field_emit = "emissions_buildings_stationary_MT_co2e_res"
	#some components
	field_dem_fac = build + "_df_pj_per_hh"
	field_factor = build + "_ef_kt_co2e_per_pj"
	field_elec_frac = build + "_frac_electric"
	field_or = "occ_rate"
	#energy demand
	field_energy_demand_elec = "energy_consumption_electricity_PJ_" + dict_shorthand[build]
	field_energy_demand_nonelec = "energy_consumption_non_electricity_PJ_" + dict_shorthand[build]
	#number of households
	vec_hh = np.array(df_in["total_population"])/np.array(df_in[field_or])
	#energy demand
	dem_ener = vec_hh*np.array(df_in[field_dem_fac])
	frac_elec = np.array(df_in[field_elec_frac])
	#output emissions
	vec_out = (1 - frac_elec)*dem_ener*np.array(df_in[field_factor])
	vec_out = vec_out/1000
	
	dict_out.update({
		field_emit: vec_out,
		field_energy_demand_elec: frac_elec*dem_ener,
		field_energy_demand_nonelec: (1 - frac_elec)*dem_ener
	})

	
	#fields to sum for buildings total over
	fields_total = ["emissions_buildings_stationary_MT_co2e_" + x for x in ["res", "com"]]
	#set total vector
	total_em = sum(np.array([dict_out[x] for x in fields_total]))
	#update
	dict_out.update({"emissions_buildings_total_MT_co2e": total_em})

	#return
	return dict_out

