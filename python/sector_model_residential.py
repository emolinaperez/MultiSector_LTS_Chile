# Residential energy model developed by Centro de Energia U. de Chile using RAND python framework
# version 1.0 december 2020

import os, os.path
import time
import pandas as pd
import numpy as np
from econometric_models import model_delta_capacity,  model_capacity

###################
#    RESIDENTIAL    #
###################

def sm_residential(df_in, dict_sector_abv):

	# conversion factor Tcal to TJ
	fact = 4.184
	# conversion factor Tcal to GWh
	fact2 = 1.162952

	year = np.array(df_in["year"])  # vector years

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
	residential_fuel_price_diesel = fuel_price_diesel * fuel_price_diesel_conversion
	fuel_price_natural_gas = np.array(df_in["fuel_price_natural_gas"])
	residential_fuel_price_natural_gas = fuel_price_natural_gas * fuel_price_natural_gas_conversion
	fuel_price_coal = np.array(df_in["fuel_price_coal"])
	residential_fuel_price_coal = fuel_price_coal * fuel_price_coal_conversion

	fuel_price_gasoline = residential_fuel_price_diesel * ratio_fuel_price_diesel_gasoline
	fuel_price_fuel_oil = residential_fuel_price_diesel * ratio_fuel_price_diesel_fuel_oil
	fuel_price_kerosene = residential_fuel_price_diesel * ratio_fuel_price_diesel_kerosene
	fuel_price_kerosene_aviation = residential_fuel_price_diesel * ratio_fuel_price_diesel_kerosene_aviation

	residential_fuel_price_coal = fuel_price_fuel_oil
	residential_fuel_price_kerosene = fuel_price_kerosene
	residential_fuel_price_gasoline = fuel_price_gasoline
	residential_fuel_price_kerosene_aviation = fuel_price_kerosene_aviation

	# cost information
	residential_fuel_price_electric = np.array(df_in["industry_and_mining_fuel_price_electric"])
	residential_fuel_price_biomass = np.array(df_in["industry_and_mining_fuel_price_biomass"])
	residential_fuel_price_pliqgas = np.array(df_in["industry_and_mining_fuel_price_pliqgas"])
	residential_fuel_price_solar = np.array(df_in["industry_and_mining_fuel_price_solar"])
	residential_fuel_price_hydrogen = np.array(df_in["industry_and_mining_fuel_price_hydrogen"])


	residential_investment_cost_heating_electric = np.array(df_in["residential_investment_cost_heating_electric"])
	residential_investment_cost_heating_biomass = np.array(df_in["residential_investment_cost_heating_biomass"])
	residential_investment_cost_heating_natural_gas = np.array(df_in["residential_investment_cost_heating_natural_gas"])
	residential_investment_cost_heating_kerosene = np.array(df_in["residential_investment_cost_heating_kerosene"])
	residential_investment_cost_heating_pliqgas = np.array(df_in["residential_investment_cost_heating_pliqgas"])
	residential_investment_cost_heating_solar = np.array(df_in["residential_investment_cost_heating_solar"])
	residential_investment_cost_heating_hydrogen = np.array(df_in["residential_investment_cost_heating_hydrogen"])
	residential_investment_cost_cooking_electric = np.array(df_in["residential_investment_cost_cooking_electric"])
	residential_investment_cost_cooking_biomass = np.array(df_in["residential_investment_cost_cooking_biomass"])
	residential_investment_cost_cooking_natural_gas = np.array(df_in["residential_investment_cost_cooking_natural_gas"])
	residential_investment_cost_cooking_kerosene = np.array(df_in["residential_investment_cost_cooking_kerosene"])
	residential_investment_cost_cooking_pliqgas = np.array(df_in["residential_investment_cost_cooking_pliqgas"])
	residential_investment_cost_cooking_solar = np.array(df_in["residential_investment_cost_cooking_solar"])
	residential_investment_cost_cooking_hydrogen = np.array(df_in["residential_investment_cost_cooking_hydrogen"])
	residential_investment_cost_pv_solar = np.array(df_in["residential_investment_cost_pv_solar"])
	residential_investment_cost_electric_appliance = np.array(df_in["residential_investment_cost_electric_appliance"])
	residential_investment_cost_acs_electric = np.array(df_in["residential_investment_cost_acs_electric"])
	residential_investment_cost_acs_biomass = np.array(df_in["residential_investment_cost_acs_biomass"])
	residential_investment_cost_acs_natural_gas = np.array(df_in["residential_investment_cost_acs_natural_gas"])
	residential_investment_cost_acs_kerosene = np.array(df_in["residential_investment_cost_acs_kerosene"])
	residential_investment_cost_acs_pliqgas = np.array(df_in["residential_investment_cost_acs_pliqgas"])
	residential_investment_cost_acs_solar = np.array(df_in["residential_investment_cost_acs_solar"])
	residential_investment_cost_acs_hydrogen = np.array(df_in["residential_investment_cost_acs_hydrogen"])

	residential_investment_cost_retrofit_house = np.array(df_in["residential_investment_cost_retrofit_house"])
	residential_investment_cost_retrofit_apartment = np.array(df_in["residential_investment_cost_retrofit_apartment"])
	residential_retrofit_house = np.array(df_in["residential_retrofit_house"])
	residential_retrofit_apartment = np.array(df_in["residential_retrofit_apartment"])
	residential_retrofit_energy_reduction_house = np.array(df_in["residential_retrofit_energy_reduction_house"])
	residential_retrofit_energy_reduction_apartment = np.array(df_in["residential_retrofit_energy_reduction_apartment"])

	# Read input parameters defined in parameter_ranges.csv
	total_population = np.array(df_in["poblacion"])
	residential_occ_rate = np.array(df_in["residential_occ_rate"])
	residential_share_household_house = np.array(df_in["residential_share_household_house"])
	residential_share_household_apartment = np.array(df_in["residential_share_household_apartment"])
	residential_house_intensity_heating = np.array(df_in["residential_house_intensity_heating"])
	residential_house_intensity_cooking = np.array(df_in["residential_house_intensity_cooking"])
	residential_house_intensity_acs = np.array(df_in["residential_house_intensity_acs"])
	residential_house_intensity_electric_appliance = np.array(df_in["residential_house_intensity_electric_appliance"])
	residential_apartment_intensity_heating = np.array(df_in["residential_apartment_intensity_heating"])
	residential_apartment_intensity_cooking = np.array(df_in["residential_apartment_intensity_cooking"])
	residential_apartment_intensity_acs = np.array(df_in["residential_apartment_intensity_acs"])
	residential_apartment_intensity_electric_appliance = np.array(df_in["residential_apartment_intensity_electric_appliance"])
	residential_activity_heating = np.array(df_in["residential_activity_heating"])
	residential_activity_cooking = np.array(df_in["residential_activity_cooking"])
	residential_activity_acs = np.array(df_in["residential_activity_acs"])
	residential_activity_electric_appliance = np.array(df_in["residential_activity_electric_appliance"])
	residential_house_heating_electric = np.array(df_in["residential_house_heating_electric"])
	residential_house_heating_biomass = np.array(df_in["residential_house_heating_biomass"])
	residential_house_heating_natural_gas = np.array(df_in["residential_house_heating_natural_gas"])
	residential_house_heating_kerosene = np.array(df_in["residential_house_heating_kerosene"])
	residential_house_heating_pliqgas = np.array(df_in["residential_house_heating_pliqgas"])
	residential_house_heating_solar = np.array(df_in["residential_house_heating_solar"])
	residential_house_heating_hydrogen = np.array(df_in["residential_house_heating_hydrogen"])
	residential_apartment_heating_electric = np.array(df_in["residential_apartment_heating_electric"])
	residential_apartment_heating_biomass = np.array(df_in["residential_apartment_heating_biomass"])
	residential_apartment_heating_natural_gas = np.array(df_in["residential_apartment_heating_natural_gas"])
	residential_apartment_heating_kerosene = np.array(df_in["residential_apartment_heating_kerosene"])
	residential_apartment_heating_pliqgas = np.array(df_in["residential_apartment_heating_pliqgas"])
	residential_apartment_heating_solar = np.array(df_in["residential_apartment_heating_solar"])
	residential_apartment_heating_hydrogen = np.array(df_in["residential_apartment_heating_hydrogen"])
	residential_house_cooking_electric = np.array(df_in["residential_house_cooking_electric"])
	residential_house_cooking_biomass = np.array(df_in["residential_house_cooking_biomass"])
	residential_house_cooking_natural_gas = np.array(df_in["residential_house_cooking_natural_gas"])
	residential_house_cooking_kerosene = np.array(df_in["residential_house_cooking_kerosene"])
	residential_house_cooking_pliqgas = np.array(df_in["residential_house_cooking_pliqgas"])
	residential_house_cooking_solar = np.array(df_in["residential_house_cooking_solar"])
	residential_house_cooking_hydrogen = np.array(df_in["residential_house_cooking_hydrogen"])
	residential_house_acs_electric = np.array(df_in["residential_house_acs_electric"])
	residential_house_acs_biomass = np.array(df_in["residential_house_acs_biomass"])
	residential_house_acs_natural_gas = np.array(df_in["residential_house_acs_natural_gas"])
	residential_house_acs_kerosene = np.array(df_in["residential_house_acs_kerosene"])
	residential_house_acs_pliqgas = np.array(df_in["residential_house_acs_pliqgas"])
	residential_house_acs_solar = np.array(df_in["residential_house_acs_solar"])
	residential_house_acs_hydrogen = np.array(df_in["residential_house_acs_hydrogen"])
	residential_apartment_cooking_electric = np.array(df_in["residential_apartment_cooking_electric"])
	residential_apartment_cooking_biomass = np.array(df_in["residential_apartment_cooking_biomass"])
	residential_apartment_cooking_natural_gas = np.array(df_in["residential_apartment_cooking_natural_gas"])
	residential_apartment_cooking_kerosene = np.array(df_in["residential_apartment_cooking_kerosene"])
	residential_apartment_cooking_pliqgas = np.array(df_in["residential_apartment_cooking_pliqgas"])
	residential_apartment_cooking_solar = np.array(df_in["residential_apartment_cooking_solar"])
	residential_apartment_cooking_hydrogen = np.array(df_in["residential_apartment_cooking_hydrogen"])
	residential_apartment_acs_electric = np.array(df_in["residential_apartment_acs_electric"])
	residential_apartment_acs_biomass = np.array(df_in["residential_apartment_acs_biomass"])
	residential_apartment_acs_natural_gas = np.array(df_in["residential_apartment_acs_natural_gas"])
	residential_apartment_acs_kerosene = np.array(df_in["residential_apartment_acs_kerosene"])
	residential_apartment_acs_pliqgas = np.array(df_in["residential_apartment_acs_pliqgas"])
	residential_apartment_acs_solar = np.array(df_in["residential_apartment_acs_solar"])
	residential_apartment_acs_hydrogen = np.array(df_in["residential_apartment_acs_hydrogen"])
	residential_efficiency_heating_electric = np.array(df_in["residential_efficiency_heating_electric"])
	residential_efficiency_heating_biomass = np.array(df_in["residential_efficiency_heating_biomass"])
	residential_efficiency_heating_natural_gas = np.array(df_in["residential_efficiency_heating_natural_gas"])
	residential_efficiency_heating_kerosene = np.array(df_in["residential_efficiency_heating_kerosene"])
	residential_efficiency_heating_pliqgas = np.array(df_in["residential_efficiency_heating_pliqgas"])
	residential_efficiency_heating_solar = np.array(df_in["residential_efficiency_heating_solar"])
	residential_efficiency_heating_hydrogen = np.array(df_in["residential_efficiency_heating_hydrogen"])
	residential_efficiency_cooking_electric = np.array(df_in["residential_efficiency_cooking_electric"])
	residential_efficiency_cooking_biomass = np.array(df_in["residential_efficiency_cooking_biomass"])
	residential_efficiency_cooking_natural_gas = np.array(df_in["residential_efficiency_cooking_natural_gas"])
	residential_efficiency_cooking_kerosene = np.array(df_in["residential_efficiency_cooking_kerosene"])
	residential_efficiency_cooking_pliqgas = np.array(df_in["residential_efficiency_cooking_pliqgas"])
	residential_efficiency_cooking_solar = np.array(df_in["residential_efficiency_cooking_solar"])
	residential_efficiency_cooking_hydrogen = np.array(df_in["residential_efficiency_cooking_hydrogen"])
	residential_efficiency_acs_electric = np.array(df_in["residential_efficiency_acs_electric"])
	residential_efficiency_acs_biomass = np.array(df_in["residential_efficiency_acs_biomass"])
	residential_efficiency_acs_natural_gas = np.array(df_in["residential_efficiency_acs_natural_gas"])
	residential_efficiency_acs_kerosene = np.array(df_in["residential_efficiency_acs_kerosene"])
	residential_efficiency_acs_pliqgas = np.array(df_in["residential_efficiency_acs_pliqgas"])
	residential_efficiency_acs_solar = np.array(df_in["residential_efficiency_acs_solar"])
	residential_efficiency_acs_hydrogen = np.array(df_in["residential_efficiency_acs_hydrogen"])
	residential_efficiency_electric_appliance = np.array(df_in["residential_efficiency_electric_appliance"])
	residential_emission_fact_natural_gas = np.array(df_in["residential_emission_fact_natural_gas"])
	residential_emission_fact_kerosene = np.array(df_in["residential_emission_fact_kerosene"])
	residential_emission_fact_pliqgas = np.array(df_in["residential_emission_fact_pliqgas"])

	#number of households by type
	residential_house = total_population / residential_occ_rate * residential_share_household_house
	residential_apartment = total_population / residential_occ_rate * residential_share_household_apartment

	residential_house_intensity_heating_with_retrofit = ((residential_house - residential_retrofit_house)*residential_house_intensity_heating+residential_retrofit_house*(1-residential_retrofit_energy_reduction_house))/residential_house
	residential_apartment_intensity_heating_with_retrofit = ((residential_apartment - residential_retrofit_apartment) * residential_apartment_intensity_heating + residential_retrofit_apartment * (1 - residential_retrofit_energy_reduction_apartment))/residential_apartment

	residential_retrofit_house_additional = model_delta_capacity(year, residential_retrofit_house)
	residential_retrofit_apartment_additional= model_delta_capacity(year, residential_retrofit_apartment)

	#demand
	#heating
	residential_dem_house_heating_electric = residential_house*residential_house_intensity_heating_with_retrofit*residential_house_heating_electric/residential_efficiency_heating_electric/1000
	residential_dem_house_heating_biomass = residential_house*residential_house_intensity_heating_with_retrofit*residential_house_heating_biomass/residential_efficiency_heating_biomass/1000
	residential_dem_house_heating_natural_gas = residential_house*residential_house_intensity_heating_with_retrofit*residential_house_heating_natural_gas/residential_efficiency_heating_natural_gas/1000
	residential_dem_house_heating_kerosene = residential_house*residential_house_intensity_heating_with_retrofit*residential_house_heating_kerosene/residential_efficiency_heating_kerosene/1000
	residential_dem_house_heating_pliqgas = residential_house*residential_house_intensity_heating_with_retrofit*residential_house_heating_pliqgas/residential_efficiency_heating_pliqgas/1000
	residential_dem_house_heating_solar = residential_house*residential_house_intensity_heating_with_retrofit*residential_house_heating_solar/residential_efficiency_heating_solar/1000
	residential_dem_house_heating_hydrogen = residential_house*residential_house_intensity_heating_with_retrofit*residential_house_heating_hydrogen/residential_efficiency_heating_hydrogen/1000
	residential_dem_apartment_heating_electric = residential_apartment * residential_apartment_intensity_heating_with_retrofit * residential_apartment_heating_electric / residential_efficiency_heating_electric / 1000
	residential_dem_apartment_heating_biomass = residential_apartment * residential_apartment_intensity_heating_with_retrofit * residential_apartment_heating_biomass / residential_efficiency_heating_biomass / 1000
	residential_dem_apartment_heating_natural_gas = residential_apartment * residential_apartment_intensity_heating_with_retrofit * residential_apartment_heating_natural_gas / residential_efficiency_heating_natural_gas / 1000
	residential_dem_apartment_heating_kerosene = residential_apartment * residential_apartment_intensity_heating_with_retrofit * residential_apartment_heating_kerosene / residential_efficiency_heating_kerosene / 1000
	residential_dem_apartment_heating_pliqgas = residential_apartment * residential_apartment_intensity_heating_with_retrofit * residential_apartment_heating_pliqgas / residential_efficiency_heating_pliqgas / 1000
	residential_dem_apartment_heating_solar = residential_apartment * residential_apartment_intensity_heating_with_retrofit * residential_apartment_heating_solar / residential_efficiency_heating_solar / 1000
	residential_dem_apartment_heating_hydrogen = residential_apartment * residential_apartment_intensity_heating_with_retrofit * residential_apartment_heating_hydrogen / residential_efficiency_heating_hydrogen / 1000

	residential_dem_heating_electric = residential_dem_house_heating_electric+residential_dem_apartment_heating_electric
	residential_dem_heating_biomass = residential_dem_house_heating_biomass+residential_dem_apartment_heating_biomass
	residential_dem_heating_natural_gas = residential_dem_house_heating_natural_gas+residential_dem_apartment_heating_natural_gas
	residential_dem_heating_kerosene = residential_dem_house_heating_kerosene+residential_dem_apartment_heating_kerosene
	residential_dem_heating_pliqgas = residential_dem_house_heating_pliqgas+residential_dem_apartment_heating_pliqgas
	residential_dem_heating_solar = residential_dem_house_heating_solar+residential_dem_apartment_heating_solar
	residential_dem_heating_hydrogen = residential_dem_house_heating_hydrogen+residential_dem_apartment_heating_hydrogen

	#cooking
	residential_dem_house_cooking_electric = residential_house*residential_house_intensity_cooking*residential_house_cooking_electric/residential_efficiency_cooking_electric/1000
	residential_dem_house_cooking_biomass = residential_house*residential_house_intensity_cooking*residential_house_cooking_biomass/residential_efficiency_cooking_biomass/1000
	residential_dem_house_cooking_natural_gas = residential_house*residential_house_intensity_cooking*residential_house_cooking_natural_gas/residential_efficiency_cooking_natural_gas/1000
	residential_dem_house_cooking_kerosene = residential_house*residential_house_intensity_cooking*residential_house_cooking_kerosene/residential_efficiency_cooking_kerosene/1000
	residential_dem_house_cooking_pliqgas = residential_house*residential_house_intensity_cooking*residential_house_cooking_pliqgas/residential_efficiency_cooking_pliqgas/1000
	residential_dem_house_cooking_solar = residential_house*residential_house_intensity_cooking*residential_house_cooking_solar/residential_efficiency_cooking_solar/1000
	residential_dem_house_cooking_hydrogen = residential_house*residential_house_intensity_cooking*residential_house_cooking_hydrogen/residential_efficiency_cooking_hydrogen/1000
	residential_dem_apartment_cooking_electric = residential_apartment*residential_apartment_intensity_cooking*residential_apartment_cooking_electric/residential_efficiency_cooking_electric/1000
	residential_dem_apartment_cooking_biomass = residential_apartment*residential_apartment_intensity_cooking*residential_apartment_cooking_biomass/residential_efficiency_cooking_biomass/1000
	residential_dem_apartment_cooking_natural_gas = residential_apartment*residential_apartment_intensity_cooking*residential_apartment_cooking_natural_gas/residential_efficiency_cooking_natural_gas/1000
	residential_dem_apartment_cooking_kerosene = residential_apartment*residential_apartment_intensity_cooking*residential_apartment_cooking_kerosene/residential_efficiency_cooking_kerosene/1000
	residential_dem_apartment_cooking_pliqgas = residential_apartment*residential_apartment_intensity_cooking*residential_apartment_cooking_pliqgas/residential_efficiency_cooking_pliqgas/1000
	residential_dem_apartment_cooking_solar = residential_apartment*residential_apartment_intensity_cooking*residential_apartment_cooking_solar/residential_efficiency_cooking_solar/1000
	residential_dem_apartment_cooking_hydrogen = residential_apartment*residential_apartment_intensity_cooking*residential_apartment_cooking_hydrogen/residential_efficiency_cooking_hydrogen/1000

	residential_dem_cooking_electric = residential_dem_house_cooking_electric+residential_dem_apartment_cooking_electric
	residential_dem_cooking_biomass = residential_dem_house_cooking_biomass+residential_dem_apartment_cooking_biomass
	residential_dem_cooking_natural_gas = residential_dem_house_cooking_natural_gas+residential_dem_apartment_cooking_natural_gas
	residential_dem_cooking_kerosene = residential_dem_house_cooking_kerosene+residential_dem_apartment_cooking_kerosene
	residential_dem_cooking_pliqgas = residential_dem_house_cooking_pliqgas+residential_dem_apartment_cooking_pliqgas
	residential_dem_cooking_solar = residential_dem_house_cooking_solar+residential_dem_apartment_cooking_solar
	residential_dem_cooking_hydrogen = residential_dem_house_cooking_hydrogen+residential_dem_apartment_cooking_hydrogen

	#ACS
	residential_dem_house_acs_electric = residential_house*residential_house_intensity_acs*residential_house_acs_electric/residential_efficiency_acs_electric/1000
	residential_dem_house_acs_biomass = residential_house*residential_house_intensity_acs*residential_house_acs_biomass/residential_efficiency_acs_biomass/1000
	residential_dem_house_acs_natural_gas = residential_house*residential_house_intensity_acs*residential_house_acs_natural_gas/residential_efficiency_acs_natural_gas/1000
	residential_dem_house_acs_kerosene = residential_house*residential_house_intensity_acs*residential_house_acs_kerosene/residential_efficiency_acs_kerosene/1000
	residential_dem_house_acs_pliqgas = residential_house*residential_house_intensity_acs*residential_house_acs_pliqgas/residential_efficiency_acs_pliqgas/1000
	residential_dem_house_acs_solar = residential_house*residential_house_intensity_acs*residential_house_acs_solar/residential_efficiency_acs_solar/1000
	residential_dem_house_acs_hydrogen = residential_house*residential_house_intensity_acs*residential_house_acs_hydrogen/residential_efficiency_acs_hydrogen/1000
	residential_dem_apartment_acs_electric = residential_apartment*residential_apartment_intensity_acs*residential_apartment_acs_electric/residential_efficiency_acs_electric/1000
	residential_dem_apartment_acs_biomass = residential_apartment*residential_apartment_intensity_acs*residential_apartment_acs_biomass/residential_efficiency_acs_biomass/1000
	residential_dem_apartment_acs_natural_gas = residential_apartment*residential_apartment_intensity_acs*residential_apartment_acs_natural_gas/residential_efficiency_acs_natural_gas/1000
	residential_dem_apartment_acs_kerosene = residential_apartment*residential_apartment_intensity_acs*residential_apartment_acs_kerosene/residential_efficiency_acs_kerosene/1000
	residential_dem_apartment_acs_pliqgas = residential_apartment*residential_apartment_intensity_acs*residential_apartment_acs_pliqgas/residential_efficiency_acs_pliqgas/1000
	residential_dem_apartment_acs_solar = residential_apartment*residential_apartment_intensity_acs*residential_apartment_acs_solar/residential_efficiency_acs_solar/1000
	residential_dem_apartment_acs_hydrogen = residential_apartment*residential_apartment_intensity_acs*residential_apartment_acs_hydrogen/residential_efficiency_acs_hydrogen/1000

	residential_dem_acs_electric = residential_dem_house_acs_electric+residential_dem_apartment_acs_electric
	residential_dem_acs_biomass = residential_dem_house_acs_biomass+residential_dem_apartment_acs_biomass
	residential_dem_acs_natural_gas = residential_dem_house_acs_natural_gas+residential_dem_apartment_acs_natural_gas
	residential_dem_acs_kerosene = residential_dem_house_acs_kerosene+residential_dem_apartment_acs_kerosene
	residential_dem_acs_pliqgas = residential_dem_house_acs_pliqgas+residential_dem_apartment_acs_pliqgas
	residential_dem_acs_solar = residential_dem_house_acs_solar+residential_dem_apartment_acs_solar
	residential_dem_acs_hydrogen = residential_dem_house_acs_hydrogen+residential_dem_apartment_acs_hydrogen

	#other electric appliances
	residential_dem_house_electric_appliance = residential_house*residential_house_intensity_electric_appliance/residential_efficiency_electric_appliance/1000
	residential_dem_apartment_electric_appliance = residential_apartment*residential_apartment_intensity_electric_appliance/residential_efficiency_electric_appliance/1000

	residential_dem_electric_appliance_electric = residential_dem_house_electric_appliance+residential_dem_apartment_electric_appliance

	#total demand
	residential_dem_electric = residential_dem_heating_electric+residential_dem_cooking_electric+residential_dem_acs_electric+residential_dem_electric_appliance_electric
	residential_dem_biomass = residential_dem_heating_biomass+residential_dem_cooking_biomass+residential_dem_acs_biomass
	residential_dem_natural_gas = residential_dem_heating_natural_gas+residential_dem_cooking_natural_gas+residential_dem_acs_natural_gas
	residential_dem_kerosene = residential_dem_heating_kerosene+residential_dem_cooking_kerosene+residential_dem_acs_kerosene
	residential_dem_pliqgas = residential_dem_heating_pliqgas+residential_dem_cooking_pliqgas+residential_dem_acs_pliqgas
	residential_dem_solar = residential_dem_heating_solar+residential_dem_cooking_solar+residential_dem_acs_solar
	residential_dem_hydrogen = residential_dem_heating_hydrogen+residential_dem_cooking_hydrogen+residential_dem_acs_hydrogen

	# calculate emission in millon tCO2
	residential_emission_natural_gas = residential_dem_natural_gas * fact * residential_emission_fact_natural_gas / (10 ** 9)
	residential_emission_kerosene = residential_dem_kerosene * fact * residential_emission_fact_kerosene / (10 ** 9)
	residential_emission_pliqgas = residential_dem_pliqgas * fact * residential_emission_fact_pliqgas / (10 ** 9)
	residential_emission = residential_emission_natural_gas + residential_emission_kerosene+residential_emission_pliqgas
	###############################COST INFORMATION####################################################################
    # capacity
	residential_capacity_heating_electric = residential_dem_heating_electric*fact2 * (10**3) /residential_activity_heating
	residential_capacity_heating_biomass = residential_dem_heating_biomass*fact2 * (10**3) /residential_activity_heating
	residential_capacity_heating_natural_gas = residential_dem_heating_natural_gas*fact2 * (10**3) /residential_activity_heating
	residential_capacity_heating_kerosene = residential_dem_heating_kerosene*fact2 * (10**3) /residential_activity_heating
	residential_capacity_heating_pliqgas = residential_dem_heating_pliqgas*fact2 * (10**3) /residential_activity_heating
	residential_capacity_heating_solar = residential_dem_heating_solar*fact2 * (10**3) /residential_activity_heating
	residential_capacity_heating_hydrogen = residential_dem_heating_hydrogen*fact2 * (10**3) /residential_activity_heating

	residential_capacity_cooking_electric = residential_dem_cooking_electric*fact2 * (10**3) /residential_activity_cooking
	residential_capacity_cooking_biomass = residential_dem_cooking_biomass*fact2 * (10**3) /residential_activity_cooking
	residential_capacity_cooking_natural_gas = residential_dem_cooking_natural_gas*fact2 * (10**3) /residential_activity_cooking
	residential_capacity_cooking_kerosene = residential_dem_cooking_kerosene*fact2 * (10**3) /residential_activity_cooking
	residential_capacity_cooking_pliqgas = residential_dem_cooking_pliqgas*fact2 * (10**3) /residential_activity_cooking
	residential_capacity_cooking_solar = residential_dem_cooking_solar*fact2 * (10**3) /residential_activity_cooking
	residential_capacity_cooking_hydrogen = residential_dem_cooking_hydrogen*fact2 * (10**3) /residential_activity_cooking

	residential_capacity_acs_electric = residential_dem_acs_electric*fact2 * (10**3) /residential_activity_acs
	residential_capacity_acs_biomass = residential_dem_acs_biomass*fact2 * (10**3) /residential_activity_acs
	residential_capacity_acs_natural_gas = residential_dem_acs_natural_gas*fact2 * (10**3) /residential_activity_acs
	residential_capacity_acs_kerosene = residential_dem_acs_kerosene*fact2 * (10**3) /residential_activity_acs
	residential_capacity_acs_pliqgas = residential_dem_acs_pliqgas*fact2 * (10**3) /residential_activity_acs
	residential_capacity_acs_solar = residential_dem_acs_solar*fact2 * (10**3) /residential_activity_acs
	residential_capacity_acs_hydrogen = residential_dem_acs_hydrogen*fact2 * (10**3) /residential_activity_acs

	residential_capacity_electric_appliance_electric = residential_dem_electric_appliance_electric*fact2 * (10**3) /residential_activity_electric_appliance

	residential_capacity_heating_electric =  model_capacity (year,residential_capacity_heating_electric)
	residential_capacity_heating_biomass =  model_capacity (year,residential_capacity_heating_biomass)
	residential_capacity_heating_natural_gas =  model_capacity (year,residential_capacity_heating_natural_gas)
	residential_capacity_heating_kerosene =  model_capacity (year,residential_capacity_heating_kerosene)
	residential_capacity_heating_pliqgas =  model_capacity (year,residential_capacity_heating_pliqgas)
	residential_capacity_heating_solar =  model_capacity (year,residential_capacity_heating_solar)
	residential_capacity_heating_hydrogen =  model_capacity (year,residential_capacity_heating_hydrogen)

	residential_capacity_cooking_electric =  model_capacity (year,residential_capacity_cooking_electric)
	residential_capacity_cooking_biomass =  model_capacity (year,residential_capacity_cooking_biomass)
	residential_capacity_cooking_natural_gas =  model_capacity (year,residential_capacity_cooking_natural_gas)
	residential_capacity_cooking_kerosene =  model_capacity (year,residential_capacity_cooking_kerosene)
	residential_capacity_cooking_pliqgas =  model_capacity (year,residential_capacity_cooking_pliqgas)
	residential_capacity_cooking_solar =  model_capacity (year,residential_capacity_cooking_solar)
	residential_capacity_cooking_hydrogen =  model_capacity (year,residential_capacity_cooking_hydrogen)
	residential_capacity_acs_electric =  model_capacity (year,residential_capacity_acs_electric)
	residential_capacity_acs_biomass =  model_capacity (year,residential_capacity_acs_biomass)
	residential_capacity_acs_natural_gas =  model_capacity (year,residential_capacity_acs_natural_gas)
	residential_capacity_acs_kerosene =  model_capacity (year,residential_capacity_acs_kerosene)
	residential_capacity_acs_pliqgas =  model_capacity (year,residential_capacity_acs_pliqgas)
	residential_capacity_acs_solar =  model_capacity (year,residential_capacity_acs_solar)
	residential_capacity_acs_hydrogen =  model_capacity (year,residential_capacity_acs_hydrogen)

	residential_capacity_electric_appliance_electric =  model_capacity (year,residential_capacity_electric_appliance_electric)

	residential_delta_capacity_heating_electric =  model_delta_capacity (year,residential_capacity_heating_electric)
	residential_delta_capacity_heating_biomass =  model_delta_capacity (year,residential_capacity_heating_biomass)
	residential_delta_capacity_heating_natural_gas =  model_delta_capacity (year,residential_capacity_heating_natural_gas)
	residential_delta_capacity_heating_kerosene =  model_delta_capacity (year,residential_capacity_heating_kerosene)
	residential_delta_capacity_heating_pliqgas =  model_delta_capacity (year,residential_capacity_heating_pliqgas)
	residential_delta_capacity_heating_solar =  model_delta_capacity (year,residential_capacity_heating_solar)
	residential_delta_capacity_heating_hydrogen =  model_delta_capacity (year,residential_capacity_heating_hydrogen)
	residential_delta_capacity_cooking_electric =  model_delta_capacity (year,residential_capacity_cooking_electric)
	residential_delta_capacity_cooking_biomass =  model_delta_capacity (year,residential_capacity_cooking_biomass)
	residential_delta_capacity_cooking_natural_gas =  model_delta_capacity (year,residential_capacity_cooking_natural_gas)
	residential_delta_capacity_cooking_kerosene =  model_delta_capacity (year,residential_capacity_cooking_kerosene)
	residential_delta_capacity_cooking_pliqgas =  model_delta_capacity (year,residential_capacity_cooking_pliqgas)
	residential_delta_capacity_cooking_solar =  model_delta_capacity (year,residential_capacity_cooking_solar)
	residential_delta_capacity_cooking_hydrogen =  model_delta_capacity (year,residential_capacity_cooking_hydrogen)
	residential_delta_capacity_acs_electric =  model_delta_capacity (year,residential_capacity_acs_electric)
	residential_delta_capacity_acs_biomass =  model_delta_capacity (year,residential_capacity_acs_biomass)
	residential_delta_capacity_acs_natural_gas =  model_delta_capacity (year,residential_capacity_acs_natural_gas)
	residential_delta_capacity_acs_kerosene =  model_delta_capacity (year,residential_capacity_acs_kerosene)
	residential_delta_capacity_acs_pliqgas =  model_delta_capacity (year,residential_capacity_acs_pliqgas)
	residential_delta_capacity_acs_solar =  model_delta_capacity (year,residential_capacity_acs_solar)
	residential_delta_capacity_acs_hydrogen =  model_delta_capacity (year,residential_capacity_acs_hydrogen)
	residential_delta_capacity_electric_appliance_electric =  model_delta_capacity (year,residential_capacity_electric_appliance_electric)

	# OPEX
	residential_OPEX_electric = residential_dem_electric*residential_fuel_price_electric/(10**6)
	residential_OPEX_biomass = residential_dem_biomass*residential_fuel_price_biomass/(10**6)
	residential_OPEX_natural_gas = residential_dem_natural_gas*residential_fuel_price_natural_gas/(10**6)
	residential_OPEX_kerosene = residential_dem_kerosene*residential_fuel_price_kerosene/(10**6)
	residential_OPEX_pliqgas = residential_dem_pliqgas*residential_fuel_price_pliqgas/(10**6)
	residential_OPEX_solar = residential_dem_solar*residential_fuel_price_solar/(10**6)
	residential_OPEX_hydrogen = residential_dem_hydrogen*residential_fuel_price_hydrogen/(10**6)
	#total OPEX
	residential_OPEX = residential_OPEX_electric+residential_OPEX_biomass+residential_OPEX_natural_gas+residential_OPEX_kerosene+residential_OPEX_pliqgas+residential_OPEX_solar+residential_OPEX_hydrogen

	#CAPEX
	residential_CAPEX_heating_electric = residential_delta_capacity_heating_electric*residential_investment_cost_heating_electric/(10**3)
	residential_CAPEX_heating_biomass = residential_delta_capacity_heating_biomass*residential_investment_cost_heating_biomass/(10**3)
	residential_CAPEX_heating_natural_gas = residential_delta_capacity_heating_natural_gas*residential_investment_cost_heating_natural_gas/(10**3)
	residential_CAPEX_heating_kerosene = residential_delta_capacity_heating_kerosene*residential_investment_cost_heating_kerosene/(10**3)
	residential_CAPEX_heating_pliqgas = residential_delta_capacity_heating_pliqgas*residential_investment_cost_heating_pliqgas/(10**3)
	residential_CAPEX_heating_solar = residential_delta_capacity_heating_solar*residential_investment_cost_heating_solar/(10**3)
	residential_CAPEX_heating_hydrogen = residential_delta_capacity_heating_hydrogen*residential_investment_cost_heating_hydrogen/(10**3)
	residential_CAPEX_heating = residential_CAPEX_heating_electric+residential_CAPEX_heating_biomass+residential_CAPEX_heating_natural_gas+residential_CAPEX_heating_kerosene+residential_CAPEX_heating_pliqgas+residential_CAPEX_heating_solar+residential_CAPEX_heating_hydrogen

	residential_CAPEX_cooking_electric = residential_delta_capacity_cooking_electric*residential_investment_cost_cooking_electric/(10**3)
	residential_CAPEX_cooking_biomass = residential_delta_capacity_cooking_biomass*residential_investment_cost_cooking_biomass/(10**3)
	residential_CAPEX_cooking_natural_gas = residential_delta_capacity_cooking_natural_gas*residential_investment_cost_cooking_natural_gas/(10**3)
	residential_CAPEX_cooking_kerosene = residential_delta_capacity_cooking_kerosene*residential_investment_cost_cooking_kerosene/(10**3)
	residential_CAPEX_cooking_pliqgas = residential_delta_capacity_cooking_pliqgas*residential_investment_cost_cooking_pliqgas/(10**3)
	residential_CAPEX_cooking_solar = residential_delta_capacity_cooking_solar*residential_investment_cost_cooking_solar/(10**3)
	residential_CAPEX_cooking_hydrogen = residential_delta_capacity_cooking_hydrogen*residential_investment_cost_cooking_hydrogen/(10**3)
	residential_CAPEX_cooking = residential_CAPEX_cooking_electric+residential_CAPEX_cooking_biomass+residential_CAPEX_cooking_natural_gas+residential_CAPEX_cooking_kerosene+residential_CAPEX_cooking_pliqgas+residential_CAPEX_cooking_solar+residential_CAPEX_cooking_hydrogen

	residential_CAPEX_acs_electric = residential_delta_capacity_acs_electric * residential_investment_cost_acs_electric / (10 ** 3)
	residential_CAPEX_acs_biomass = residential_delta_capacity_acs_biomass * residential_investment_cost_acs_biomass / (10 ** 3)
	residential_CAPEX_acs_natural_gas = residential_delta_capacity_acs_natural_gas * residential_investment_cost_acs_natural_gas / (10 ** 3)
	residential_CAPEX_acs_kerosene = residential_delta_capacity_acs_kerosene * residential_investment_cost_acs_kerosene / (10 ** 3)
	residential_CAPEX_acs_pliqgas = residential_delta_capacity_acs_pliqgas * residential_investment_cost_acs_pliqgas / (10 ** 3)
	residential_CAPEX_acs_solar = residential_delta_capacity_acs_solar * residential_investment_cost_acs_solar / (10 ** 3)
	residential_CAPEX_acs_hydrogen = residential_delta_capacity_acs_hydrogen * residential_investment_cost_acs_hydrogen / (10 ** 3)
	residential_CAPEX_acs = residential_CAPEX_acs_electric + residential_CAPEX_acs_biomass + residential_CAPEX_acs_natural_gas + residential_CAPEX_acs_kerosene + residential_CAPEX_acs_pliqgas + residential_CAPEX_acs_solar + residential_CAPEX_acs_hydrogen

	residential_CAPEX_electric_appliance_electric = residential_delta_capacity_electric_appliance_electric*residential_investment_cost_electric_appliance/(10**3)

	#CAPEX retrofit
	residential_CAPEX_retrofit=(residential_retrofit_house_additional*residential_investment_cost_retrofit_house + residential_retrofit_apartment_additional*residential_investment_cost_retrofit_apartment) / (10 ** 6)


	#total CAPEX
	residential_CAPEX = residential_CAPEX_heating+residential_CAPEX_cooking+residential_CAPEX_acs+residential_CAPEX_electric_appliance_electric+residential_CAPEX_retrofit

	##################################################################################################################
	dict_emission = {"residential": residential_emission}
	dict_electric_demand = {"residential": residential_dem_electric*fact2}
	# CAPEX, OPEX
	dict_CAPEX = {"residential": residential_CAPEX}
	dict_OPEX = {"residential": residential_OPEX}

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
	

	# add OPEX to master output
	for k in dict_OPEX.keys():
		# new key conveys emissions
		k_new = str(k).replace("residential", dict_sector_abv["residential"]) + "-OPEX-MMUSD"
		# add to output
		dict_out.update({k_new: dict_OPEX[k].copy()})


	# add CAPEX to master output
	for k in dict_CAPEX.keys():
		# new key conveys emissions
		k_new = str(k).replace("residential", dict_sector_abv["residential"]) + "-CAPEX-MMUSD"
		# add to output
		dict_out.update({k_new: dict_CAPEX[k].copy()})

	#return
	return dict_out#dict_emission,dict_electric_demand
