# Commercial energy model developed by Centro de Energia U. de Chile using RAND python framework
# version 0.9 september 2020

import os, os.path
import time
import pandas as pd
import numpy as np
from econometric_models import model_commercial, model_delta_capacity,  model_capacity

#############################
#    COMMERCIAL    #
############################

def sm_commercial(df_in, dict_sector_abv):

	# conversion factor Tcal to TJ
	fact = 4.184
	# conversion factor Tcal to GWh
	fact2 = 1.162952

	# Common parameters
	share_electric_grid_to_hydrogen = np.array(df_in["share_electric_grid_to_hydrogen"])
	electrolyzer_efficiency = np.array(df_in["electrolyzer_efficiency"])

	# conversion factor to fuel price from fisic unit to US$/Tcal
	fuel_price_coal_conversion = 142.9
	fuel_price_natural_gas_conversion = 4000
	fuel_price_diesel_conversion = 91.7

	# ratio between diesel and other fuels to model correlation
	ratio_fuel_price_diesel_gasoline = 1.75
	ratio_fuel_price_diesel_fuel_oil = 0.69
	ratio_fuel_price_diesel_kerosene = 0.72
	ratio_fuel_price_diesel_kerosene_aviation = 1.1

	# cost information
	# Conversion of fuel price to express all in US$/Tcal and to be coherent with the fuel prices of other sectors
	fuel_price_diesel = np.array(df_in["fuel_price_diesel"])
	commercial_fuel_price_diesel = fuel_price_diesel * fuel_price_diesel_conversion
	fuel_price_natural_gas = np.array(df_in["fuel_price_natural_gas"])
	commercial_fuel_price_natural_gas = fuel_price_natural_gas * fuel_price_natural_gas_conversion
	fuel_price_coal = np.array(df_in["fuel_price_coal"])
	commercial_fuel_price_coal = fuel_price_coal * fuel_price_coal_conversion

	fuel_price_gasoline = commercial_fuel_price_diesel * ratio_fuel_price_diesel_gasoline
	fuel_price_fuel_oil = commercial_fuel_price_diesel * ratio_fuel_price_diesel_fuel_oil
	fuel_price_kerosene = commercial_fuel_price_diesel * ratio_fuel_price_diesel_kerosene
	fuel_price_kerosene_aviation = commercial_fuel_price_diesel * ratio_fuel_price_diesel_kerosene_aviation

	commercial_fuel_price_coal = fuel_price_fuel_oil
	commercial_fuel_price_kerosene = fuel_price_kerosene
	commercial_fuel_price_gasoline = fuel_price_gasoline
	commercial_fuel_price_kerosene_aviation = fuel_price_kerosene_aviation

	# cost information
	commercial_fuel_price_electric = np.array(df_in["industry_and_mining_fuel_price_electric"])
	commercial_fuel_price_biomass = np.array(df_in["industry_and_mining_fuel_price_biomass"])
	commercial_fuel_price_pliqgas = np.array(df_in["industry_and_mining_fuel_price_pliqgas"])
	commercial_fuel_price_solar = np.array(df_in["industry_and_mining_fuel_price_solar"])
	commercial_fuel_price_hydrogen = np.array(df_in["industry_and_mining_fuel_price_hydrogen"])

	# cost information
	commercial_investment_cost_ACS_natural_gas = np.array(df_in["commercial_investment_cost_acs_natural_gas"])
	commercial_investment_cost_ACS_pliqgas = np.array(df_in["commercial_investment_cost_acs_pliqgas"])
	commercial_investment_cost_ACS_diesel = np.array(df_in["commercial_investment_cost_acs_diesel"])
	commercial_investment_cost_heating_natural_gas = np.array(df_in["commercial_investment_cost_heating_natural_gas"])
	commercial_investment_cost_heating_pliqgas = np.array(df_in["commercial_investment_cost_heating_pliqgas"])
	commercial_investment_cost_heating_diesel = np.array(df_in["commercial_investment_cost_heating_diesel"])
	commercial_investment_cost_heating_electric = np.array(df_in["commercial_investment_cost_heating_electric"])
	commercial_investment_cost_motive_electric = np.array(df_in["commercial_investment_cost_motive_electric"])
	commercial_investment_cost_other_natural_gas = np.array(df_in["commercial_investment_cost_other_natural_gas"])
	commercial_investment_cost_other_pliqgas = np.array(df_in["commercial_investment_cost_other_pliqgas"])
	commercial_investment_cost_other_diesel = np.array(df_in["commercial_investment_cost_other_diesel"])
	commercial_investment_cost_other_electric = np.array(df_in["commercial_investment_cost_other_electric"])
	commercial_investment_cost_other_biomass = np.array(df_in["commercial_investment_cost_other_biomass"])
	commercial_investment_cost_other_kerosene = np.array(df_in["commercial_investment_cost_other_kerosene"])
	commercial_investment_cost_other_gas = np.array(df_in["commercial_investment_cost_other_gas"])

	# Read input parameters defined in parameter_ranges.csv
	gdp = np.array(df_in["pib"]) * np.array(df_in["pib_scalar_transport"])
	growth_rate_gdp = np.array(df_in["gr_pib"])
	commercial_elasticity = np.array(df_in["commercial_elasticity"])
	commercial_relation_usefull_energy = np.array(df_in["commercial_relation_usefull_energy"])
	commercial_dem_ACS = np.array(df_in["commercial_dem_acs"])
	commercial_dem_heating = np.array(df_in["commercial_dem_heating"])
	commercial_dem_motive = np.array(df_in["commercial_dem_motive"])
	commercial_dem_other = np.array(df_in["commercial_dem_other"])
	commercial_activity_ACS = np.array(df_in["commercial_activity_acs"])
	commercial_activity_heating = np.array(df_in["commercial_activity_heating"])
	commercial_activity_motive = np.array(df_in["commercial_activity_motive"])
	commercial_activity_other = np.array(df_in["commercial_activity_other"])
	commercial_ACS_natural_gas = np.array(df_in["commercial_acs_natural_gas"])
	commercial_ACS_pliqgas = np.array(df_in["commercial_acs_pliqgas"])
	commercial_ACS_diesel = np.array(df_in["commercial_acs_diesel"])
	commercial_heating_natural_gas = np.array(df_in["commercial_heating_natural_gas"])
	commercial_heating_pliqgas = np.array(df_in["commercial_heating_pliqgas"])
	commercial_heating_diesel = np.array(df_in["commercial_heating_diesel"])
	commercial_heating_electric = np.array(df_in["commercial_heating_electric"])
	commercial_motive_electric = np.array(df_in["commercial_motive_electric"])
	commercial_other_natural_gas = np.array(df_in["commercial_other_natural_gas"])
	commercial_other_pliqgas = np.array(df_in["commercial_other_pliqgas"])
	commercial_other_diesel = np.array(df_in["commercial_other_diesel"])
	commercial_other_electric = np.array(df_in["commercial_other_electric"])
	commercial_other_biomass = np.array(df_in["commercial_other_biomass"])
	commercial_other_kerosene = np.array(df_in["commercial_other_kerosene"])
	commercial_other_gas = np.array(df_in["commercial_other_gas"])
	commercial_other_hydrogen = np.array(df_in["commercial_other_hydrogen"])
	commercial_efficiency_ACS_natural_gas = np.array(df_in["commercial_efficiency_acs_natural_gas"])
	commercial_efficiency_ACS_pliqgas = np.array(df_in["commercial_efficiency_acs_pliqgas"])
	commercial_efficiency_ACS_diesel = np.array(df_in["commercial_efficiency_acs_diesel"])
	commercial_efficiency_heating_natural_gas = np.array(df_in["commercial_efficiency_heating_natural_gas"])
	commercial_efficiency_heating_pliqgas = np.array(df_in["commercial_efficiency_heating_pliqgas"])
	commercial_efficiency_heating_diesel = np.array(df_in["commercial_efficiency_heating_diesel"])
	commercial_efficiency_heating_electric = np.array(df_in["commercial_efficiency_heating_electric"])
	commercial_efficiency_motive_electric = np.array(df_in["commercial_efficiency_motive_electric"])
	commercial_efficiency_other_natural_gas = np.array(df_in["commercial_efficiency_other_natural_gas"])
	commercial_efficiency_other_pliqgas = np.array(df_in["commercial_efficiency_other_pliqgas"])
	commercial_efficiency_other_diesel = np.array(df_in["commercial_efficiency_other_diesel"])
	commercial_efficiency_other_electric = np.array(df_in["commercial_efficiency_other_electric"])
	commercial_efficiency_other_biomass = np.array(df_in["commercial_efficiency_other_biomass"])
	commercial_efficiency_other_kerosene = np.array(df_in["commercial_efficiency_other_kerosene"])
	commercial_efficiency_other_gas = np.array(df_in["commercial_efficiency_other_gas"])
	commercial_efficiency_other_hydrogen = np.array(df_in["commercial_efficiency_other_hydrogen"])
	commercial_emission_fact_diesel = np.array(df_in["commercial_emission_fact_diesel"])
	commercial_emission_fact_natural_gas = np.array(df_in["commercial_emission_fact_natural_gas"])
	commercial_emission_fact_pliqgas = np.array(df_in["commercial_emission_fact_pliqgas"])
	commercial_emission_fact_kerosene = np.array(df_in["commercial_emission_fact_kerosene"])


	# calculate demand in Tcal as function of GDP
	# commercial_demand = np.exp(alfa+beta*np.log(gdp))
	year = np.array(df_in["year"])  # vector years
	commercial_demand = model_commercial(year, growth_rate_gdp, commercial_elasticity)
	commercial_useful_demand = commercial_demand*commercial_relation_usefull_energy

	commercial_dem_ACS_natural_gas = commercial_useful_demand * commercial_dem_ACS * commercial_ACS_natural_gas / commercial_efficiency_ACS_natural_gas
	commercial_dem_ACS_pliqgas = commercial_useful_demand * commercial_dem_ACS * commercial_ACS_pliqgas / commercial_efficiency_ACS_pliqgas
	commercial_dem_ACS_diesel = commercial_useful_demand * commercial_dem_ACS * commercial_ACS_diesel / commercial_efficiency_ACS_diesel
	commercial_dem_heating_natural_gas = commercial_useful_demand * commercial_dem_heating * commercial_heating_natural_gas / commercial_efficiency_heating_natural_gas
	commercial_dem_heating_pliqgas = commercial_useful_demand * commercial_dem_heating * commercial_heating_pliqgas / commercial_efficiency_heating_pliqgas
	commercial_dem_heating_diesel = commercial_useful_demand * commercial_dem_heating * commercial_heating_diesel / commercial_efficiency_heating_diesel
	commercial_dem_heating_electric = commercial_useful_demand * commercial_dem_heating * commercial_heating_electric / commercial_efficiency_heating_electric
	commercial_dem_motive_electric = commercial_useful_demand * commercial_dem_motive * commercial_motive_electric / commercial_efficiency_motive_electric
	commercial_dem_other_natural_gas = commercial_useful_demand * commercial_dem_other * commercial_other_natural_gas / commercial_efficiency_other_natural_gas
	commercial_dem_other_pliqgas = commercial_useful_demand * commercial_dem_other * commercial_other_pliqgas / commercial_efficiency_other_pliqgas
	commercial_dem_other_diesel = commercial_useful_demand * commercial_dem_other * commercial_other_diesel / commercial_efficiency_other_diesel
	commercial_dem_other_electric = commercial_useful_demand * commercial_dem_other * commercial_other_electric / commercial_efficiency_other_electric
	commercial_dem_other_biomass = commercial_useful_demand * commercial_dem_other * commercial_other_biomass / commercial_efficiency_other_biomass
	commercial_dem_other_kerosene = commercial_useful_demand * commercial_dem_other * commercial_other_kerosene / commercial_efficiency_other_kerosene
	commercial_dem_other_gas = commercial_useful_demand * commercial_dem_other * commercial_other_gas / commercial_efficiency_other_gas
	commercial_dem_other_hydrogen = commercial_useful_demand * commercial_dem_other * commercial_other_hydrogen / commercial_efficiency_other_hydrogen

	commercial_dem_natural_gas = commercial_dem_ACS_natural_gas+commercial_dem_heating_natural_gas+commercial_dem_other_natural_gas
	commercial_dem_pliqgas = commercial_dem_ACS_pliqgas+commercial_dem_heating_pliqgas+commercial_dem_other_pliqgas
	commercial_dem_diesel = commercial_dem_ACS_diesel+commercial_dem_heating_diesel+commercial_dem_other_diesel
	commercial_dem_electric = commercial_dem_heating_electric+commercial_dem_motive_electric+commercial_dem_other_electric
	commercial_dem_biomass = commercial_dem_other_biomass
	commercial_dem_kerosene = commercial_dem_other_kerosene
	commercial_dem_other_gas = commercial_dem_other_gas
	commercial_dem_hydrogen = commercial_dem_other_hydrogen

	# calculate emission in millon tCO2
	commercial_emission_diesel = commercial_dem_diesel * fact * commercial_emission_fact_diesel / (10 ** 9)
	commercial_emission_natural_gas = commercial_dem_natural_gas * fact * commercial_emission_fact_natural_gas / (10 ** 9)
	commercial_emission_pliqgas = commercial_dem_pliqgas * fact * commercial_emission_fact_pliqgas / (10 ** 9)
	commercial_emission_kerosene = commercial_dem_kerosene * fact * commercial_emission_fact_kerosene / (10 ** 9)

	commercial_emission = commercial_emission_diesel + commercial_emission_natural_gas + commercial_emission_pliqgas + commercial_emission_kerosene

	# electric demand to produce hydrogen
	electric_demand_hydrogen = commercial_dem_hydrogen / electrolyzer_efficiency * share_electric_grid_to_hydrogen
	electric_demand_hydrogen = electric_demand_hydrogen * fact2

	#############################################################################
	################# COST INFORMATION ##########################################
	#capacity
	commercial_capacity_ACS_natural_gas = commercial_dem_ACS_natural_gas * fact2 * (10 ** 3) / commercial_activity_ACS
	commercial_capacity_ACS_pliqgas = commercial_dem_ACS_pliqgas * fact2 * (10 ** 3) / commercial_activity_ACS
	commercial_capacity_ACS_diesel = commercial_dem_ACS_diesel * fact2 * (10 ** 3) / commercial_activity_ACS
	commercial_capacity_heating_natural_gas = commercial_dem_heating_natural_gas * fact2 * (10 ** 3) / commercial_activity_heating
	commercial_capacity_heating_pliqgas = commercial_dem_heating_pliqgas * fact2 * (10 ** 3) / commercial_activity_heating
	commercial_capacity_heating_diesel = commercial_dem_heating_diesel * fact2 * (10 ** 3) / commercial_activity_heating
	commercial_capacity_heating_electric = commercial_dem_heating_electric * fact2 * (10 ** 3) / commercial_activity_heating
	commercial_capacity_motive_electric = commercial_dem_motive_electric * fact2 * (10 ** 3) / commercial_activity_motive
	commercial_capacity_other_natural_gas = commercial_dem_other_natural_gas * fact2 * (10 ** 3) / commercial_activity_other
	commercial_capacity_other_pliqgas = commercial_dem_other_pliqgas * fact2 * (10 ** 3) / commercial_activity_other
	commercial_capacity_other_diesel = commercial_dem_other_diesel * fact2 * (10 ** 3) / commercial_activity_other
	commercial_capacity_other_electric = commercial_dem_other_electric * fact2 * (10 ** 3) / commercial_activity_other
	commercial_capacity_other_biomass = commercial_dem_other_biomass * fact2 * (10 ** 3) / commercial_activity_other
	commercial_capacity_other_kerosene = commercial_dem_other_kerosene * fact2 * (10 ** 3) / commercial_activity_other
	commercial_capacity_other_gas = commercial_dem_other_gas * fact2 * (10 ** 3) /commercial_activity_other

	commercial_capacity_ACS_natural_gas = model_capacity(year, commercial_capacity_ACS_natural_gas)
	commercial_capacity_ACS_pliqgas = model_capacity(year, commercial_capacity_ACS_pliqgas)
	commercial_capacity_ACS_diesel = model_capacity(year, commercial_capacity_ACS_diesel)
	commercial_capacity_heating_natural_gas = model_capacity(year, commercial_capacity_heating_natural_gas)
	commercial_capacity_heating_pliqgas = model_capacity(year, commercial_capacity_heating_pliqgas)
	commercial_capacity_heating_diesel = model_capacity(year, commercial_capacity_heating_diesel)
	commercial_capacity_heating_electric = model_capacity(year, commercial_capacity_heating_electric)
	commercial_capacity_motive_electric = model_capacity(year, commercial_capacity_motive_electric)
	commercial_capacity_other_natural_gas = model_capacity(year, commercial_capacity_other_natural_gas)
	commercial_capacity_other_pliqgas = model_capacity(year, commercial_capacity_other_pliqgas)
	commercial_capacity_other_diesel = model_capacity(year, commercial_capacity_other_diesel)
	commercial_capacity_other_electric = model_capacity(year, commercial_capacity_other_electric)
	commercial_capacity_other_biomass = model_capacity(year, commercial_capacity_other_biomass)
	commercial_capacity_other_kerosene = model_capacity(year, commercial_capacity_other_kerosene)
	commercial_capacity_other_gas = model_capacity(year, commercial_capacity_other_gas)

	commercial_delta_capacity_ACS_natural_gas = model_delta_capacity(year, commercial_capacity_ACS_natural_gas)
	commercial_delta_capacity_ACS_pliqgas = model_delta_capacity(year, commercial_capacity_ACS_pliqgas)
	commercial_delta_capacity_ACS_diesel = model_delta_capacity(year, commercial_capacity_ACS_diesel)
	commercial_delta_capacity_heating_natural_gas = model_delta_capacity(year, commercial_capacity_heating_natural_gas)
	commercial_delta_capacity_heating_pliqgas = model_delta_capacity(year, commercial_capacity_heating_pliqgas)
	commercial_delta_capacity_heating_diesel = model_delta_capacity(year, commercial_capacity_heating_diesel)
	commercial_delta_capacity_heating_electric = model_delta_capacity(year, commercial_capacity_heating_electric)
	commercial_delta_capacity_motive_electric = model_delta_capacity(year, commercial_capacity_motive_electric)
	commercial_delta_capacity_other_natural_gas = model_delta_capacity(year, commercial_capacity_other_natural_gas)
	commercial_delta_capacity_other_pliqgas = model_delta_capacity(year, commercial_capacity_other_pliqgas)
	commercial_delta_capacity_other_diesel = model_delta_capacity(year, commercial_capacity_other_diesel)
	commercial_delta_capacity_other_electric = model_delta_capacity(year, commercial_capacity_other_electric)
	commercial_delta_capacity_other_biomass = model_delta_capacity(year, commercial_capacity_other_biomass)
	commercial_delta_capacity_other_kerosene = model_delta_capacity(year, commercial_capacity_other_kerosene)
	commercial_delta_capacity_other_gas = model_delta_capacity(year, commercial_capacity_other_gas)

	#OPEX
	commercial_OPEX_electric = commercial_dem_electric * commercial_fuel_price_electric / (10 ** 6)
	commercial_OPEX_biomass = commercial_dem_biomass * commercial_fuel_price_biomass / (10 ** 6)
	commercial_OPEX_natural_gas = commercial_dem_natural_gas * commercial_fuel_price_natural_gas / (10 ** 6)
	commercial_OPEX_kerosene = commercial_dem_kerosene * commercial_fuel_price_kerosene / (10 ** 6)
	commercial_OPEX_pliqgas = commercial_dem_pliqgas * commercial_fuel_price_pliqgas / (10 ** 6)
	commercial_OPEX_diesel = commercial_dem_diesel * commercial_fuel_price_diesel / (10 ** 6)
	commercial_OPEX_solar = commercial_dem_other_gas * commercial_fuel_price_solar / (10 ** 6)
	commercial_OPEX_hydrogen = commercial_dem_hydrogen * commercial_fuel_price_hydrogen / (10 ** 6)
	commercial_OPEX = commercial_OPEX_electric+commercial_OPEX_biomass+commercial_OPEX_natural_gas+commercial_OPEX_kerosene+commercial_OPEX_pliqgas+commercial_OPEX_diesel+commercial_OPEX_solar+commercial_OPEX_hydrogen

	#CAPEX
	commercial_CAPEX_ACS_natural_gas = commercial_delta_capacity_ACS_natural_gas * commercial_investment_cost_ACS_natural_gas / (10 ** 3)
	commercial_CAPEX_ACS_pliqgas = commercial_delta_capacity_ACS_pliqgas * commercial_investment_cost_ACS_pliqgas / (10 ** 3)
	commercial_CAPEX_ACS_diesel = commercial_delta_capacity_ACS_diesel * commercial_investment_cost_ACS_diesel / (10 ** 3)
	commercial_CAPEX_ACS=commercial_CAPEX_ACS_natural_gas+commercial_CAPEX_ACS_pliqgas+commercial_CAPEX_ACS_diesel

	commercial_CAPEX_heating_natural_gas = commercial_delta_capacity_heating_natural_gas * commercial_investment_cost_heating_natural_gas / (10 ** 3)
	commercial_CAPEX_heating_pliqgas = commercial_delta_capacity_heating_pliqgas * commercial_investment_cost_heating_pliqgas / (10 ** 3)
	commercial_CAPEX_heating_diesel = commercial_delta_capacity_heating_diesel * commercial_investment_cost_heating_diesel / (10 ** 3)
	commercial_CAPEX_heating_electric = commercial_delta_capacity_heating_electric * commercial_investment_cost_heating_electric / (10 ** 3)
	commercial_CAPEX_heating=commercial_CAPEX_heating_natural_gas+commercial_CAPEX_heating_pliqgas+commercial_CAPEX_heating_diesel+commercial_CAPEX_heating_electric

	commercial_CAPEX_motive_electric = commercial_delta_capacity_motive_electric * commercial_investment_cost_motive_electric / (10 ** 3)
	commercial_CAPEX_motive=commercial_CAPEX_motive_electric

	commercial_CAPEX_other_natural_gas = commercial_delta_capacity_other_natural_gas * commercial_investment_cost_other_natural_gas / (10 ** 3)
	commercial_CAPEX_other_pliqgas = commercial_delta_capacity_other_pliqgas * commercial_investment_cost_other_pliqgas / (10 ** 3)
	commercial_CAPEX_other_diesel = commercial_delta_capacity_other_diesel * commercial_investment_cost_other_diesel / (10 ** 3)
	commercial_CAPEX_other_electric = commercial_delta_capacity_other_electric * commercial_investment_cost_other_electric / (10 ** 3)
	commercial_CAPEX_other_biomass = commercial_delta_capacity_other_biomass * commercial_investment_cost_other_biomass / (10 ** 3)
	commercial_CAPEX_other_kerosene = commercial_delta_capacity_other_kerosene * commercial_investment_cost_other_kerosene / (10 ** 3)
	commercial_CAPEX_other_gas = commercial_delta_capacity_other_gas * commercial_investment_cost_other_gas / (10 ** 3)
	commercial_CAPEX_other = commercial_CAPEX_other_natural_gas+commercial_CAPEX_other_pliqgas+commercial_CAPEX_other_diesel+commercial_CAPEX_other_electric+commercial_CAPEX_other_biomass +commercial_CAPEX_other_kerosene+commercial_CAPEX_other_gas

	# total CAPEX
	commercial_CAPEX =commercial_CAPEX_ACS+commercial_CAPEX_heating+commercial_CAPEX_motive+commercial_CAPEX_other


	dict_emission = {"commercial": commercial_emission}
	dict_electric_demand = {"commercial": commercial_dem_electric * fact2}
	# CAPEX, OPEX
	dict_CAPEX = {"commercial": commercial_CAPEX}
	dict_OPEX = {"commercial": commercial_OPEX}

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

	# add OPEX to master output
	for k in dict_OPEX.keys():
		# new key conveys emissions
		k_new = str(k).replace("commercial", dict_sector_abv["commercial"]) + "-OPEX-MMUSD"
		# add to output
		dict_out.update({k_new: dict_OPEX[k].copy()})

	# add CAPEX to master output
	for k in dict_CAPEX.keys():
		# new key conveys emissions
		k_new = str(k).replace("commercial", dict_sector_abv["commercial"]) + "-CAPEX-MMUSD"
		# add to output
		dict_out.update({k_new: dict_CAPEX[k].copy()})

	dict_out.update({
		(dict_sector_abv["commercial"] + "-electricity_hydrogen-gwh"): electric_demand_hydrogen,
	})

	# return
	return dict_out  # dict_emission,dict_electric_demand
