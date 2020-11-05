# Residential energy model developed by Centro de Energia U. de Chile using RAND python framework
# version 0.9 september 2020

import os, os.path
import time
import pandas as pd
import numpy as np


#################################
#    PUBLIC SECTOR & SANITARY   #
################################

#pending
def sm_public(df_in, dict_sector_abv):

	# conversion factor Tcal to TJ
	fact = 4.184
	# conversion factor Tcal to GWh
	fact2 = 1.162952

	# Read input parameters defined in parameter_ranges.csv

	population = np.array(df_in["poblacion"])
	public_intensity = np.array(df_in["public_intensity"])
	public_frac_diesel = np.array(df_in["public_frac_diesel"])
	public_frac_natural_gas = np.array(df_in["public_frac_natural_gas"])
	public_frac_electric = np.array(df_in["public_frac_electric"])
	public_frac_biomass = np.array(df_in["public_frac_biomass"])
	public_frac_pliqgas = np.array(df_in["public_frac_pliqgas"])
	public_frac_kerosene = np.array(df_in["public_frac_kerosene"])
	public_emission_fact_natural_gas = np.array(df_in["public_emission_fact_natural_gas"])
	public_emission_fact_kerosene = np.array(df_in["public_emission_fact_kerosene"])
	public_emission_fact_pliqgas = np.array(df_in["public_emission_fact_pliqgas"])

	# calculate demand in Tcal
	public_dem_diesel = population * public_intensity * public_frac_diesel/1000
	public_dem_natural_gas = population * public_intensity * public_frac_natural_gas/1000
	public_dem_electric = population * public_intensity * public_frac_electric/1000
	public_dem_biomass = population * public_intensity * public_frac_biomass/1000
	public_dem_kerosene = population * public_intensity * public_frac_kerosene/1000
	public_dem_pliqgas = population * public_intensity * public_frac_pliqgas/1000

	# calculate emission in millon tCO2
	public_emission_natural_gas = public_dem_natural_gas * fact * public_emission_fact_natural_gas / (10 ** 9)
	public_emission_kerosene = public_dem_kerosene * fact * public_emission_fact_kerosene / (10 ** 9)
	public_emission_pliqgas = public_dem_pliqgas * fact * public_emission_fact_pliqgas / (10 ** 9)
	public_emission = public_emission_natural_gas + public_emission_kerosene + public_emission_pliqgas

	dict_emission = {"public": public_emission}
	dict_electric_demand = {"public": public_dem_electric * fact2}

	#output dictionary
	dict_out = {}
	
	#add emissions to master output
	for k in dict_emission.keys():
		#new key conveys emissions
		k_new = str(k).replace("public", dict_sector_abv["public"]) + "-emissions_total-mtco2e"
		#add to output
		dict_out.update({k_new: dict_emission[k].copy()})
	
	#add electric demand to master output
	for k in dict_electric_demand.keys():
		#new key conveys emissions
		k_new = str(k).replace("public", dict_sector_abv["public"]) + "-electricity_total_demand-gwh"
		#add to output
		dict_out.update({k_new: dict_electric_demand[k].copy()})
		
	return dict_out#dict_emission,dict_electric_demand
