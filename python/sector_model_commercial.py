# Commercial energy model developed by Centro de Energia U. de Chile using RAND python framework
# version 0.9 september 2020

import os, os.path
import time
import pandas as pd
import numpy as np
from econometric_models import model_commercial

#############################
#    COMMERCIAL    #
############################

def sm_commercial(df_in, dict_sector_abv):

	# conversion factor Tcal to TJ
	fact = 4.184
	# conversion factor Tcal to GWh
	fact2 = 1.162952

	# econometric parameters
	alfa = -10.9583
	beta = 1.7308

	# Common parameters
	share_electric_grid_to_hydrogen = np.array(df_in["share_electric_grid_to_hydrogen"])
	electrolyzer_efficiency = np.array(df_in["electrolyzer_efficiency"])

	# Read input parameters defined in parameter_ranges.csv
	gdp = np.array(df_in["pib"]) * np.array(df_in["pib_scalar_transport"])
	growth_rate_gdp = np.array(df_in["gr_pib"])
	#growth_rate_gdp = np.array(df_in["growth_rate_gdp"])
	commercial_elasticity = np.array(df_in["commercial_elasticity"])
	commercial_frac_diesel = np.array(df_in["commercial_frac_diesel"])
	commercial_frac_natural_gas = np.array(df_in["commercial_frac_natural_gas"])
	commercial_frac_electric = np.array(df_in["commercial_frac_electric"])
	commercial_frac_biomass = np.array(df_in["commercial_frac_biomass"])
	commercial_frac_hydrogen = np.array(df_in["commercial_frac_hydrogen"])
	commercial_frac_pliqgas = np.array(df_in["commercial_frac_pliqgas"])
	commercial_frac_kerosene = np.array(df_in["commercial_frac_kerosene"])
	commercial_frac_solar = np.array(df_in["commercial_frac_solar"])
	commercial_emission_fact_diesel = np.array(df_in["commercial_emission_fact_diesel"])
	commercial_emission_fact_natural_gas = np.array(df_in["commercial_emission_fact_natural_gas"])
	commercial_emission_fact_pliqgas = np.array(df_in["commercial_emission_fact_pliqgas"])
	commercial_emission_fact_kerosene = np.array(df_in["commercial_emission_fact_kerosene"])

	# calculate demand in Tcal as function of GDP
	# commercial_demand = np.exp(alfa+beta*np.log(gdp))
	year = np.array(df_in["year"])  # vector years
	commercial_demand = model_commercial(year, growth_rate_gdp, commercial_elasticity)

	commercial_dem_diesel = commercial_demand * commercial_frac_diesel
	commercial_dem_natural_gas = commercial_demand * commercial_frac_natural_gas
	commercial_dem_electric = commercial_demand * commercial_frac_electric
	commercial_dem_biomass = commercial_demand * commercial_frac_biomass
	commercial_dem_hydrogen = commercial_demand * commercial_frac_hydrogen
	commercial_dem_pliqgas = commercial_demand * commercial_frac_pliqgas
	commercial_dem_kerosene = commercial_demand * commercial_frac_kerosene
	commercial_dem_solar = commercial_demand * commercial_frac_solar

	# calculate emission in millon tCO2
	commercial_emission_diesel = commercial_dem_diesel * fact * commercial_emission_fact_diesel / (10 ** 9)
	commercial_emission_natural_gas = commercial_dem_natural_gas * fact * commercial_emission_fact_natural_gas / (
				10 ** 9)
	commercial_emission_pliqgas = commercial_dem_pliqgas * fact * commercial_emission_fact_pliqgas / (10 ** 9)
	commercial_emission_kerosene = commercial_dem_kerosene * fact * commercial_emission_fact_kerosene / (10 ** 9)

	commercial_emission = commercial_emission_diesel + commercial_emission_natural_gas + commercial_emission_pliqgas + commercial_emission_kerosene

	# electric demand to produce hydrogen
	electric_demand_hydrogen = commercial_dem_hydrogen / electrolyzer_efficiency * share_electric_grid_to_hydrogen
	electric_demand_hydrogen = electric_demand_hydrogen * fact2

	dict_emission = {"commercial": commercial_emission}
	dict_electric_demand = {"commercial": commercial_dem_electric * fact2}

	# output dictionary
	dict_out = {}

	# add emissions to master output
	for k in dict_emission.keys():
		# new key conveys emissions
		k_new = str(k).replace("commercial", dict_sector_abv["commercial"]) + "-emissions_total-mtco2e"
		# add to output
		dict_out.update({k_new: dict_emission[k].copy()})

	# add electric demand to master output
	for k in dict_electric_demand.keys():
		# new key conveys emissions
		k_new = str(k).replace("commercial", dict_sector_abv["commercial"]) + "-electricity_total_demand-gwh"
		# add to output
		dict_out.update({k_new: dict_electric_demand[k].copy()})

	dict_out.update({
		(dict_sector_abv["commercial"] + "-electricity_hydrogen-gwh"): electric_demand_hydrogen,
	})

	# return
	return dict_out  # dict_emission,dict_electric_demand
