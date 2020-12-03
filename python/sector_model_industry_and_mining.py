# Industry and Mining energy model developed by Centro de Energia U. de Chile using RAND python framework
# version 0.9 september 2020

import os, os.path
import time
import pandas as pd
import numpy as np
from econometric_models import model_other_industries as dem_other_industries

#############################
#    INDUSTRY AND MINING    #
############################

def sm_industry_and_mining(df_in, dict_sector_abv):

	# conversion factor Tcal to TJ
	fact = 4.184
	# conversion factor Tcal to GWh
	fact2 = 1.162952

	# Common parameters
	share_electric_grid_to_hydrogen = np.array(df_in["share_electric_grid_to_hydrogen"])
	electrolyzer_efficiency = np.array(df_in["electrolyzer_efficiency"])

	# SUB SECTOR: COPPER MINING MODEL - Mineria del cobre

	# Read input parameters defined in parameter_ranges.csv

	copper_production = np.array(df_in["copper_production"])
	copper_intensity_useful_energy = np.array(df_in["copper_intensity_useful_energy"])
	copper_share_open_pit_mine = np.array(df_in["copper_share_open_pit_mine"])
	copper_share_subt_mine = np.array(df_in["copper_share_subt_mine"])
	copper_share_motor = np.array(df_in["copper_share_motor"])
	copper_share_other = np.array(df_in["copper_share_other"])
	copper_share_heat = np.array(df_in["copper_share_heat"])
	copper_open_pit_mine_diesel = np.array(df_in["copper_open_pit_mine_diesel"])
	copper_open_pit_mine_electricitiy = np.array(df_in["copper_open_pit_mine_electricitiy"])
	copper_open_pit_mine_hydrogen = np.array(df_in["copper_open_pit_mine_hydrogen"])
	copper_subt_mine_diesel = np.array(df_in["copper_subt_mine_diesel"])
	copper_subt_mine_electricitiy = np.array(df_in["copper_subt_mine_electricitiy"])
	copper_subt_mine_hydrogen = np.array(df_in["copper_subt_mine_hydrogen"])
	copper_motor_diesel = np.array(df_in["copper_motor_diesel"])
	copper_motor_electricitiy = np.array(df_in["copper_motor_electricitiy"])
	copper_motor_hydrogen = np.array(df_in["copper_motor_hydrogen"])
	copper_other_electricity = np.array(df_in["copper_other_electricity"])
	copper_other_natural_gas = np.array(df_in["copper_other_natural_gas"])
	copper_other_diesel = np.array(df_in["copper_other_diesel"])
	copper_heat_diesel = np.array(df_in["copper_heat_diesel"])
	copper_heat_electricitiy = np.array(df_in["copper_heat_electricitiy"])
	copper_heat_hydrogen = np.array(df_in["copper_heat_hydrogen"])
	copper_heat_natural_gas = np.array(df_in["copper_heat_natural_gas"])
	copper_heat_plqgas = np.array(df_in["copper_heat_plqgas"])
	copper_heat_solar = np.array(df_in["copper_heat_solar"])
	copper_efficiency_open_pit_mine_diesel = np.array(df_in["copper_efficiency_open_pit_mine_diesel"])
	copper_efficiency_open_pit_mine_electricitiy = np.array(df_in["copper_efficiency_open_pit_mine_electricitiy"])
	copper_efficiency_open_pit_mine_hydrogen = np.array(df_in["copper_efficiency_open_pit_mine_hydrogen"])
	copper_efficiency_subt_mine_diesel = np.array(df_in["copper_efficiency_subt_mine_diesel"])
	copper_efficiency_subt_mine_electricitiy = np.array(df_in["copper_efficiency_subt_mine_electricitiy"])
	copper_efficiency_subt_mine_hydrogen = np.array(df_in["copper_efficiency_subt_mine_hydrogen"])
	copper_efficiency_motor_diesel = np.array(df_in["copper_efficiency_motor_diesel"])
	copper_efficiency_motor_electricitiy = np.array(df_in["copper_efficiency_motor_electricitiy"])
	copper_efficiency_motor_hydrogen = np.array(df_in["copper_efficiency_motor_hydrogen"])
	copper_efficiency_other_electricity = np.array(df_in["copper_efficiency_other_electricity"])
	copper_efficiency_other_natural_gas = np.array(df_in["copper_efficiency_other_natural_gas"])
	copper_efficiency_other_diesel = np.array(df_in["copper_efficiency_other_diesel"])
	copper_efficiency_heat_diesel = np.array(df_in["copper_efficiency_heat_diesel"])
	copper_efficiency_heat_electricitiy = np.array(df_in["copper_efficiency_heat_electricitiy"])
	copper_efficiency_heat_hydrogen = np.array(df_in["copper_efficiency_heat_hydrogen"])
	copper_efficiency_heat_natural_gas = np.array(df_in["copper_efficiency_heat_natural_gas"])
	copper_efficiency_heat_plqgas = np.array(df_in["copper_efficiency_heat_plqgas"])
	copper_efficiency_heat_solar = np.array(df_in["copper_efficiency_heat_solar"])
	copper_emission_fact_diesel = np.array(df_in["copper_emission_fact_diesel"])
	copper_emission_fact_kerosene = np.array(df_in["copper_emission_fact_kerosene"])
	copper_emission_fact_natural_gas = np.array(df_in["copper_emission_fact_natural_gas"])
	copper_emission_fact_pliqgas = np.array(df_in["copper_emission_fact_pliqgas"])
	copper_emission_fact_fueloil = np.array(df_in["copper_emission_fact_fueloil"])

	# calculate demand by en use

	copper_dem_open_pit_mine_diesel = copper_production * copper_intensity_useful_energy * copper_share_open_pit_mine * copper_open_pit_mine_diesel / copper_efficiency_open_pit_mine_diesel
	copper_dem_open_pit_mine_electricitiy = copper_production * copper_intensity_useful_energy * copper_share_open_pit_mine * copper_open_pit_mine_electricitiy / copper_efficiency_open_pit_mine_electricitiy
	copper_dem_open_pit_mine_hydrogen = copper_production * copper_intensity_useful_energy * copper_share_open_pit_mine * copper_open_pit_mine_hydrogen / copper_efficiency_open_pit_mine_hydrogen

	copper_dem_subt_mine_diesel = copper_production * copper_intensity_useful_energy * copper_share_subt_mine * copper_subt_mine_diesel / copper_efficiency_subt_mine_diesel
	copper_dem_subt_mine_electricitiy = copper_production * copper_intensity_useful_energy * copper_share_subt_mine * copper_subt_mine_electricitiy / copper_efficiency_subt_mine_electricitiy
	copper_dem_subt_mine_hydrogen = copper_production * copper_intensity_useful_energy * copper_share_subt_mine * copper_subt_mine_hydrogen / copper_efficiency_subt_mine_hydrogen

	copper_dem_motor_diesel = copper_production * copper_intensity_useful_energy * copper_share_motor * copper_motor_diesel / copper_efficiency_motor_diesel
	copper_dem_motor_electricitiy = copper_production * copper_intensity_useful_energy * copper_share_motor * copper_motor_electricitiy / copper_efficiency_motor_electricitiy
	copper_dem_motor_hydrogen = copper_production * copper_intensity_useful_energy * copper_share_motor * copper_motor_hydrogen / copper_efficiency_motor_hydrogen

	copper_dem_other_electricity = copper_production * copper_intensity_useful_energy * copper_share_other * copper_other_electricity / copper_efficiency_other_electricity
	copper_dem_other_natural_gas = copper_production * copper_intensity_useful_energy * copper_share_other * copper_other_natural_gas / copper_efficiency_other_natural_gas
	copper_dem_other_diesel = copper_production * copper_intensity_useful_energy * copper_share_other * copper_other_diesel / copper_efficiency_other_diesel

	copper_dem_heat_diesel = copper_production * copper_intensity_useful_energy * copper_share_heat * copper_heat_diesel / copper_efficiency_heat_diesel
	copper_dem_heat_electricitiy = copper_production * copper_intensity_useful_energy * copper_share_heat * copper_heat_electricitiy / copper_efficiency_heat_electricitiy
	copper_dem_heat_hydrogen = copper_production * copper_intensity_useful_energy * copper_share_heat * copper_heat_hydrogen / copper_efficiency_heat_hydrogen
	copper_dem_heat_natural_gas = copper_production * copper_intensity_useful_energy * copper_share_heat * copper_heat_natural_gas / copper_efficiency_heat_natural_gas
	copper_dem_heat_plqgas = copper_production * copper_intensity_useful_energy * copper_share_heat * copper_heat_plqgas / copper_efficiency_heat_plqgas
	copper_dem_heat_solar = copper_production * copper_intensity_useful_energy * copper_share_heat * copper_heat_solar / copper_efficiency_heat_solar

	# calculate demand in Tcal
	copper_dem_diesel = copper_dem_open_pit_mine_diesel + copper_dem_subt_mine_diesel + copper_dem_motor_diesel + copper_dem_other_diesel + copper_dem_heat_diesel
	copper_dem_kerosene = 0
	copper_dem_natural_gas = copper_dem_other_natural_gas + copper_dem_heat_natural_gas
	copper_dem_electric = copper_dem_open_pit_mine_electricitiy + copper_dem_subt_mine_electricitiy + copper_dem_motor_electricitiy + copper_dem_other_electricity + copper_dem_heat_electricitiy
	copper_dem_hydrogen = copper_dem_open_pit_mine_hydrogen + copper_dem_subt_mine_hydrogen + copper_dem_heat_hydrogen + copper_dem_motor_hydrogen
	copper_dem_pliqgas = copper_dem_heat_plqgas
	copper_dem_fueloil = 0

	# calculate emission in millon tCO2
	copper_emission_diesel = copper_dem_diesel * fact * copper_emission_fact_diesel / (10 ** 9)
	copper_emission_kerosene = copper_dem_kerosene * fact * copper_emission_fact_kerosene / (10 ** 9)
	copper_emission_natural_gas = copper_dem_natural_gas * fact * copper_emission_fact_natural_gas / (10 ** 9)
	copper_emission_pliqgas = copper_dem_pliqgas * fact * copper_emission_fact_pliqgas / (10 ** 9)
	copper_emission_fueloil = copper_dem_fueloil * fact * copper_emission_fact_fueloil / (10 ** 9)

	copper_emission = copper_emission_diesel + copper_emission_kerosene + copper_emission_natural_gas + copper_emission_pliqgas + copper_emission_fueloil

	# electric demand to produce hydrogen
	electric_demand_hydrogen = copper_dem_hydrogen / electrolyzer_efficiency * share_electric_grid_to_hydrogen

	dict_emission = {"copper": copper_emission}
	dict_electric_demand = {"copper": copper_dem_electric * fact2}

	# SUB SECTOR: PULP ENERGY MODEL - Papel y Celulosa

	# Read input parameters defined in parameter_ranges.csv
	pulp_production = np.array(df_in["pulp_production"])
	pulp_intensity = np.array(df_in["pulp_intensity"])
	pulp_frac_diesel = np.array(df_in["pulp_frac_diesel"])
	pulp_frac_natural_gas = np.array(df_in["pulp_frac_natural_gas"])
	pulp_frac_electric = np.array(df_in["pulp_frac_electric"])
	pulp_frac_biomass = np.array(df_in["pulp_frac_biomass"])
	pulp_frac_hydrogen = np.array(df_in["pulp_frac_hydrogen"])
	pulp_frac_thermal_solar = np.array(df_in["pulp_frac_thermal_solar"])
	pulp_frac_solar = np.array(df_in["pulp_frac_solar"])
	pulp_emission_fact_diesel = np.array(df_in["pulp_emission_fact_diesel"])
	pulp_emission_fact_natural_gas = np.array(df_in["pulp_emission_fact_natural_gas"])

	# calculate demand in Tcal
	pulp_dem_diesel = pulp_production * pulp_intensity * pulp_frac_diesel
	pulp_dem_natural_gas = pulp_production * pulp_intensity * pulp_frac_natural_gas
	pulp_dem_electric = pulp_production * pulp_intensity * pulp_frac_electric
	pulp_dem_biomass = pulp_production * pulp_intensity * pulp_frac_biomass
	pulp_dem_hydrogen = pulp_production * pulp_intensity * pulp_frac_hydrogen

	# calculate emission in millon tCO2
	pulp_emission_diesel = pulp_dem_diesel * fact * pulp_emission_fact_diesel / (10 ** 9)
	pulp_emission_natural_gas = pulp_dem_natural_gas * fact * pulp_emission_fact_natural_gas / (10 ** 9)
	pulp_emission = pulp_emission_diesel + pulp_emission_natural_gas

	# electric demand to produce hydrogen
	electric_demand_hydrogen = electric_demand_hydrogen + pulp_dem_hydrogen / electrolyzer_efficiency * share_electric_grid_to_hydrogen

	# update
	dict_emission.update({"pulp": pulp_emission})
	dict_electric_demand.update({"pulp": pulp_dem_electric * fact2})

	# SUB SECTOR: Other industries - Industrias

	# Read input parameters defined in parameter_ranges.csv
	gdp = np.array(df_in["pib"]) * np.array(df_in["pib_scalar_transport"])
	growth_rate_gdp = np.array(df_in["gr_pib"])
	
	other_industries_intensity = np.array(df_in["other_industries_intensity"])

	#
	#gdp = np.array(df_in["gdp"])
	#growth_rate_gdp = np.array(df_in["growth_rate_gdp"])
	other_industries_elasticity = np.array(df_in["other_industries_elasticity"])
	other_industries_rate_useful_energy = np.array(df_in["other_industries_rate_useful_energy"])
	other_industries_share_motor = np.array(df_in["other_industries_share_motor"])
	other_industries_share_other = np.array(df_in["other_industries_share_other"])
	other_industries_share_heat = np.array(df_in["other_industries_share_heat"])
	other_industries_motor_diesel = np.array(df_in["other_industries_motor_diesel"])
	other_industries_motor_pliqgas = np.array(df_in["other_industries_motor_pliqgas"])
	other_industries_motor_electric = np.array(df_in["other_industries_motor_electric"])
	other_industries_motor_hydrogen = np.array(df_in["other_industries_motor_hydrogen"])
	other_industries_other_electric = np.array(df_in["other_industries_other_electric"])
	other_industries_heat_coal = np.array(df_in["other_industries_heat_coal"])
	other_industries_heat_electric = np.array(df_in["other_industries_heat_electric"])
	other_industries_heat_solar = np.array(df_in["other_industries_heat_solar"])
	other_industries_heat_pliqgas = np.array(df_in["other_industries_heat_pliqgas"])
	other_industries_heat_natural_gas = np.array(df_in["other_industries_heat_natural_gas"])
	other_industries_heat_biomass = np.array(df_in["other_industries_heat_biomass"])
	other_industries_heat_diesel = np.array(df_in["other_industries_heat_diesel"])
	other_industries_heat_fuel_oil = np.array(df_in["other_industries_heat_fuel_oil"])
	other_industries_heat_hydrogen = np.array(df_in["other_industries_heat_hydrogen"])
	other_industries_efficiency_motor_diesel = np.array(df_in["other_industries_efficiency_motor_diesel"])
	other_industries_efficiency_motor_pliqgas = np.array(df_in["other_industries_efficiency_motor_pliqgas"])
	other_industries_efficiency_motor_electric = np.array(df_in["other_industries_efficiency_motor_electric"])
	other_industries_efficiency_motor_hydrogen = np.array(df_in["other_industries_efficiency_motor_hydrogen"])
	other_industries_efficiency_other_electric = np.array(df_in["other_industries_efficiency_other_electric"])
	other_industries_efficiency_heat_coal = np.array(df_in["other_industries_efficiency_heat_coal"])
	other_industries_efficiency_heat_electric = np.array(df_in["other_industries_efficiency_heat_electric"])
	other_industries_efficiency_heat_solar = np.array(df_in["other_industries_efficiency_heat_solar"])
	other_industries_efficiency_heat_pliqgas = np.array(df_in["other_industries_efficiency_heat_pliqgas"])
	other_industries_efficiency_heat_natural_gas = np.array(df_in["other_industries_efficiency_heat_natural_gas"])
	other_industries_efficiency_heat_biomass = np.array(df_in["other_industries_efficiency_heat_biomass"])
	other_industries_efficiency_heat_diesel = np.array(df_in["other_industries_efficiency_heat_diesel"])
	other_industries_efficiency_heat_fuel_oil = np.array(df_in["other_industries_efficiency_heat_fuel_oil"])
	other_industries_efficiency_heat_hydrogen = np.array(df_in["other_industries_efficiency_heat_hydrogen"])
	other_industries_emission_fact_diesel = np.array(df_in["other_industries_emission_fact_diesel"])
	other_industries_emission_fact_natural_gas = np.array(df_in["other_industries_emission_fact_natural_gas"])
	other_industries_emission_fact_coal = np.array(df_in["other_industries_emission_fact_coal"])
	other_industries_emission_fact_pliqgas = np.array(df_in["other_industries_emission_fact_pliqgas"])
	other_industries_emission_fact_fueloil = np.array(df_in["other_industries_emission_fact_fueloil"])

	#
	year = np.array(df_in["year"])  # vector years

	other_industries_total_demand = dem_other_industries(year, growth_rate_gdp, other_industries_elasticity)
	other_industries_useful_energy = other_industries_total_demand * other_industries_rate_useful_energy

	# calculate demand in Tcal by en use
	other_industries_dem_motor_diesel = other_industries_useful_energy * other_industries_share_motor * other_industries_motor_diesel / other_industries_efficiency_motor_diesel
	other_industries_dem_motor_pliqgas = other_industries_useful_energy * other_industries_share_motor * other_industries_motor_pliqgas / other_industries_efficiency_motor_pliqgas
	other_industries_dem_motor_electric = other_industries_useful_energy * other_industries_share_motor * other_industries_motor_electric / other_industries_efficiency_motor_electric
	other_industries_dem_motor_hydrogen = other_industries_useful_energy * other_industries_share_motor * other_industries_motor_hydrogen / other_industries_efficiency_motor_hydrogen

	other_industries_dem_other_electric = other_industries_useful_energy * other_industries_share_other * other_industries_other_electric / other_industries_efficiency_other_electric

	other_industries_dem_heat_coal = other_industries_useful_energy * other_industries_share_heat * other_industries_heat_coal / other_industries_efficiency_heat_coal
	other_industries_dem_heat_electric = other_industries_useful_energy * other_industries_share_heat * other_industries_heat_electric / other_industries_efficiency_heat_electric
	other_industries_dem_heat_solar = other_industries_useful_energy * other_industries_share_heat * other_industries_heat_solar / other_industries_efficiency_heat_solar
	other_industries_dem_heat_pliqgas = other_industries_useful_energy * other_industries_share_heat * other_industries_heat_pliqgas / other_industries_efficiency_heat_pliqgas
	other_industries_dem_heat_natural_gas = other_industries_useful_energy * other_industries_share_heat * other_industries_heat_natural_gas / other_industries_efficiency_heat_natural_gas
	other_industries_dem_heat_biomass = other_industries_useful_energy * other_industries_share_heat * other_industries_heat_biomass / other_industries_efficiency_heat_biomass
	other_industries_dem_heat_diesel = other_industries_useful_energy * other_industries_share_heat * other_industries_heat_diesel / other_industries_efficiency_heat_diesel
	other_industries_dem_heat_fuel_oil = other_industries_useful_energy * other_industries_share_heat * other_industries_heat_fuel_oil / other_industries_efficiency_heat_fuel_oil
	other_industries_dem_heat_hydrogen = other_industries_useful_energy * other_industries_share_heat * other_industries_heat_hydrogen / other_industries_efficiency_heat_hydrogen

	# total demand by type of energy

	other_industries_dem_diesel = other_industries_dem_motor_diesel + other_industries_dem_heat_diesel
	other_industries_dem_natural_gas = other_industries_dem_heat_natural_gas
	other_industries_dem_electric = other_industries_dem_motor_electric + other_industries_dem_other_electric + other_industries_dem_heat_electric
	other_industries_dem_coal = other_industries_dem_heat_coal
	other_industries_dem_biomass = other_industries_dem_heat_biomass
	other_industries_dem_solar = other_industries_dem_heat_solar
	other_industries_dem_hydrogen = other_industries_dem_motor_hydrogen + other_industries_dem_heat_hydrogen
	other_industries_dem_pliqgas = other_industries_dem_motor_pliqgas + other_industries_dem_heat_pliqgas
	other_industries_dem_fueloil = other_industries_dem_heat_fuel_oil

	# calculate emission in millon tCO2

	other_industries_emission_diesel = other_industries_dem_diesel * other_industries_emission_fact_diesel * fact / (
				10 ** 9)
	other_industries_emission_natural_gas = other_industries_dem_natural_gas * other_industries_emission_fact_natural_gas * fact / (
				10 ** 9)
	other_industries_emission_coal = other_industries_dem_coal * other_industries_emission_fact_coal * fact / (10 ** 9)
	other_industries_emission_pliqgas = other_industries_dem_pliqgas * other_industries_emission_fact_pliqgas * fact / (
				10 ** 9)
	other_industries_emission_fueloil = other_industries_dem_fueloil * other_industries_emission_fact_fueloil * fact / (
				10 ** 9)
	other_industries_emission = other_industries_emission_diesel + other_industries_emission_natural_gas + other_industries_emission_coal + other_industries_emission_pliqgas + other_industries_emission_fueloil

	# electric demand to produce hydrogen
	electric_demand_hydrogen = electric_demand_hydrogen + other_industries_dem_hydrogen / electrolyzer_efficiency * share_electric_grid_to_hydrogen

	# update
	dict_emission.update({"other_industries": other_industries_emission})
	dict_electric_demand.update({"other_industries": other_industries_dem_electric * fact2})

	# SUB SECTOR: CEMENT Industry- Industria del cemento

	cement_production = np.array(df_in["cement_production"])
	cement_intensity = np.array(df_in["cement_intensity"])
	cement_frac_diesel = np.array(df_in["cement_frac_diesel"])
	cement_frac_natural_gas = np.array(df_in["cement_frac_natural_gas"])
	cement_frac_electric = np.array(df_in["cement_frac_electric"])
	cement_frac_biomass = np.array(df_in["cement_frac_biomass"])
	cement_frac_hydrogen = np.array(df_in["cement_frac_hydrogen"])
	cement_frac_coal = np.array(df_in["cement_frac_coal"])
	cement_frac_kerosene = np.array(df_in["cement_frac_kerosene"])
	cement_frac_thermal_solar = np.array(df_in["cement_frac_thermal_solar"])
	cement_frac_solar = np.array(df_in["cement_frac_solar"])
	cement_emission_fact_diesel = np.array(df_in["cement_emission_fact_diesel"])
	cement_emission_fact_natural_gas = np.array(df_in["cement_emission_fact_natural_gas"])
	cement_emission_fact_coal = np.array(df_in["cement_emission_fact_coal"])
	cement_emission_fact_kerosene = np.array(df_in["cement_emission_fact_kerosene"])

	# calculate demand in Tcal
	cement_dem_diesel = cement_production * cement_intensity * cement_frac_diesel
	cement_dem_natural_gas = cement_production * cement_intensity * cement_frac_natural_gas
	cement_dem_electric = cement_production * cement_intensity * cement_frac_electric
	cement_dem_biomass = cement_production * cement_intensity * cement_frac_biomass
	cement_dem_hydrogen = cement_production * cement_intensity * cement_frac_hydrogen
	cement_dem_coal = cement_production * cement_intensity * cement_frac_coal
	cement_dem_kerosene = cement_production * cement_intensity * cement_frac_kerosene

	# calculate emission in millon tCO2
	cement_emission_diesel = cement_dem_diesel * fact * cement_emission_fact_diesel / (10 ** 9)
	cement_emission_natural_gas = cement_dem_natural_gas * fact * cement_emission_fact_natural_gas / (10 ** 9)
	cement_emission_coal = cement_dem_coal * fact * cement_emission_fact_coal / (10 ** 9)
	cement_emission_kerosene = cement_dem_kerosene * fact * cement_emission_fact_kerosene / (10 ** 9)
	cement_emission = cement_emission_diesel + cement_emission_natural_gas + cement_emission_coal + cement_emission_kerosene

	# electric demand to produce hydrogen
	electric_demand_hydrogen = electric_demand_hydrogen + cement_dem_hydrogen / electrolyzer_efficiency * share_electric_grid_to_hydrogen

	# update
	dict_emission.update({"cement": cement_emission})
	dict_electric_demand.update({"cement": cement_dem_electric * fact2})

	# SUB SECTOR: IRON Industry- Minieria del hierro
	iron_production = np.array(df_in["iron_production"])
	iron_intensity = np.array(df_in["iron_intensity"])
	iron_frac_diesel = np.array(df_in["iron_frac_diesel"])
	iron_frac_natural_gas = np.array(df_in["iron_frac_natural_gas"])
	iron_frac_electric = np.array(df_in["iron_frac_electric"])
	iron_frac_biomass = np.array(df_in["iron_frac_biomass"])
	iron_frac_hydrogen = np.array(df_in["iron_frac_hydrogen"])
	iron_frac_coal = np.array(df_in["iron_frac_coal"])
	iron_frac_thermal_solar = np.array(df_in["iron_frac_thermal_solar"])
	iron_frac_solar = np.array(df_in["iron_frac_solar"])
	iron_emission_fact_diesel = np.array(df_in["iron_emission_fact_diesel"])
	iron_emission_fact_natural_gas = np.array(df_in["iron_emission_fact_natural_gas"])
	iron_emission_fact_coal = np.array(df_in["iron_emission_fact_coal"])

	# calculate demand in Tcal
	iron_dem_diesel = iron_production * iron_intensity * iron_frac_diesel
	iron_dem_natural_gas = iron_production * iron_intensity * iron_frac_natural_gas
	iron_dem_electric = iron_production * iron_intensity * iron_frac_electric
	iron_dem_biomass = iron_production * iron_intensity * iron_frac_biomass
	iron_dem_hydrogen = iron_production * iron_intensity * iron_frac_hydrogen
	iron_dem_coal = iron_production * iron_intensity * iron_frac_coal

	# calculate emission in millon tCO2
	iron_emission_diesel = iron_dem_diesel * fact * iron_emission_fact_diesel / (10 ** 9)
	iron_emission_natural_gas = iron_dem_natural_gas * fact * iron_emission_fact_natural_gas / (10 ** 9)
	iron_emission_coal = iron_dem_coal * fact * iron_emission_fact_coal / (10 ** 9)
	iron_emission = iron_emission_diesel + iron_emission_natural_gas + iron_emission_coal

	# electric demand to produce hydrogen
	electric_demand_hydrogen = electric_demand_hydrogen + iron_dem_hydrogen / electrolyzer_efficiency * share_electric_grid_to_hydrogen

	# update
	dict_emission.update({"iron": iron_emission})
	dict_electric_demand.update({"iron": iron_dem_electric * fact2})

	# SUB SECTOR: Steel Industry- Industria del acero
	steel_production = np.array(df_in["steel_production"])
	steel_intensity = np.array(df_in["steel_intensity"])
	steel_frac_diesel = np.array(df_in["steel_frac_diesel"])
	steel_frac_natural_gas = np.array(df_in["steel_frac_natural_gas"])
	steel_frac_electric = np.array(df_in["steel_frac_electric"])
	steel_frac_biomass = np.array(df_in["steel_frac_biomass"])
	steel_frac_hydrogen = np.array(df_in["steel_frac_hydrogen"])
	steel_frac_coal = np.array(df_in["steel_frac_coal"])
	steel_frac_kerosene = np.array(df_in["steel_frac_kerosene"])
	steel_frac_thermal_solar = np.array(df_in["iron_frac_thermal_solar"])
	steel_frac_solar = np.array(df_in["iron_frac_solar"])
	steel_emission_fact_diesel = np.array(df_in["steel_emission_fact_diesel"])
	steel_emission_fact_natural_gas = np.array(df_in["steel_emission_fact_natural_gas"])
	steel_emission_fact_coal = np.array(df_in["steel_emission_fact_coal"])
	steel_emission_fact_kerosene = np.array(df_in["steel_emission_fact_kerosene"])

	# calculate demand in Tcal
	steel_dem_diesel = steel_production * steel_intensity * steel_frac_diesel
	steel_dem_natural_gas = steel_production * steel_intensity * steel_frac_natural_gas
	steel_dem_electric = steel_production * steel_intensity * steel_frac_electric
	steel_dem_biomass = steel_production * steel_intensity * steel_frac_biomass
	steel_dem_hydrogen = steel_production * steel_intensity * steel_frac_hydrogen
	steel_dem_coal = steel_production * steel_intensity * steel_frac_coal
	steel_dem_kerosene = steel_production * steel_intensity * steel_frac_kerosene

	# calculate emission in millon tCO2
	steel_emission_diesel = steel_dem_diesel * fact * steel_emission_fact_diesel / (10 ** 9)
	steel_emission_natural_gas = steel_dem_natural_gas * fact * steel_emission_fact_natural_gas / (10 ** 9)
	steel_emission_coal = steel_dem_coal * fact * steel_emission_fact_coal / (10 ** 9)
	steel_emission_kerosene = steel_dem_kerosene * fact * steel_emission_fact_kerosene / (10 ** 9)
	steel_emission = steel_emission_diesel + steel_emission_natural_gas + steel_emission_coal + steel_emission_kerosene

	# electric demand to produce hydrogen
	electric_demand_hydrogen = electric_demand_hydrogen + steel_dem_hydrogen / electrolyzer_efficiency * share_electric_grid_to_hydrogen

	# update
	dict_emission.update({"steel": steel_emission})
	dict_electric_demand.update({"steel": steel_dem_electric * fact2})

	# SUB SECTOR: Sugar - Azucar

	sugar_production = np.array(df_in["sugar_production"])
	sugar_intensity = np.array(df_in["sugar_intensity"])
	sugar_frac_diesel = np.array(df_in["sugar_frac_diesel"])
	sugar_frac_natural_gas = np.array(df_in["sugar_frac_natural_gas"])
	sugar_frac_electric = np.array(df_in["sugar_frac_electric"])
	sugar_frac_biomass = np.array(df_in["sugar_frac_biomass"])
	sugar_frac_hydrogen = np.array(df_in["sugar_frac_hydrogen"])
	sugar_frac_coal = np.array(df_in["sugar_frac_coal"])
	sugar_frac_thermal_solar = np.array(df_in["sugar_frac_thermal_solar"])
	sugar_frac_solar = np.array(df_in["sugar_frac_solar"])

	sugar_emission_fact_diesel = np.array(df_in["sugar_emission_fact_diesel"])
	sugar_emission_fact_natural_gas = np.array(df_in["sugar_emission_fact_natural_gas"])
	sugar_emission_fact_coal = np.array(df_in["sugar_emission_fact_coal"])

	# calculate demand in Tcal
	sugar_dem_diesel = sugar_production * sugar_intensity * sugar_frac_diesel
	sugar_dem_natural_gas = sugar_production * sugar_intensity * sugar_frac_natural_gas
	sugar_dem_electric = sugar_production * sugar_intensity * sugar_frac_electric
	sugar_dem_biomass = sugar_production * sugar_intensity * sugar_frac_biomass
	sugar_dem_hydrogen = sugar_production * sugar_intensity * sugar_frac_hydrogen
	sugar_dem_coal = sugar_production * sugar_intensity * sugar_frac_coal

	# calculate emission in millon tCO2
	sugar_emission_diesel = sugar_dem_diesel * fact * sugar_emission_fact_diesel / (10 ** 9)
	sugar_emission_natural_gas = sugar_dem_natural_gas * fact * sugar_emission_fact_natural_gas / (10 ** 9)
	sugar_emission_coal = sugar_dem_coal * fact * sugar_emission_fact_coal / (10 ** 9)
	sugar_emission = sugar_emission_diesel + sugar_emission_natural_gas + sugar_emission_coal

	# electric demand to produce hydrogen
	electric_demand_hydrogen = electric_demand_hydrogen + sugar_dem_hydrogen / electrolyzer_efficiency * share_electric_grid_to_hydrogen

	# update
	dict_emission.update({"sugar": sugar_emission})
	dict_electric_demand.update({"sugar": sugar_dem_electric * fact2})

	# SUB SECTOR: Saltpeter - Salitre

	saltpeter_production = np.array(df_in["saltpeter_production"])
	saltpeter_intensity = np.array(df_in["saltpeter_intensity"])
	saltpeter_frac_diesel = np.array(df_in["saltpeter_frac_diesel"])
	saltpeter_frac_natural_gas = np.array(df_in["saltpeter_frac_natural_gas"])
	saltpeter_frac_electric = np.array(df_in["saltpeter_frac_electric"])
	saltpeter_frac_biomass = np.array(df_in["saltpeter_frac_biomass"])
	saltpeter_frac_hydrogen = np.array(df_in["saltpeter_frac_hydrogen"])
	saltpeter_frac_coal = np.array(df_in["saltpeter_frac_coal"])
	saltpeter_frac_thermal_solar = np.array(df_in["saltpeter_frac_thermal_solar"])
	saltpeter_frac_solar = np.array(df_in["saltpeter_frac_solar"])

	saltpeter_emission_fact_diesel = np.array(df_in["saltpeter_emission_fact_diesel"])
	saltpeter_emission_fact_natural_gas = np.array(df_in["saltpeter_emission_fact_natural_gas"])
	saltpeter_emission_fact_coal = np.array(df_in["saltpeter_emission_fact_coal"])

	# calculate demand in Tcal
	saltpeter_dem_diesel = saltpeter_production * saltpeter_intensity * saltpeter_frac_diesel
	saltpeter_dem_natural_gas = saltpeter_production * saltpeter_intensity * saltpeter_frac_natural_gas
	saltpeter_dem_electric = saltpeter_production * saltpeter_intensity * saltpeter_frac_electric
	saltpeter_dem_biomass = saltpeter_production * saltpeter_intensity * saltpeter_frac_biomass
	saltpeter_dem_hydrogen = saltpeter_production * saltpeter_intensity * saltpeter_frac_hydrogen
	saltpeter_dem_coal = saltpeter_production * saltpeter_intensity * saltpeter_frac_coal

	# calculate emission in millon tCO2
	saltpeter_emission_diesel = saltpeter_dem_diesel * fact * saltpeter_emission_fact_diesel / (10 ** 9)
	saltpeter_emission_natural_gas = saltpeter_dem_natural_gas * fact * saltpeter_emission_fact_natural_gas / (10 ** 9)
	saltpeter_emission_coal = saltpeter_dem_coal * fact * saltpeter_emission_fact_coal / (10 ** 9)
	saltpeter_emission = saltpeter_emission_diesel + saltpeter_emission_natural_gas + saltpeter_emission_coal

	# electric demand to produce hydrogen
	electric_demand_hydrogen = electric_demand_hydrogen + saltpeter_dem_hydrogen / electrolyzer_efficiency * share_electric_grid_to_hydrogen

	# update
	dict_emission.update({"saltpeter": saltpeter_emission})
	dict_electric_demand.update({"saltpeter": saltpeter_dem_electric * fact2})

	# SUB SECTOR: Other mining industries - Minas varias

	other_mining_production = np.array(df_in["other_mining_production"])
	other_mining_intensity = np.array(df_in["other_mining_intensity"])
	other_mining_frac_diesel = np.array(df_in["other_mining_frac_diesel"])
	other_mining_frac_natural_gas = np.array(df_in["other_mining_frac_natural_gas"])
	other_mining_frac_electric = np.array(df_in["other_mining_frac_electric"])
	other_mining_frac_biomass = np.array(df_in["other_mining_frac_biomass"])
	other_mining_frac_hydrogen = np.array(df_in["other_mining_frac_hydrogen"])
	other_mining_frac_coal = np.array(df_in["other_mining_frac_coal"])
	other_mining_frac_thermal_solar = np.array(df_in["other_mining_frac_thermal_solar"])
	other_mining_frac_solar = np.array(df_in["other_mining_frac_solar"])

	other_mining_emission_fact_diesel = np.array(df_in["other_mining_emission_fact_diesel"])
	other_mining_emission_fact_natural_gas = np.array(df_in["other_mining_emission_fact_natural_gas"])
	other_mining_emission_fact_coal = np.array(df_in["other_mining_emission_fact_coal"])

	# calculate demand in Tcal
	other_mining_dem_diesel = other_mining_production * other_mining_intensity * other_mining_frac_diesel
	other_mining_dem_natural_gas = other_mining_production * other_mining_intensity * other_mining_frac_natural_gas
	other_mining_dem_electric = other_mining_production * other_mining_intensity * other_mining_frac_electric
	other_mining_dem_biomass = other_mining_production * other_mining_intensity * other_mining_frac_biomass
	other_mining_dem_hydrogen = other_mining_production * other_mining_intensity * other_mining_frac_hydrogen
	other_mining_dem_coal = other_mining_production * other_mining_intensity * other_mining_frac_coal

	# calculate emission in millon tCO2
	other_mining_emission_diesel = other_mining_dem_diesel * fact * other_mining_emission_fact_diesel / (10 ** 9)
	other_mining_emission_natural_gas = other_mining_dem_natural_gas * fact * other_mining_emission_fact_natural_gas / (
				10 ** 9)
	other_mining_emission_coal = other_mining_dem_coal * fact * other_mining_emission_fact_coal / (10 ** 9)
	other_mining_emission = other_mining_emission_diesel + other_mining_emission_natural_gas + other_mining_emission_coal

	# electric demand to produce hydrogen
	electric_demand_hydrogen = electric_demand_hydrogen + other_mining_dem_hydrogen / electrolyzer_efficiency * share_electric_grid_to_hydrogen

	# update
	dict_emission.update({"other_mining": other_mining_emission})
	dict_electric_demand.update({"other_mining": other_mining_dem_electric * fact2})

	# SUB SECTOR: Fishing - Pesca

	fishing_production = np.array(df_in["fishing_production"])
	fishing_intensity = np.array(df_in["fishing_intensity"])
	fishing_frac_diesel = np.array(df_in["fishing_frac_diesel"])
	fishing_frac_natural_gas = np.array(df_in["fishing_frac_natural_gas"])
	fishing_frac_electric = np.array(df_in["fishing_frac_electric"])
	fishing_frac_biomass = np.array(df_in["fishing_frac_biomass"])
	fishing_frac_hydrogen = np.array(df_in["fishing_frac_hydrogen"])
	fishing_frac_coal = np.array(df_in["fishing_frac_coal"])
	fishing_frac_thermal_solar = np.array(df_in["fishing_frac_thermal_solar"])
	fishing_frac_solar = np.array(df_in["fishing_frac_solar"])

	fishing_emission_fact_diesel = np.array(df_in["fishing_emission_fact_diesel"])
	fishing_emission_fact_natural_gas = np.array(df_in["fishing_emission_fact_natural_gas"])
	fishing_emission_fact_coal = np.array(df_in["fishing_emission_fact_coal"])

	# calculate demand in Tcal
	fishing_dem_diesel = fishing_production * fishing_intensity * fishing_frac_diesel
	fishing_dem_natural_gas = fishing_production * fishing_intensity * fishing_frac_natural_gas
	fishing_dem_electric = fishing_production * fishing_intensity * fishing_frac_electric
	fishing_dem_biomass = fishing_production * fishing_intensity * fishing_frac_biomass
	fishing_dem_hydrogen = fishing_production * fishing_intensity * fishing_frac_hydrogen
	fishing_dem_coal = fishing_production * fishing_intensity * fishing_frac_coal

	# calculate emission in millon tCO2
	fishing_emission_diesel = fishing_dem_diesel * fact * fishing_emission_fact_diesel / (10 ** 9)
	fishing_emission_natural_gas = fishing_dem_natural_gas * fact * fishing_emission_fact_natural_gas / (10 ** 9)
	fishing_emission_coal = fishing_dem_coal * fact * fishing_emission_fact_coal / (10 ** 9)
	fishing_emission = fishing_emission_diesel + fishing_emission_natural_gas + fishing_emission_coal

	# electric demand to produce hydrogen
	electric_demand_hydrogen = electric_demand_hydrogen + fishing_dem_hydrogen / electrolyzer_efficiency * share_electric_grid_to_hydrogen

	# update
	dict_emission.update({"fishing": fishing_emission})
	dict_electric_demand.update({"fishing": fishing_dem_electric * fact2})

	# electric demand to produce hydrogen
	electric_demand_hydrogen = electric_demand_hydrogen * fact2

	##  final output dictionary
	dict_out = {}

	vec_total_emissions = 0
	# add emissions to master output
	for k in dict_emission.keys():
		# new key conveys emissions
		k_new = (dict_sector_abv["industry_and_mining"]) + "-emissions_" + str(k) + "-mtco2e"
		# add to output
		dict_out.update({k_new: dict_emission[k].copy()})
		# update total
		vec_total_emissions = vec_total_emissions + np.array(dict_emission[k])

	vec_total_demand_electricity = 0
	# add electric demand to master output
	for k in dict_electric_demand.keys():
		# new key conveys emissions
		k_new = (dict_sector_abv["industry_and_mining"]) + "-electricity_" + str(k) + "_demand-gwh"
		# add to output
		dict_out.update({k_new: dict_electric_demand[k].copy()})
		# update total
		vec_total_demand_electricity = vec_total_demand_electricity + np.array(dict_electric_demand[k])

	# update with electricity to produce hydrogen
	vec_total_demand_electricity = vec_total_demand_electricity + electric_demand_hydrogen

	# add totals
	dict_out.update({
		(dict_sector_abv["industry_and_mining"] + "-emissions_total-mtco2e"): vec_total_emissions,
		(dict_sector_abv["industry_and_mining"] + "-electricity_total_demand-gwh"): vec_total_demand_electricity,
		(dict_sector_abv["industry_and_mining"] + "-electricity_hydrogen-gwh"): electric_demand_hydrogen,
	})

	# return
	return dict_out  # dict_emission,dict_electric_demand
