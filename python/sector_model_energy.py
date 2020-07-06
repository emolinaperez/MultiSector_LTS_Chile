import os, os.path
import time
import pandas as pd
import numpy as np


################
#    ENERGY    #
################

#note: energy model here doesn't pull from the df_in directly—as the other sector models do—due to legacy issues. This can be fixed easily.

def sm_energy(vec_pop, vec_gdp, vec_dem_pgdp_grid_com, vec_dem_pgdp_ind, vec_dem_pc_grid_res, frac_ind_energy_elec, vec_ef_per_energy_ind, dict_pp_props, dict_pp_ef, dict_co2e):
		
	# vec_pop is the population in millions
	# vec_gdp is total gdp in billion $USD
	# vec_dem_pgdp_grid_com is commercial demand factor in PJ/billion $USD
	# vec_dem_pgdp_grid_ind is industrial demand factor in PJ/billion $USD
	# vec_dem_pc_grid_res is residential demand factor in PJ/million people
	# frac_ind_energy_elec is the fraction of industrial energy that comes from electricity
	# vec_ef_per_energy_ind is the emissions factor for non-electric industrial energy (KTCO2e/PJ)
	# dict_pp_props is a dictionary (power plant, subtype) of proportion of power provided by each type
	# dict_pp_ef is a dictionary (gas, power plant, pp subtype) of emissions factors by gas, pp, and pps
	# dict_co2e gives the co2e transformations for different gasses

	#names from each dictionary

	#set all classes
	all_pp = [x for x in dict_pp_props.keys()]
	all_pps = [x for x in dict_pp_props[all_pp[0]]]
	all_gasses = [x for x in dict_co2e if (x in dict_pp_ef.keys())]

	#generate total grid demand by sector
	dem_grid_com = vec_gdp * vec_dem_pgdp_grid_com
	dem_grid_ind = vec_gdp * vec_dem_pgdp_ind * frac_ind_energy_elec
	dem_grid_res = vec_pop * vec_dem_pc_grid_res
	
	#get non-electric industrial energy emissions
	dem_nongrid_ind = vec_gdp * vec_dem_pgdp_ind * (1 - frac_ind_energy_elec)
	em_nonelectric_energy_ind = dem_nongrid_ind * vec_ef_per_energy_ind
	
	
	#initialize each grid emissions type
	grid_em_com = [0 for x in range(len(vec_gdp))]
	grid_em_ind = [0 for x in range(len(vec_gdp))]
	grid_em_res = [0 for x in range(len(vec_pop))]

	#loop over gas types to generate emissions totals
	for gas in all_gasses:
		#multiply by co2e
		equiv = dict_co2e[gas]
		#loop over each power plant type
		for ppt in all_pp:
			for ppst in all_pps:
				#get proportion of emissions from the type
				prop = dict_pp_props[ppt][ppst]
				#get emissions factors per PJ
				ef = dict_pp_ef[gas][ppt][ppst]
				#get total commercial and residential grid demand satisfied
				grid_em_com = grid_em_com + ef * prop * dem_grid_com
				grid_em_ind = grid_em_ind + ef * prop * dem_grid_ind
				grid_em_res = grid_em_res + ef * prop * dem_grid_res
				
	#set total vector
	total_em_grid = [(grid_em_com[x] + grid_em_ind[x] + grid_em_res[x])/1000 for x in range(len(grid_em_com))]
	#set total vector
	total_em = [(total_em_grid[x] + (em_nonelectric_energy_ind[x]/1000)) for x in range(len(grid_em_com))]
				
	#set output
	dict_output = {
		"energy_consumption_electricity_PJ_com": dem_grid_com,
		"energy_consumption_electricity_PJ_ind": dem_grid_ind,
		"energy_consumption_electricity_PJ_res": dem_grid_res,
		"energy_consumption_non_electricity_PJ_ind": dem_nongrid_ind,
		"emissions_electricity_MT_co2e_com": grid_em_com/1000,
		"emissions_electricity_MT_co2e_ind": grid_em_ind/1000,
		"emissions_electricity_MT_co2e_res": grid_em_res/1000,
		"emissions_non_electricity_energy_MT_co2e_ind": em_nonelectric_energy_ind/1000,
		"emissions_electricity_total_MT_co2e": total_em_grid,
		"emissions_energy_sector_total_MT_co2e": total_em
	}
	#return
	return dict_output


