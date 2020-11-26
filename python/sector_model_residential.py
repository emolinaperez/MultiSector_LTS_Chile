# Residential energy model developed by Centro de Energia U. de Chile using RAND python framework
# version 0.7 september 2020

import os, os.path
import time
import pandas as pd
import numpy as np


###################
#    RESIDENTIAL    #
###################

def sm_residential(df_in, dict_sector_abv):
	# conversion factor Tcal to TJ
	fact = 4.184
	# conversion factor Tcal to GWh
	fact2 = 1.162952

	# Read input parameters defined in parameter_ranges.csv
	total_population = np.array(df_in["poblacion"])
	residential_occ_rate = np.array(df_in["residential_occ_rate"])
	residential_intensity = np.array(df_in["residential_intensity"])
	residential_frac_natural_gas = np.array(df_in["residential_frac_natural_gas"])
	residential_frac_kerosene = np.array(df_in["residential_frac_kerosene"])
	residential_frac_electric = np.array(df_in["residential_frac_electric"])
	residential_frac_biomass = np.array(df_in["residential_frac_biomass"])
	residential_frac_pliqgas = np.array(df_in["residential_frac_pliqgas"])
	residential_frac_solar = np.array(df_in["residential_frac_solar"])
	residential_frac_hydrogen = np.array(df_in["residential_frac_hydrogen"])
	residential_emission_fact_natural_gas = np.array(df_in["residential_emission_fact_natural_gas"])
	residential_emission_fact_kerosene = np.array(df_in["residential_emission_fact_kerosene"])
	residential_emission_fact_pliqgas = np.array(df_in["residential_emission_fact_pliqgas"])

	# number of households
	residential_household = total_population/residential_occ_rate

	# calculate demand in Tcal
	residential_demand = residential_intensity*total_population/1000
	residential_dem_natural_gas =  residential_intensity*residential_household*residential_frac_natural_gas/1000
	residential_dem_kerosene =  residential_intensity*residential_household*residential_frac_kerosene/1000
	residential_dem_electric =  residential_intensity*residential_household*residential_frac_electric/1000
	residential_dem_biomass =  residential_intensity*residential_household*residential_frac_biomass/1000
	residential_dem_pliqgas =  residential_intensity*residential_household*residential_frac_pliqgas/1000
	residential_dem_solar =  residential_intensity*residential_household*residential_frac_solar/1000

	# calculate emission in millon tCO2
	residential_emission_natural_gas = residential_dem_natural_gas * fact * residential_emission_fact_natural_gas / (10 ** 9)
	residential_emission_kerosene = residential_dem_kerosene * fact * residential_emission_fact_kerosene / (10 ** 9)
	residential_emission_pliqgas = residential_dem_pliqgas * fact * residential_emission_fact_pliqgas / (10 ** 9)
	residential_emission = residential_emission_natural_gas+residential_emission_kerosene+residential_emission_pliqgas

	dict_emission = {"residential": residential_emission}
	dict_electric_demand = {"residential": residential_dem_electric*fact2}


	##  final output dictionary
	
	dict_out = {}
	
	#add emissions to master output
	for k in dict_emission.keys():
		#new key conveys emissions
		k_new = str(k).replace("residential", dict_sector_abv["residential"]) + "-emissions_total-mtco2e"
		#add to output
		dict_out.update({k_new: dict_emission[k].copy()})
		
	#add electric demand to master output
	for k in dict_electric_demand.keys():
		#new key conveys emissions
		k_new = str(k).replace("residential", dict_sector_abv["residential"]) + "-electricity_total_demand-gwh"
		#add to output
		dict_out.update({k_new: dict_electric_demand[k].copy()})
	
	#return
	return dict_out#dict_emission,dict_electric_demand
