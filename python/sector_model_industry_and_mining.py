# Industry and Mining energy model developed by Centro de Energia U. de Chile using RAND python framework
# version 1.0 december 2020

import os, os.path
import time
import pandas as pd
import numpy as np
from econometric_models import model_other_industries as dem_other_industries,  model_delta_capacity,  model_capacity

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
    other_industries_plant_factor_sst = np.array(df_in["iron_plant_factor_sst"])

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

    #cost information
    #Conversion of fuel price to express all in US$/Tcal and to be coherent with the fuel prices of other sectors
    fuel_price_diesel = np.array(df_in["fuel_price_diesel"])
    industry_and_mining_fuel_price_diesel = fuel_price_diesel*fuel_price_diesel_conversion
    fuel_price_natural_gas = np.array(df_in["fuel_price_natural_gas"])
    industry_and_mining_fuel_price_natural_gas = fuel_price_natural_gas*fuel_price_natural_gas_conversion
    fuel_price_coal = np.array(df_in["fuel_price_coal"])
    industry_and_mining_fuel_price_coal = fuel_price_coal*fuel_price_coal_conversion

    fuel_price_gasoline = industry_and_mining_fuel_price_diesel*ratio_fuel_price_diesel_gasoline
    fuel_price_fuel_oil = industry_and_mining_fuel_price_diesel*ratio_fuel_price_diesel_fuel_oil
    fuel_price_kerosene = industry_and_mining_fuel_price_diesel*ratio_fuel_price_diesel_kerosene
    fuel_price_kerosene_aviation = industry_and_mining_fuel_price_diesel * ratio_fuel_price_diesel_kerosene_aviation

    industry_and_mining_fuel_price_fuel_oil = fuel_price_fuel_oil
    industry_and_mining_fuel_price_kerosene = fuel_price_kerosene
    industry_and_mining_fuel_price_gasoline = fuel_price_gasoline
    industry_and_mining_fuel_price_kerosene_aviation = fuel_price_kerosene_aviation

    industry_and_mining_fuel_price_electric = np.array(df_in["industry_and_mining_fuel_price_electric"])
    industry_and_mining_fuel_price_coke = np.array(df_in["industry_and_mining_fuel_price_coke"])
    industry_and_mining_fuel_price_biomass = np.array(df_in["industry_and_mining_fuel_price_biomass"])
    industry_and_mining_fuel_price_solar = np.array(df_in["industry_and_mining_fuel_price_solar"])
    industry_and_mining_fuel_price_hydrogen = np.array(df_in["industry_and_mining_fuel_price_hydrogen"])
    industry_and_mining_fuel_price_pliqgas = np.array(df_in["industry_and_mining_fuel_price_pliqgas"])

    industry_and_mining_investment_cost_motor_diesel = np.array(df_in["industry_and_mining_investment_cost_motor_diesel"])
    industry_and_mining_investment_cost_motor_pliqgas = np.array(df_in["industry_and_mining_investment_cost_motor_pliqgas"])
    industry_and_mining_investment_cost_motor_electric = np.array(df_in["industry_and_mining_investment_cost_motor_electric"])
    industry_and_mining_investment_cost_motor_hydrogen = np.array(df_in["industry_and_mining_investment_cost_motor_hydrogen"])
    industry_and_mining_investment_cost_heat_coal = np.array(df_in["industry_and_mining_investment_cost_heat_coal"])
    industry_and_mining_investment_cost_heat_coke = np.array(df_in["industry_and_mining_investment_cost_heat_coke"])
    industry_and_mining_investment_cost_heat_electric = np.array(df_in["industry_and_mining_investment_cost_heat_electric"])
    industry_and_mining_investment_cost_heat_solar = np.array(df_in["industry_and_mining_investment_cost_heat_solar"])
    industry_and_mining_investment_cost_heat_pliqgas = np.array(df_in["industry_and_mining_investment_cost_heat_pliqgas"])
    industry_and_mining_investment_cost_heat_natural_gas = np.array(df_in["industry_and_mining_investment_cost_heat_natural_gas"])
    industry_and_mining_investment_cost_heat_biomass = np.array(df_in["industry_and_mining_investment_cost_heat_biomass"])
    industry_and_mining_investment_cost_heat_diesel = np.array(df_in["industry_and_mining_investment_cost_heat_diesel"])
    industry_and_mining_investment_cost_heat_fuel_oil = np.array(df_in["industry_and_mining_investment_cost_heat_fuel_oil"])
    industry_and_mining_investment_cost_heat_hydrogen = np.array(df_in["industry_and_mining_investment_cost_heat_hydrogen"])

    ####################################################################################################################

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
    copper_activity_open_pit_mine = np.array(df_in["copper_activity_open_pit_mine"])
    copper_activity_subt_mine = np.array(df_in["copper_activity_subt_mine"])
    copper_activity_motor = np.array(df_in["copper_activity_motor"])
    copper_activity_other = np.array(df_in["copper_activity_other"])
    copper_activity_heat = np.array(df_in["copper_activity_heat"])
    copper_investment_cost_open_pit_mine_diesel = np.array(df_in["copper_investment_cost_open_pit_mine_diesel"])
    copper_investment_cost_open_pit_mine_electricitiy = np.array(df_in["copper_investment_cost_open_pit_mine_electricitiy"])
    copper_investment_cost_open_pit_mine_hydrogen = np.array(df_in["copper_investment_cost_open_pit_mine_hydrogen"])
    copper_investment_cost_subt_mine_diesel = np.array(df_in["copper_investment_cost_subt_mine_diesel"])
    copper_investment_cost_subt_mine_electricitiy = np.array(df_in["copper_investment_cost_subt_mine_electricitiy"])
    copper_investment_cost_subt_mine_hydrogen = np.array(df_in["copper_investment_cost_subt_mine_hydrogen"])
    copper_investment_cost_motor_diesel = np.array(df_in["copper_investment_cost_motor_diesel"])
    copper_investment_cost_motor_electricitiy = np.array(df_in["copper_investment_cost_motor_electricitiy"])
    copper_investment_cost_motor_hydrogen = np.array(df_in["copper_investment_cost_motor_hydrogen"])
    copper_investment_cost_heat_diesel = np.array(df_in["copper_investment_cost_heat_diesel"])
    copper_investment_cost_heat_electricitiy = np.array(df_in["copper_investment_cost_heat_electricitiy"])
    copper_investment_cost_heat_hydrogen = np.array(df_in["copper_investment_cost_heat_hydrogen"])
    copper_investment_cost_heat_natural_gas = np.array(df_in["copper_investment_cost_heat_natural_gas"])
    copper_investment_cost_heat_plqgas = np.array(df_in["copper_investment_cost_heat_plqgas"])
    copper_investment_cost_heat_solar = np.array(df_in["copper_investment_cost_heat_solar"])

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

    #############################################################################
    ################# COST INFORMATION ##########################################

    # OPEX (in millon US$)
    copper_OPEX_diesel = copper_dem_diesel * industry_and_mining_fuel_price_diesel / (10 ** 6)
    copper_OPEX_kerosene = copper_dem_kerosene * industry_and_mining_fuel_price_kerosene / (10 ** 6)
    copper_OPEX_natural_gas = copper_dem_natural_gas * industry_and_mining_fuel_price_natural_gas/ (10 ** 6)
    copper_OPEX_electric = copper_dem_electric * industry_and_mining_fuel_price_electric / (10 ** 6)
    copper_OPEX_hydrogen = copper_dem_hydrogen * industry_and_mining_fuel_price_hydrogen / (10 ** 6)
    copper_OPEX_pliqgas = copper_dem_pliqgas * industry_and_mining_fuel_price_pliqgas / (10 ** 6)
    copper_OPEX_fueloil = copper_dem_fueloil * industry_and_mining_fuel_price_fuel_oil / (10 ** 6)

    copper_OPEX = copper_OPEX_diesel+copper_OPEX_kerosene+copper_OPEX_natural_gas+copper_OPEX_electric+copper_OPEX_hydrogen+copper_OPEX_pliqgas+copper_OPEX_fueloil

    # capacity (MW)
    #open pit
    copper_capacity_open_pit_mine_diesel = copper_dem_open_pit_mine_diesel * fact2 * 10**3 / copper_activity_open_pit_mine
    copper_capacity_open_pit_mine_electricitiy = copper_dem_open_pit_mine_electricitiy * fact2 * 10**3/ copper_activity_open_pit_mine
    copper_capacity_open_pit_mine_hydrogen = copper_dem_open_pit_mine_hydrogen * fact2 * 10**3 / copper_activity_open_pit_mine

    copper_capacity_open_pit_mine_diesel =  model_capacity (year,copper_capacity_open_pit_mine_diesel)
    copper_capacity_open_pit_mine_electricitiy =  model_capacity (year,copper_capacity_open_pit_mine_electricitiy)
    copper_capacity_open_pit_mine_hydrogen =  model_capacity (year,copper_capacity_open_pit_mine_hydrogen)

    copper_delta_capacity_open_pit_mine_diesel = model_delta_capacity(year, copper_capacity_open_pit_mine_diesel)
    copper_delta_capacity_open_pit_mine_electricitiy = model_delta_capacity(year, copper_capacity_open_pit_mine_electricitiy)
    copper_delta_capacity_open_pit_mine_hydrogen = model_delta_capacity(year, copper_capacity_open_pit_mine_hydrogen)

    # CAPEX (in millon US$)
    copper_CAPEX_open_pit_mine_diesel = copper_delta_capacity_open_pit_mine_diesel * copper_investment_cost_open_pit_mine_diesel / (10 ** 3)
    copper_CAPEX_open_pit_mine_electricitiy = copper_delta_capacity_open_pit_mine_electricitiy * copper_investment_cost_open_pit_mine_electricitiy / (10 ** 3)
    copper_CAPEX_open_pit_mine_hydrogen = copper_delta_capacity_open_pit_mine_hydrogen * copper_investment_cost_open_pit_mine_hydrogen / (10 ** 3)
    copper_CAPEX_open_pit_mine = copper_CAPEX_open_pit_mine_diesel + copper_CAPEX_open_pit_mine_electricitiy + copper_CAPEX_open_pit_mine_hydrogen

    # Underground
    copper_capacity_subt_mine_diesel = copper_dem_subt_mine_diesel * fact2 * 10 ** 3 / copper_activity_subt_mine
    copper_capacity_subt_mine_electricitiy = copper_dem_subt_mine_electricitiy * fact2 * 10 ** 3 / copper_activity_subt_mine
    copper_capacity_subt_mine_hydrogen = copper_dem_subt_mine_hydrogen * fact2 * 10 ** 3 / copper_activity_subt_mine

    copper_capacity_subt_mine_diesel = model_capacity(year, copper_capacity_subt_mine_diesel)
    copper_capacity_subt_mine_electricitiy = model_capacity(year, copper_capacity_subt_mine_electricitiy)
    copper_capacity_subt_mine_hydrogen = model_capacity(year, copper_capacity_subt_mine_hydrogen)

    copper_delta_capacity_subt_mine_diesel = model_delta_capacity(year, copper_capacity_subt_mine_diesel)
    copper_delta_capacity_subt_mine_electricitiy = model_delta_capacity(year, copper_capacity_subt_mine_electricitiy)
    copper_delta_capacity_subt_mine_hydrogen = model_delta_capacity(year, copper_capacity_subt_mine_hydrogen)

    # CAPEX (in millon US$)
    copper_CAPEX_subt_mine_diesel = copper_delta_capacity_subt_mine_diesel * copper_investment_cost_subt_mine_diesel / (10 ** 3)
    copper_CAPEX_subt_mine_electricitiy = copper_delta_capacity_subt_mine_electricitiy * copper_investment_cost_subt_mine_electricitiy / (10 ** 3)
    copper_CAPEX_subt_mine_hydrogen = copper_delta_capacity_subt_mine_hydrogen * copper_investment_cost_subt_mine_hydrogen / (10 ** 3)
    copper_CAPEX_subt_mine = copper_CAPEX_subt_mine_diesel + copper_CAPEX_subt_mine_electricitiy + copper_CAPEX_subt_mine_hydrogen

    # Motor
    copper_capacity_motor_diesel = copper_dem_motor_diesel * fact2 * 10 ** 3 / copper_activity_motor
    copper_capacity_motor_electricitiy = copper_dem_motor_electricitiy * fact2 * 10 ** 3 / copper_activity_motor
    copper_capacity_motor_hydrogen = copper_dem_motor_hydrogen * fact2 * 10 ** 3 / copper_activity_motor

    copper_capacity_motor_diesel = model_capacity(year, copper_capacity_motor_diesel)
    copper_capacity_motor_electricitiy = model_capacity(year, copper_capacity_motor_electricitiy)
    copper_capacity_motor_hydrogen = model_capacity(year, copper_capacity_motor_hydrogen)

    copper_delta_capacity_motor_diesel = model_delta_capacity(year, copper_capacity_motor_diesel)
    copper_delta_capacity_motor_electricitiy = model_delta_capacity(year, copper_capacity_motor_electricitiy)
    copper_delta_capacity_motor_hydrogen = model_delta_capacity(year, copper_capacity_motor_hydrogen)

    # CAPEX (in millon US$)
    copper_CAPEX_motor_diesel = copper_delta_capacity_motor_diesel * copper_investment_cost_motor_diesel / (10 ** 3)
    copper_CAPEX_motor_electricitiy = copper_delta_capacity_motor_electricitiy * copper_investment_cost_motor_electricitiy / (10 ** 3)
    copper_CAPEX_motor_hydrogen = copper_delta_capacity_motor_hydrogen * copper_investment_cost_motor_hydrogen / (10 ** 3)
    copper_CAPEX_motor = copper_CAPEX_motor_diesel + copper_CAPEX_motor_electricitiy + copper_CAPEX_motor_hydrogen

    # HEAT
    copper_capacity_heat_diesel = copper_dem_heat_diesel * fact2 * 10 ** 3 / copper_activity_heat
    copper_capacity_heat_electricitiy = copper_dem_heat_electricitiy * fact2 * 10 ** 3 / copper_activity_heat
    copper_capacity_heat_hydrogen = copper_dem_heat_hydrogen * fact2 * 10 ** 3 / copper_activity_heat
    copper_capacity_heat_natural_gas = copper_dem_heat_natural_gas * fact2 * 10 ** 3 / copper_activity_heat
    copper_capacity_heat_plqgas = copper_dem_heat_plqgas * fact2 * 10 ** 3 / copper_activity_heat
    copper_capacity_heat_solar = copper_dem_heat_solar * fact2 * 10 ** 3 / (8760*other_industries_plant_factor_sst)

    copper_capacity_heat_diesel = model_capacity(year, copper_capacity_heat_diesel)
    copper_capacity_heat_electricitiy = model_capacity(year, copper_capacity_heat_electricitiy)
    copper_capacity_heat_hydrogen = model_capacity(year, copper_capacity_heat_hydrogen)
    copper_capacity_heat_natural_gas = model_capacity(year, copper_capacity_heat_natural_gas)
    copper_capacity_heat_plqgas = model_capacity(year, copper_capacity_heat_plqgas)
    copper_capacity_heat_solar = model_capacity(year, copper_capacity_heat_solar)

    copper_delta_capacity_heat_diesel = model_delta_capacity(year, copper_capacity_heat_diesel)
    copper_delta_capacity_heat_electricitiy = model_delta_capacity(year, copper_capacity_heat_electricitiy)
    copper_delta_capacity_heat_hydrogen = model_delta_capacity(year, copper_capacity_heat_hydrogen)
    copper_delta_capacity_heat_natural_gas = model_delta_capacity(year, copper_capacity_heat_natural_gas)
    copper_delta_capacity_heat_plqgas = model_delta_capacity(year, copper_capacity_heat_plqgas)
    copper_delta_capacity_heat_solar = model_delta_capacity(year, copper_capacity_heat_solar)

    # CAPEX (in millon US$)
    copper_CAPEX_heat_diesel = copper_delta_capacity_heat_diesel * copper_investment_cost_heat_diesel / (10 ** 3)
    copper_CAPEX_heat_electricitiy = copper_delta_capacity_heat_electricitiy * copper_investment_cost_heat_electricitiy / (10 ** 3)
    copper_CAPEX_heat_hydrogen = copper_delta_capacity_heat_hydrogen * copper_investment_cost_heat_hydrogen / (10 ** 3)
    copper_CAPEX_heat_natural_gas = copper_delta_capacity_heat_natural_gas * copper_investment_cost_heat_natural_gas / (10 ** 3)
    copper_CAPEX_heat_nplqgas = copper_delta_capacity_heat_plqgas * copper_investment_cost_heat_plqgas/ (10 ** 3)
    copper_CAPEX_heat_solar = copper_delta_capacity_heat_solar * copper_investment_cost_heat_solar / (10 ** 3)
    copper_CAPEX_heat = copper_CAPEX_heat_diesel + copper_CAPEX_heat_electricitiy + copper_CAPEX_heat_hydrogen+copper_CAPEX_heat_natural_gas+copper_CAPEX_heat_nplqgas+copper_CAPEX_heat_solar

    # total CAPEX
    copper_CAPEX = copper_CAPEX_open_pit_mine + copper_CAPEX_subt_mine + copper_CAPEX_motor+copper_CAPEX_heat

    ########################################################################################################################

    dict_emission = {"copper": copper_emission}
    dict_electric_demand = {"copper": copper_dem_electric * fact2}
    # CAPEX, OPEX
    dict_CAPEX = {"copper": copper_CAPEX}
    dict_OPEX ={"copper": copper_OPEX}


    ####################################################################################################################
    # SUB SECTOR: PULP ENERGY MODEL - Papel y Celulosa

    # Read input parameters defined in parameter_ranges.csv

    pulp_production = np.array(df_in["pulp_production"])
    pulp_intensity = np.array(df_in["pulp_intensity"])
    pulp_share_motor = np.array(df_in["pulp_share_motor"])
    pulp_share_other = np.array(df_in["pulp_share_other"])
    pulp_share_heat = np.array(df_in["pulp_share_heat"])
    pulp_motor_diesel = np.array(df_in["pulp_motor_diesel"])
    pulp_motor_pliqgas = np.array(df_in["pulp_motor_pliqgas"])
    pulp_motor_electric = np.array(df_in["pulp_motor_electric"])
    pulp_motor_hydrogen = np.array(df_in["pulp_motor_hydrogen"])
    pulp_other_electric = np.array(df_in["pulp_other_electric"])
    pulp_heat_coal = np.array(df_in["pulp_heat_coal"])
    pulp_heat_electric = np.array(df_in["pulp_heat_electric"])
    pulp_heat_solar = np.array(df_in["pulp_heat_solar"])
    pulp_heat_pliqgas = np.array(df_in["pulp_heat_pliqgas"])
    pulp_heat_natural_gas = np.array(df_in["pulp_heat_natural_gas"])
    pulp_heat_biomass = np.array(df_in["pulp_heat_biomass"])
    pulp_heat_diesel = np.array(df_in["pulp_heat_diesel"])
    pulp_heat_fuel_oil = np.array(df_in["pulp_heat_fuel_oil"])
    pulp_heat_hydrogen = np.array(df_in["pulp_heat_hydrogen"])
    pulp_efficiency_motor_diesel = np.array(df_in["pulp_efficiency_motor_diesel"])
    pulp_efficiency_motor_pliqgas = np.array(df_in["pulp_efficiency_motor_pliqgas"])
    pulp_efficiency_motor_electric = np.array(df_in["pulp_efficiency_motor_electric"])
    pulp_efficiency_motor_hydrogen = np.array(df_in["pulp_efficiency_motor_hydrogen"])
    pulp_efficiency_other_electric = np.array(df_in["pulp_efficiency_other_electric"])
    pulp_efficiency_heat_coal = np.array(df_in["pulp_efficiency_heat_coal"])
    pulp_efficiency_heat_electric = np.array(df_in["pulp_efficiency_heat_electric"])
    pulp_efficiency_heat_solar = np.array(df_in["pulp_efficiency_heat_solar"])
    pulp_efficiency_heat_pliqgas = np.array(df_in["pulp_efficiency_heat_pliqgas"])
    pulp_efficiency_heat_natural_gas = np.array(df_in["pulp_efficiency_heat_natural_gas"])
    pulp_efficiency_heat_biomass = np.array(df_in["pulp_efficiency_heat_biomass"])
    pulp_efficiency_heat_diesel = np.array(df_in["pulp_efficiency_heat_diesel"])
    pulp_efficiency_heat_fuel_oil = np.array(df_in["pulp_efficiency_heat_fuel_oil"])
    pulp_efficiency_heat_hydrogen = np.array(df_in["pulp_efficiency_heat_hydrogen"])
    pulp_emission_fact_diesel = np.array(df_in["pulp_emission_fact_diesel"])
    pulp_emission_fact_natural_gas = np.array(df_in["pulp_emission_fact_natural_gas"])
    pulp_emission_fact_coal = np.array(df_in["pulp_emission_fact_coal"])
    pulp_emission_fact_pliqgas = np.array(df_in["pulp_emission_fact_pliqgas"])
    pulp_emission_fact_fueloil = np.array(df_in["pulp_emission_fact_fueloil"])
    pulp_plant_factor_sst = np.array(df_in["pulp_plant_factor_sst"])
    pulp_activity_motor = np.array(df_in["pulp_activity_motor"])
    pulp_activity_other = np.array(df_in["pulp_activity_other"])
    pulp_activity_heat = np.array(df_in["pulp_activity_heat"])

    # calculate useful total demand

    pulp_useful_energy = pulp_production * pulp_intensity

    # calculate demand in Tcal by en use
    pulp_dem_motor_diesel = pulp_useful_energy * pulp_share_motor * pulp_motor_diesel / pulp_efficiency_motor_diesel
    pulp_dem_motor_pliqgas = pulp_useful_energy * pulp_share_motor * pulp_motor_pliqgas / pulp_efficiency_motor_pliqgas
    pulp_dem_motor_electric = pulp_useful_energy * pulp_share_motor * pulp_motor_electric / pulp_efficiency_motor_electric
    pulp_dem_motor_hydrogen = pulp_useful_energy * pulp_share_motor * pulp_motor_hydrogen / pulp_efficiency_motor_hydrogen

    pulp_dem_other_electric = pulp_useful_energy * pulp_share_other * pulp_other_electric / pulp_efficiency_other_electric

    pulp_dem_heat_coal = pulp_useful_energy * pulp_share_heat * pulp_heat_coal / pulp_efficiency_heat_coal
    pulp_dem_heat_electric = pulp_useful_energy * pulp_share_heat * pulp_heat_electric / pulp_efficiency_heat_electric
    pulp_dem_heat_solar = pulp_useful_energy * pulp_share_heat * pulp_heat_solar / pulp_efficiency_heat_solar
    pulp_dem_heat_pliqgas = pulp_useful_energy * pulp_share_heat * pulp_heat_pliqgas / pulp_efficiency_heat_pliqgas
    pulp_dem_heat_natural_gas = pulp_useful_energy * pulp_share_heat * pulp_heat_natural_gas / pulp_efficiency_heat_natural_gas
    pulp_dem_heat_biomass = pulp_useful_energy * pulp_share_heat * pulp_heat_biomass / pulp_efficiency_heat_biomass
    pulp_dem_heat_diesel = pulp_useful_energy * pulp_share_heat * pulp_heat_diesel / pulp_efficiency_heat_diesel
    pulp_dem_heat_fuel_oil = pulp_useful_energy * pulp_share_heat * pulp_heat_fuel_oil / pulp_efficiency_heat_fuel_oil
    pulp_dem_heat_hydrogen = pulp_useful_energy * pulp_share_heat * pulp_heat_hydrogen / pulp_efficiency_heat_hydrogen

    # total demand by type of energy

    pulp_dem_diesel = pulp_dem_motor_diesel + pulp_dem_heat_diesel
    pulp_dem_natural_gas = pulp_dem_heat_natural_gas
    pulp_dem_electric = pulp_dem_motor_electric + pulp_dem_other_electric + pulp_dem_heat_electric
    pulp_dem_coal = pulp_dem_heat_coal
    pulp_dem_biomass = pulp_dem_heat_biomass
    pulp_dem_solar = pulp_dem_heat_solar
    pulp_dem_hydrogen = pulp_dem_motor_hydrogen + pulp_dem_heat_hydrogen
    pulp_dem_pliqgas = pulp_dem_motor_pliqgas + pulp_dem_heat_pliqgas
    pulp_dem_fueloil = pulp_dem_heat_fuel_oil

    # calculate demand in Tcal by en use
    pulp_emission_diesel = pulp_dem_diesel * pulp_emission_fact_diesel * fact / (10 ** 9)
    pulp_emission_natural_gas = pulp_dem_natural_gas * pulp_emission_fact_natural_gas * fact / (10 ** 9)
    pulp_emission_coal = pulp_dem_coal * pulp_emission_fact_coal * fact / (10 ** 9)
    pulp_emission_pliqgas = pulp_dem_pliqgas * pulp_emission_fact_pliqgas * fact / (10 ** 9)
    pulp_emission_fueloil = pulp_dem_fueloil * pulp_emission_fact_fueloil * fact / (10 ** 9)
    pulp_emission = pulp_emission_diesel + pulp_emission_natural_gas + pulp_emission_coal + pulp_emission_pliqgas + pulp_emission_fueloil

    # electric demand to produce hydrogen
    electric_demand_hydrogen = electric_demand_hydrogen + pulp_dem_hydrogen / electrolyzer_efficiency * share_electric_grid_to_hydrogen

    #############################################################################
    ################# COST INFORMATION ##########################################

    # capacity
    pulp_capacity_motor_diesel = pulp_dem_motor_diesel * fact2 * (10 ** 3) / pulp_activity_motor
    pulp_capacity_motor_pliqgas = pulp_dem_motor_pliqgas * fact2 * (10 ** 3) / pulp_activity_motor
    pulp_capacity_motor_electric = pulp_dem_motor_electric * fact2 * (10 ** 3) / pulp_activity_motor
    pulp_capacity_motor_hydrogen = pulp_dem_motor_hydrogen * fact2 * (10 ** 3) / pulp_activity_motor
    pulp_capacity_heat_coal = pulp_dem_heat_coal * fact2 * (10 ** 3) / pulp_activity_heat
    pulp_capacity_heat_electric = pulp_dem_heat_electric * fact2 * (10 ** 3) / pulp_activity_heat
    pulp_capacity_heat_solar = pulp_dem_heat_solar * fact2 * (10 ** 3) / (8760*other_industries_plant_factor_sst)
    pulp_capacity_heat_pliqgas = pulp_dem_heat_pliqgas * fact2 * (10 ** 3) / pulp_activity_heat
    pulp_capacity_heat_natural_gas = pulp_dem_heat_natural_gas * fact2 * (10 ** 3) / pulp_activity_heat
    pulp_capacity_heat_biomass = pulp_dem_heat_biomass * fact2 * (10 ** 3) / pulp_activity_heat
    pulp_capacity_heat_diesel = pulp_dem_heat_diesel * fact2 * (10 ** 3) / pulp_activity_heat
    pulp_capacity_heat_fuel_oil = pulp_dem_heat_fuel_oil * fact2 * (10 ** 3) / pulp_activity_heat
    pulp_capacity_heat_hydrogen = pulp_dem_heat_hydrogen * fact2 * (10 ** 3) / pulp_activity_heat

    pulp_capacity_motor_diesel = model_capacity(year, pulp_capacity_motor_diesel)
    pulp_capacity_motor_pliqgas = model_capacity(year, pulp_capacity_motor_pliqgas)
    pulp_capacity_motor_electric = model_capacity(year, pulp_capacity_motor_electric)
    pulp_capacity_motor_hydrogen = model_capacity(year, pulp_capacity_motor_hydrogen)
    pulp_capacity_heat_coal = model_capacity(year, pulp_capacity_heat_coal)
    pulp_capacity_heat_electric = model_capacity(year, pulp_capacity_heat_electric)
    pulp_capacity_heat_solar = model_capacity(year, pulp_capacity_heat_solar)
    pulp_capacity_heat_pliqgas = model_capacity(year, pulp_capacity_heat_pliqgas)
    pulp_capacity_heat_natural_gas = model_capacity(year, pulp_capacity_heat_natural_gas)
    pulp_capacity_heat_biomass = model_capacity(year, pulp_capacity_heat_biomass)
    pulp_capacity_heat_diesel = model_capacity(year, pulp_capacity_heat_diesel)
    pulp_capacity_heat_fuel_oil = model_capacity(year, pulp_capacity_heat_fuel_oil)
    pulp_capacity_heat_hydrogen = model_capacity(year, pulp_capacity_heat_hydrogen)

    pulp_delta_capacity_motor_diesel = model_delta_capacity(year, pulp_capacity_motor_diesel)
    pulp_delta_capacity_motor_pliqgas = model_delta_capacity(year, pulp_capacity_motor_pliqgas)
    pulp_delta_capacity_motor_electric = model_delta_capacity(year, pulp_capacity_motor_electric)
    pulp_delta_capacity_motor_hydrogen = model_delta_capacity(year, pulp_capacity_motor_hydrogen)
    pulp_delta_capacity_heat_coal = model_delta_capacity(year, pulp_capacity_heat_coal)
    pulp_delta_capacity_heat_electric = model_delta_capacity(year, pulp_capacity_heat_electric)
    pulp_delta_capacity_heat_solar = model_delta_capacity(year, pulp_capacity_heat_solar)
    pulp_delta_capacity_heat_pliqgas = model_delta_capacity(year, pulp_capacity_heat_pliqgas)
    pulp_delta_capacity_heat_natural_gas = model_delta_capacity(year, pulp_capacity_heat_natural_gas)
    pulp_delta_capacity_heat_biomass = model_delta_capacity(year, pulp_capacity_heat_biomass)
    pulp_delta_capacity_heat_diesel = model_delta_capacity(year, pulp_capacity_heat_diesel)
    pulp_delta_capacity_heat_fuel_oil = model_delta_capacity(year, pulp_capacity_heat_fuel_oil)
    pulp_delta_capacity_heat_hydrogen = model_delta_capacity(year, pulp_capacity_heat_hydrogen)

    # OPEX
    pulp_OPEX_diesel = pulp_dem_diesel * industry_and_mining_fuel_price_diesel / (10 ** 6)
    pulp_OPEX_natural_gas = pulp_dem_natural_gas * industry_and_mining_fuel_price_natural_gas / (10 ** 6)
    pulp_OPEX_electric = pulp_dem_electric * industry_and_mining_fuel_price_electric / (10 ** 6)
    pulp_OPEX_coal = pulp_dem_coal * industry_and_mining_fuel_price_coal / (10 ** 6)
    pulp_OPEX_biomass = pulp_dem_biomass * industry_and_mining_fuel_price_biomass / (10 ** 6)
    pulp_OPEX_solar = pulp_dem_solar * industry_and_mining_fuel_price_solar / (10 ** 6)
    pulp_OPEX_hydrogen = pulp_dem_hydrogen * industry_and_mining_fuel_price_hydrogen / (10 ** 6)
    pulp_OPEX_pliqgas = pulp_dem_pliqgas * industry_and_mining_fuel_price_pliqgas / (10 ** 6)
    pulp_OPEX_fuel_oil = pulp_dem_fueloil * industry_and_mining_fuel_price_fuel_oil / (10 ** 6)
    pulp_OPEX = pulp_OPEX_diesel + pulp_OPEX_natural_gas + pulp_OPEX_electric + pulp_OPEX_coal + pulp_OPEX_biomass + pulp_OPEX_solar + pulp_OPEX_hydrogen + pulp_OPEX_pliqgas + pulp_OPEX_fuel_oil

    # CAPEX
    pulp_CAPEX_motor_diesel = pulp_delta_capacity_motor_diesel * industry_and_mining_investment_cost_motor_diesel / (10 ** 3)
    pulp_CAPEX_motor_pliqgas = pulp_delta_capacity_motor_pliqgas * industry_and_mining_investment_cost_motor_pliqgas / (10 ** 3)
    pulp_CAPEX_motor_electric = pulp_delta_capacity_motor_electric * industry_and_mining_investment_cost_motor_electric / (10 ** 3)
    pulp_CAPEX_motor_hydrogen = pulp_delta_capacity_motor_hydrogen * industry_and_mining_investment_cost_motor_hydrogen / (10 ** 3)
    pulp_CAPEX_motor = pulp_CAPEX_motor_diesel + pulp_CAPEX_motor_pliqgas + pulp_CAPEX_motor_electric + pulp_CAPEX_motor_hydrogen

    pulp_CAPEX_heat_coal = pulp_delta_capacity_heat_coal * industry_and_mining_investment_cost_heat_coal / (10 ** 3)
    pulp_CAPEX_heat_electric = pulp_delta_capacity_heat_electric * industry_and_mining_investment_cost_heat_electric / (10 ** 3)
    pulp_CAPEX_heat_solar = pulp_delta_capacity_heat_solar * industry_and_mining_investment_cost_heat_solar / (10 ** 3)
    pulp_CAPEX_heat_pliqgas = pulp_delta_capacity_heat_pliqgas * industry_and_mining_investment_cost_heat_pliqgas / (10 ** 3)
    pulp_CAPEX_heat_natural_gas = pulp_delta_capacity_heat_natural_gas * industry_and_mining_investment_cost_heat_natural_gas / (10 ** 3)
    pulp_CAPEX_heat_biomass = pulp_delta_capacity_heat_biomass * industry_and_mining_investment_cost_heat_biomass / (10 ** 3)
    pulp_CAPEX_heat_diesel = pulp_delta_capacity_heat_diesel * industry_and_mining_investment_cost_heat_diesel / (10 ** 3)
    pulp_CAPEX_heat_fuel_oil = pulp_delta_capacity_heat_fuel_oil * industry_and_mining_investment_cost_heat_fuel_oil / (10 ** 3)
    pulp_CAPEX_heat_hydrogen = pulp_delta_capacity_heat_hydrogen * industry_and_mining_investment_cost_heat_hydrogen / (10 ** 3)
    pulp_CAPEX_heat = pulp_CAPEX_heat_coal + pulp_CAPEX_heat_electric + pulp_CAPEX_heat_solar + pulp_CAPEX_heat_pliqgas + pulp_CAPEX_heat_natural_gas + pulp_CAPEX_heat_biomass + pulp_CAPEX_heat_diesel + pulp_CAPEX_heat_fuel_oil + pulp_CAPEX_heat_hydrogen

    # total CAPEX
    pulp_CAPEX = pulp_CAPEX_motor + pulp_CAPEX_heat


    # update
    dict_emission.update({"pulp": pulp_emission})
    dict_electric_demand.update({"pulp": pulp_dem_electric * fact2})
    # CAPEX, OPEX
    dict_CAPEX.update({"other_pulp": pulp_CAPEX})
    dict_OPEX.update({"other_pulp": pulp_OPEX})

    ####################################################################################################################

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
    other_industries_activity_motor = np.array(df_in["other_industries_activity_motor"])
    other_industries_activity_other = np.array(df_in["other_industries_activity_other"])
    other_industries_activity_heat = np.array(df_in["other_industries_activity_heat"])


    #
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

    other_industries_emission_diesel = other_industries_dem_diesel * other_industries_emission_fact_diesel * fact / (10 ** 9)
    other_industries_emission_natural_gas = other_industries_dem_natural_gas * other_industries_emission_fact_natural_gas * fact / (10 ** 9)
    other_industries_emission_coal = other_industries_dem_coal * other_industries_emission_fact_coal * fact / (10 ** 9)
    other_industries_emission_pliqgas = other_industries_dem_pliqgas * other_industries_emission_fact_pliqgas * fact / (10 ** 9)
    other_industries_emission_fueloil = other_industries_dem_fueloil * other_industries_emission_fact_fueloil * fact / (10 ** 9)
    other_industries_emission = other_industries_emission_diesel + other_industries_emission_natural_gas + other_industries_emission_coal + other_industries_emission_pliqgas + other_industries_emission_fueloil

    # electric demand to produce hydrogen
    electric_demand_hydrogen = electric_demand_hydrogen + other_industries_dem_hydrogen / electrolyzer_efficiency * share_electric_grid_to_hydrogen

    #############################################################################
    ################# COST INFORMATION ##########################################

    # capacity
    other_industries_capacity_motor_diesel = other_industries_dem_motor_diesel * fact2 * (10 ** 3) / other_industries_activity_motor
    other_industries_capacity_motor_pliqgas = other_industries_dem_motor_pliqgas * fact2 * (10 ** 3) / other_industries_activity_motor
    other_industries_capacity_motor_electric = other_industries_dem_motor_electric * fact2 * (10 ** 3) / other_industries_activity_motor
    other_industries_capacity_motor_hydrogen = other_industries_dem_motor_hydrogen * fact2 * (10 ** 3) / other_industries_activity_motor
    other_industries_capacity_heat_coal = other_industries_dem_heat_coal * fact2 * (10 ** 3) / other_industries_activity_heat
    other_industries_capacity_heat_electric = other_industries_dem_heat_electric * fact2 * (10 ** 3) / other_industries_activity_heat
    other_industries_capacity_heat_solar = other_industries_dem_heat_solar * fact2 * (10 ** 3) / (8760*other_industries_plant_factor_sst)
    other_industries_capacity_heat_pliqgas = other_industries_dem_heat_pliqgas * fact2 * (10 ** 3) / other_industries_activity_heat
    other_industries_capacity_heat_natural_gas = other_industries_dem_heat_natural_gas * fact2 * (10 ** 3) / other_industries_activity_heat
    other_industries_capacity_heat_biomass = other_industries_dem_heat_biomass * fact2 * (10 ** 3) / other_industries_activity_heat
    other_industries_capacity_heat_diesel = other_industries_dem_heat_diesel * fact2 * (10 ** 3) / other_industries_activity_heat
    other_industries_capacity_heat_fuel_oil = other_industries_dem_heat_fuel_oil * fact2 * (10 ** 3) / other_industries_activity_heat
    other_industries_capacity_heat_hydrogen = other_industries_dem_heat_hydrogen * fact2 * (10 ** 3) / other_industries_activity_heat

    other_industries_capacity_motor_diesel = model_capacity(year, other_industries_capacity_motor_diesel)
    other_industries_capacity_motor_pliqgas = model_capacity(year, other_industries_capacity_motor_pliqgas)
    other_industries_capacity_motor_electric = model_capacity(year, other_industries_capacity_motor_electric)
    other_industries_capacity_motor_hydrogen = model_capacity(year, other_industries_capacity_motor_hydrogen)
    other_industries_capacity_heat_coal = model_capacity(year, other_industries_capacity_heat_coal)
    other_industries_capacity_heat_electric = model_capacity(year, other_industries_capacity_heat_electric)
    other_industries_capacity_heat_solar = model_capacity(year, other_industries_capacity_heat_solar)
    other_industries_capacity_heat_pliqgas = model_capacity(year, other_industries_capacity_heat_pliqgas)
    other_industries_capacity_heat_natural_gas = model_capacity(year, other_industries_capacity_heat_natural_gas)
    other_industries_capacity_heat_biomass = model_capacity(year, other_industries_capacity_heat_biomass)
    other_industries_capacity_heat_diesel = model_capacity(year, other_industries_capacity_heat_diesel)
    other_industries_capacity_heat_fuel_oil = model_capacity(year, other_industries_capacity_heat_fuel_oil)
    other_industries_capacity_heat_hydrogen = model_capacity(year, other_industries_capacity_heat_hydrogen)

    other_industries_delta_capacity_motor_diesel = model_delta_capacity(year, other_industries_capacity_motor_diesel)
    other_industries_delta_capacity_motor_pliqgas = model_delta_capacity(year, other_industries_capacity_motor_pliqgas)
    other_industries_delta_capacity_motor_electric = model_delta_capacity(year,other_industries_capacity_motor_electric)
    other_industries_delta_capacity_motor_hydrogen = model_delta_capacity(year,other_industries_capacity_motor_hydrogen)
    other_industries_delta_capacity_heat_coal = model_delta_capacity(year, other_industries_capacity_heat_coal)
    other_industries_delta_capacity_heat_electric = model_delta_capacity(year, other_industries_capacity_heat_electric)
    other_industries_delta_capacity_heat_solar = model_delta_capacity(year, other_industries_capacity_heat_solar)
    other_industries_delta_capacity_heat_pliqgas = model_delta_capacity(year, other_industries_capacity_heat_pliqgas)
    other_industries_delta_capacity_heat_natural_gas = model_delta_capacity(year,other_industries_capacity_heat_natural_gas)
    other_industries_delta_capacity_heat_biomass = model_delta_capacity(year, other_industries_capacity_heat_biomass)
    other_industries_delta_capacity_heat_diesel = model_delta_capacity(year, other_industries_capacity_heat_diesel)
    other_industries_delta_capacity_heat_fuel_oil = model_delta_capacity(year, other_industries_capacity_heat_fuel_oil)
    other_industries_delta_capacity_heat_hydrogen = model_delta_capacity(year, other_industries_capacity_heat_hydrogen)

    #OPEX
    other_industries_OPEX_diesel = other_industries_dem_diesel * industry_and_mining_fuel_price_diesel / (10 ** 6)
    other_industries_OPEX_natural_gas = other_industries_dem_natural_gas * industry_and_mining_fuel_price_natural_gas / (10 ** 6)
    other_industries_OPEX_electric = other_industries_dem_electric * industry_and_mining_fuel_price_electric / (10 ** 6)
    other_industries_OPEX_coal = other_industries_dem_coal * industry_and_mining_fuel_price_coal / (10 ** 6)
    other_industries_OPEX_biomass = other_industries_dem_biomass * industry_and_mining_fuel_price_biomass / (10 ** 6)
    other_industries_OPEX_solar = other_industries_dem_solar * industry_and_mining_fuel_price_solar / (10 ** 6)
    other_industries_OPEX_hydrogen = other_industries_dem_hydrogen * industry_and_mining_fuel_price_hydrogen / (10 ** 6)
    other_industries_OPEX_pliqgas = other_industries_dem_pliqgas * industry_and_mining_fuel_price_pliqgas / (10 ** 6)
    other_industries_OPEX_fuel_oil = other_industries_dem_fueloil * industry_and_mining_fuel_price_fuel_oil / (10 ** 6)
    other_industries_OPEX = other_industries_OPEX_diesel+other_industries_OPEX_natural_gas+other_industries_OPEX_electric+other_industries_OPEX_coal+other_industries_OPEX_biomass+other_industries_OPEX_solar+other_industries_OPEX_hydrogen+other_industries_OPEX_pliqgas+other_industries_OPEX_fuel_oil

    #CAPEX
    other_industries_CAPEX_motor_diesel = other_industries_delta_capacity_motor_diesel * industry_and_mining_investment_cost_motor_diesel / (10 ** 3)
    other_industries_CAPEX_motor_pliqgas = other_industries_delta_capacity_motor_pliqgas * industry_and_mining_investment_cost_motor_pliqgas / (10 ** 3)
    other_industries_CAPEX_motor_electric = other_industries_delta_capacity_motor_electric * industry_and_mining_investment_cost_motor_electric / (10 ** 3)
    other_industries_CAPEX_motor_hydrogen = other_industries_delta_capacity_motor_hydrogen * industry_and_mining_investment_cost_motor_hydrogen / (10 ** 3)
    other_industries_CAPEX_motor = other_industries_CAPEX_motor_diesel + other_industries_CAPEX_motor_pliqgas + other_industries_CAPEX_motor_electric + other_industries_CAPEX_motor_hydrogen

    other_industries_CAPEX_heat_coal = other_industries_delta_capacity_heat_coal * industry_and_mining_investment_cost_heat_coal / (10 ** 3)
    other_industries_CAPEX_heat_electric = other_industries_delta_capacity_heat_electric * industry_and_mining_investment_cost_heat_electric / (10 ** 3)
    other_industries_CAPEX_heat_solar = other_industries_delta_capacity_heat_solar * industry_and_mining_investment_cost_heat_solar / (10 ** 3)
    other_industries_CAPEX_heat_pliqgas = other_industries_delta_capacity_heat_pliqgas * industry_and_mining_investment_cost_heat_pliqgas / (10 ** 3)
    other_industries_CAPEX_heat_natural_gas = other_industries_delta_capacity_heat_natural_gas * industry_and_mining_investment_cost_heat_natural_gas / (10 ** 3)
    other_industries_CAPEX_heat_biomass = other_industries_delta_capacity_heat_biomass * industry_and_mining_investment_cost_heat_biomass / (10 ** 3)
    other_industries_CAPEX_heat_diesel = other_industries_delta_capacity_heat_diesel * industry_and_mining_investment_cost_heat_diesel / (10 ** 3)
    other_industries_CAPEX_heat_fuel_oil = other_industries_delta_capacity_heat_fuel_oil * industry_and_mining_investment_cost_heat_fuel_oil / (10 ** 3)
    other_industries_CAPEX_heat_hydrogen = other_industries_delta_capacity_heat_hydrogen * industry_and_mining_investment_cost_heat_hydrogen / (10 ** 3)
    other_industries_CAPEX_heat = other_industries_CAPEX_heat_coal + other_industries_CAPEX_heat_electric + other_industries_CAPEX_heat_solar + other_industries_CAPEX_heat_pliqgas + other_industries_CAPEX_heat_natural_gas + other_industries_CAPEX_heat_biomass + other_industries_CAPEX_heat_diesel + other_industries_CAPEX_heat_fuel_oil + other_industries_CAPEX_heat_hydrogen

    #total CAPEX
    other_industries_CAPEX = other_industries_CAPEX_motor+other_industries_CAPEX_heat

    # update
    dict_emission.update({"other_industries": other_industries_emission})
    dict_electric_demand.update({"other_industries": other_industries_dem_electric * fact2})
    #CAPEX, OPEX
    dict_CAPEX.update({"other_industries": other_industries_CAPEX})
    dict_OPEX.update({"other_industries": other_industries_OPEX})

    ####################################################################################################################
    # SUB SECTOR: Other mining industries - Minas varias

    other_mining_production = np.array(df_in["other_mining_production"])
    other_mining_intensity = np.array(df_in["other_mining_intensity"])
    other_mining_share_motor = np.array(df_in["other_mining_share_motor"])
    other_mining_share_other = np.array(df_in["other_mining_share_other"])
    other_mining_share_heat = np.array(df_in["other_mining_share_heat"])
    other_mining_motor_diesel = np.array(df_in["other_mining_motor_diesel"])
    other_mining_motor_pliqgas = np.array(df_in["other_mining_motor_pliqgas"])
    other_mining_motor_electric = np.array(df_in["other_mining_motor_electric"])
    other_mining_motor_hydrogen = np.array(df_in["other_mining_motor_hydrogen"])
    other_mining_other_electric = np.array(df_in["other_mining_other_electric"])
    other_mining_heat_coal = np.array(df_in["other_mining_heat_coal"])
    other_mining_heat_electric = np.array(df_in["other_mining_heat_electric"])
    other_mining_heat_solar = np.array(df_in["other_mining_heat_solar"])
    other_mining_heat_pliqgas = np.array(df_in["other_mining_heat_pliqgas"])
    other_mining_heat_natural_gas = np.array(df_in["other_mining_heat_natural_gas"])
    other_mining_heat_biomass = np.array(df_in["other_mining_heat_biomass"])
    other_mining_heat_diesel = np.array(df_in["other_mining_heat_diesel"])
    other_mining_heat_fuel_oil = np.array(df_in["other_mining_heat_fuel_oil"])
    other_mining_heat_hydrogen = np.array(df_in["other_mining_heat_hydrogen"])
    other_mining_efficiency_motor_diesel = np.array(df_in["other_mining_efficiency_motor_diesel"])
    other_mining_efficiency_motor_pliqgas = np.array(df_in["other_mining_efficiency_motor_pliqgas"])
    other_mining_efficiency_motor_electric = np.array(df_in["other_mining_efficiency_motor_electric"])
    other_mining_efficiency_motor_hydrogen = np.array(df_in["other_mining_efficiency_motor_hydrogen"])
    other_mining_efficiency_other_electric = np.array(df_in["other_mining_efficiency_other_electric"])
    other_mining_efficiency_heat_coal = np.array(df_in["other_mining_efficiency_heat_coal"])
    other_mining_efficiency_heat_electric = np.array(df_in["other_mining_efficiency_heat_electric"])
    other_mining_efficiency_heat_solar = np.array(df_in["other_mining_efficiency_heat_solar"])
    other_mining_efficiency_heat_pliqgas = np.array(df_in["other_mining_efficiency_heat_pliqgas"])
    other_mining_efficiency_heat_natural_gas = np.array(df_in["other_mining_efficiency_heat_natural_gas"])
    other_mining_efficiency_heat_biomass = np.array(df_in["other_mining_efficiency_heat_biomass"])
    other_mining_efficiency_heat_diesel = np.array(df_in["other_mining_efficiency_heat_diesel"])
    other_mining_efficiency_heat_fuel_oil = np.array(df_in["other_mining_efficiency_heat_fuel_oil"])
    other_mining_efficiency_heat_hydrogen = np.array(df_in["other_mining_efficiency_heat_hydrogen"])
    other_mining_emission_fact_diesel = np.array(df_in["other_mining_emission_fact_diesel"])
    other_mining_emission_fact_natural_gas = np.array(df_in["other_mining_emission_fact_natural_gas"])
    other_mining_emission_fact_coal = np.array(df_in["other_mining_emission_fact_coal"])
    other_mining_emission_fact_pliqgas = np.array(df_in["other_mining_emission_fact_pliqgas"])
    other_mining_emission_fact_fueloil = np.array(df_in["other_mining_emission_fact_fueloil"])
    other_mining_plant_factor_sst = np.array(df_in["other_mining_plant_factor_sst"])
    other_mining_activity_motor = np.array(df_in["other_mining_activity_motor"])
    other_mining_activity_other = np.array(df_in["other_mining_activity_other"])
    other_mining_activity_heat = np.array(df_in["other_mining_activity_heat"])

    # calculate useful total demand

    other_mining_useful_energy = other_mining_production * other_mining_intensity

    # calculate demand in Tcal by en use
    other_mining_dem_motor_diesel = other_mining_useful_energy * other_mining_share_motor * other_mining_motor_diesel / other_mining_efficiency_motor_diesel
    other_mining_dem_motor_pliqgas = other_mining_useful_energy * other_mining_share_motor * other_mining_motor_pliqgas / other_mining_efficiency_motor_pliqgas
    other_mining_dem_motor_electric = other_mining_useful_energy * other_mining_share_motor * other_mining_motor_electric / other_mining_efficiency_motor_electric
    other_mining_dem_motor_hydrogen = other_mining_useful_energy * other_mining_share_motor * other_mining_motor_hydrogen / other_mining_efficiency_motor_hydrogen

    other_mining_dem_other_electric = other_mining_useful_energy * other_mining_share_other * other_mining_other_electric / other_mining_efficiency_other_electric

    other_mining_dem_heat_coal = other_mining_useful_energy * other_mining_share_heat * other_mining_heat_coal / other_mining_efficiency_heat_coal
    other_mining_dem_heat_electric = other_mining_useful_energy * other_mining_share_heat * other_mining_heat_electric / other_mining_efficiency_heat_electric
    other_mining_dem_heat_solar = other_mining_useful_energy * other_mining_share_heat * other_mining_heat_solar / other_mining_efficiency_heat_solar
    other_mining_dem_heat_pliqgas = other_mining_useful_energy * other_mining_share_heat * other_mining_heat_pliqgas / other_mining_efficiency_heat_pliqgas
    other_mining_dem_heat_natural_gas = other_mining_useful_energy * other_mining_share_heat * other_mining_heat_natural_gas / other_mining_efficiency_heat_natural_gas
    other_mining_dem_heat_biomass = other_mining_useful_energy * other_mining_share_heat * other_mining_heat_biomass / other_mining_efficiency_heat_biomass
    other_mining_dem_heat_diesel = other_mining_useful_energy * other_mining_share_heat * other_mining_heat_diesel / other_mining_efficiency_heat_diesel
    other_mining_dem_heat_fuel_oil = other_mining_useful_energy * other_mining_share_heat * other_mining_heat_fuel_oil / other_mining_efficiency_heat_fuel_oil
    other_mining_dem_heat_hydrogen = other_mining_useful_energy * other_mining_share_heat * other_mining_heat_hydrogen / other_mining_efficiency_heat_hydrogen

    # total demand by type of energy

    other_mining_dem_diesel = other_mining_dem_motor_diesel + other_mining_dem_heat_diesel
    other_mining_dem_natural_gas = other_mining_dem_heat_natural_gas
    other_mining_dem_electric = other_mining_dem_motor_electric + other_mining_dem_other_electric + other_mining_dem_heat_electric
    other_mining_dem_coal = other_mining_dem_heat_coal
    other_mining_dem_biomass = other_mining_dem_heat_biomass
    other_mining_dem_solar = other_mining_dem_heat_solar
    other_mining_dem_hydrogen = other_mining_dem_motor_hydrogen + other_mining_dem_heat_hydrogen
    other_mining_dem_pliqgas = other_mining_dem_motor_pliqgas + other_mining_dem_heat_pliqgas
    other_mining_dem_fueloil = other_mining_dem_heat_fuel_oil

    # calculate demand in Tcal by en use
    other_mining_emission_diesel = other_mining_dem_diesel * other_mining_emission_fact_diesel * fact / (10 ** 9)
    other_mining_emission_natural_gas = other_mining_dem_natural_gas * other_mining_emission_fact_natural_gas * fact / (10 ** 9)
    other_mining_emission_coal = other_mining_dem_coal * other_mining_emission_fact_coal * fact / (10 ** 9)
    other_mining_emission_pliqgas = other_mining_dem_pliqgas * other_mining_emission_fact_pliqgas * fact / (10 ** 9)
    other_mining_emission_fueloil = other_mining_dem_fueloil * other_mining_emission_fact_fueloil * fact / (10 ** 9)
    other_mining_emission = other_mining_emission_diesel + other_mining_emission_natural_gas + other_mining_emission_coal + other_mining_emission_pliqgas + other_mining_emission_fueloil

    # electric demand to produce hydrogen
    electric_demand_hydrogen = electric_demand_hydrogen + other_mining_dem_hydrogen / electrolyzer_efficiency * share_electric_grid_to_hydrogen

    #############################################################################
    ################# COST INFORMATION ##########################################

    # capacity

    other_mining_capacity_motor_diesel = other_mining_dem_motor_diesel * fact2 * (10 ** 3) / other_mining_activity_motor
    other_mining_capacity_motor_pliqgas = other_mining_dem_motor_pliqgas * fact2 * (10 ** 3) / other_mining_activity_motor
    other_mining_capacity_motor_electric = other_mining_dem_motor_electric * fact2 * (10 ** 3) / other_mining_activity_motor
    other_mining_capacity_motor_hydrogen = other_mining_dem_motor_hydrogen * fact2 * (10 ** 3) / other_mining_activity_motor
    other_mining_capacity_heat_coal = other_mining_dem_heat_coal * fact2 * (10 ** 3) / other_mining_activity_heat
    other_mining_capacity_heat_electric = other_mining_dem_heat_electric * fact2 * (10 ** 3) / other_mining_activity_heat
    other_mining_capacity_heat_solar = other_mining_dem_heat_solar * fact2 * (10 ** 3) / (8760*other_mining_plant_factor_sst)
    other_mining_capacity_heat_pliqgas = other_mining_dem_heat_pliqgas * fact2 * (10 ** 3) / other_mining_activity_heat
    other_mining_capacity_heat_natural_gas = other_mining_dem_heat_natural_gas * fact2 * (10 ** 3) / other_mining_activity_heat
    other_mining_capacity_heat_biomass = other_mining_dem_heat_biomass * fact2 * (10 ** 3) / other_mining_activity_heat
    other_mining_capacity_heat_diesel = other_mining_dem_heat_diesel * fact2 * (10 ** 3) / other_mining_activity_heat
    other_mining_capacity_heat_fuel_oil = other_mining_dem_heat_fuel_oil * fact2 * (10 ** 3) / other_mining_activity_heat
    other_mining_capacity_heat_hydrogen = other_mining_dem_heat_hydrogen * fact2 * (10 ** 3) / other_mining_activity_heat

    other_mining_capacity_motor_diesel = model_capacity(year, other_mining_capacity_motor_diesel)
    other_mining_capacity_motor_pliqgas = model_capacity(year, other_mining_capacity_motor_pliqgas)
    other_mining_capacity_motor_electric = model_capacity(year, other_mining_capacity_motor_electric)
    other_mining_capacity_motor_hydrogen = model_capacity(year, other_mining_capacity_motor_hydrogen)
    other_mining_capacity_heat_coal = model_capacity(year, other_mining_capacity_heat_coal)
    other_mining_capacity_heat_electric = model_capacity(year, other_mining_capacity_heat_electric)
    other_mining_capacity_heat_solar = model_capacity(year, other_mining_capacity_heat_solar)
    other_mining_capacity_heat_pliqgas = model_capacity(year, other_mining_capacity_heat_pliqgas)
    other_mining_capacity_heat_natural_gas = model_capacity(year, other_mining_capacity_heat_natural_gas)
    other_mining_capacity_heat_biomass = model_capacity(year, other_mining_capacity_heat_biomass)
    other_mining_capacity_heat_diesel = model_capacity(year, other_mining_capacity_heat_diesel)
    other_mining_capacity_heat_fuel_oil = model_capacity(year, other_mining_capacity_heat_fuel_oil)
    other_mining_capacity_heat_hydrogen = model_capacity(year, other_mining_capacity_heat_hydrogen)

    other_mining_delta_capacity_motor_diesel = model_delta_capacity(year, other_mining_capacity_motor_diesel)
    other_mining_delta_capacity_motor_pliqgas = model_delta_capacity(year, other_mining_capacity_motor_pliqgas)
    other_mining_delta_capacity_motor_electric = model_delta_capacity(year, other_mining_capacity_motor_electric)
    other_mining_delta_capacity_motor_hydrogen = model_delta_capacity(year, other_mining_capacity_motor_hydrogen)
    other_mining_delta_capacity_heat_coal = model_delta_capacity(year, other_mining_capacity_heat_coal)
    other_mining_delta_capacity_heat_electric = model_delta_capacity(year, other_mining_capacity_heat_electric)
    other_mining_delta_capacity_heat_solar = model_delta_capacity(year, other_mining_capacity_heat_solar)
    other_mining_delta_capacity_heat_pliqgas = model_delta_capacity(year, other_mining_capacity_heat_pliqgas)
    other_mining_delta_capacity_heat_natural_gas = model_delta_capacity(year, other_mining_capacity_heat_natural_gas)
    other_mining_delta_capacity_heat_biomass = model_delta_capacity(year, other_mining_capacity_heat_biomass)
    other_mining_delta_capacity_heat_diesel = model_delta_capacity(year, other_mining_capacity_heat_diesel)
    other_mining_delta_capacity_heat_fuel_oil = model_delta_capacity(year, other_mining_capacity_heat_fuel_oil)
    other_mining_delta_capacity_heat_hydrogen = model_delta_capacity(year, other_mining_capacity_heat_hydrogen)

    # OPEX
    other_mining_OPEX_diesel = other_mining_dem_diesel * industry_and_mining_fuel_price_diesel / (10 ** 6)
    other_mining_OPEX_natural_gas = other_mining_dem_natural_gas * industry_and_mining_fuel_price_natural_gas / (10 ** 6)
    other_mining_OPEX_electric = other_mining_dem_electric * industry_and_mining_fuel_price_electric / (10 ** 6)
    other_mining_OPEX_coal = other_mining_dem_coal * industry_and_mining_fuel_price_coal / (10 ** 6)
    other_mining_OPEX_biomass = other_mining_dem_biomass * industry_and_mining_fuel_price_biomass / (10 ** 6)
    other_mining_OPEX_solar = other_mining_dem_solar * industry_and_mining_fuel_price_solar / (10 ** 6)
    other_mining_OPEX_hydrogen = other_mining_dem_hydrogen * industry_and_mining_fuel_price_hydrogen / (10 ** 6)
    other_mining_OPEX_pliqgas = other_mining_dem_pliqgas * industry_and_mining_fuel_price_pliqgas / (10 ** 6)
    other_mining_OPEX_fuel_oil = other_mining_dem_fueloil * industry_and_mining_fuel_price_fuel_oil / (10 ** 6)
    other_mining_OPEX = other_mining_OPEX_diesel + other_mining_OPEX_natural_gas + other_mining_OPEX_electric + other_mining_OPEX_coal + other_mining_OPEX_biomass + other_mining_OPEX_solar + other_mining_OPEX_hydrogen + other_mining_OPEX_pliqgas + other_mining_OPEX_fuel_oil

    # CAPEX
    other_mining_CAPEX_motor_diesel = other_mining_delta_capacity_motor_diesel * industry_and_mining_investment_cost_motor_diesel / (10 ** 3)
    other_mining_CAPEX_motor_pliqgas = other_mining_delta_capacity_motor_pliqgas * industry_and_mining_investment_cost_motor_pliqgas / (10 ** 3)
    other_mining_CAPEX_motor_electric = other_mining_delta_capacity_motor_electric * industry_and_mining_investment_cost_motor_electric / (10 ** 3)
    other_mining_CAPEX_motor_hydrogen = other_mining_delta_capacity_motor_hydrogen * industry_and_mining_investment_cost_motor_hydrogen / (10 ** 3)
    other_mining_CAPEX_motor = other_mining_CAPEX_motor_diesel + other_mining_CAPEX_motor_pliqgas + other_mining_CAPEX_motor_electric + other_mining_CAPEX_motor_hydrogen

    other_mining_CAPEX_heat_coal = other_mining_delta_capacity_heat_coal * industry_and_mining_investment_cost_heat_coal / (10 ** 3)
    other_mining_CAPEX_heat_electric = other_mining_delta_capacity_heat_electric * industry_and_mining_investment_cost_heat_electric / (10 ** 3)
    other_mining_CAPEX_heat_solar = other_mining_delta_capacity_heat_solar * industry_and_mining_investment_cost_heat_solar / (10 ** 3)
    other_mining_CAPEX_heat_pliqgas = other_mining_delta_capacity_heat_pliqgas * industry_and_mining_investment_cost_heat_pliqgas / (10 ** 3)
    other_mining_CAPEX_heat_natural_gas = other_mining_delta_capacity_heat_natural_gas * industry_and_mining_investment_cost_heat_natural_gas / (10 ** 3)
    other_mining_CAPEX_heat_biomass = other_mining_delta_capacity_heat_biomass * industry_and_mining_investment_cost_heat_biomass / (10 ** 3)
    other_mining_CAPEX_heat_diesel = other_mining_delta_capacity_heat_diesel * industry_and_mining_investment_cost_heat_diesel / (10 ** 3)
    other_mining_CAPEX_heat_fuel_oil = other_mining_delta_capacity_heat_fuel_oil * industry_and_mining_investment_cost_heat_fuel_oil / (10 ** 3)
    other_mining_CAPEX_heat_hydrogen = other_mining_delta_capacity_heat_hydrogen * industry_and_mining_investment_cost_heat_hydrogen / (10 ** 3)
    other_mining_CAPEX_heat = other_mining_CAPEX_heat_coal + other_mining_CAPEX_heat_electric + other_mining_CAPEX_heat_solar + other_mining_CAPEX_heat_pliqgas + other_mining_CAPEX_heat_natural_gas + other_mining_CAPEX_heat_biomass + other_mining_CAPEX_heat_diesel + other_mining_CAPEX_heat_fuel_oil + other_mining_CAPEX_heat_hydrogen

    # total CAPEX
    other_mining_CAPEX = other_mining_CAPEX_motor + other_mining_CAPEX_heat

    # update
    dict_emission.update({"other_mining": other_mining_emission})
    dict_electric_demand.update({"other_mining": other_mining_dem_electric * fact2})
    # CAPEX, OPEX
    dict_CAPEX.update({"other_mining": other_mining_CAPEX})
    dict_OPEX.update({"other_mining": other_mining_OPEX})

    ####################################################################################################################

    # SUB SECTOR: Steel-Siderurgia- Industria del Acero

    steel_production = np.array(df_in["steel_production"])
    steel_intensity = np.array(df_in["steel_intensity"])
    steel_intensity_reference = np.array(df_in["steel_intensity_reference"])
    steel_share_motor = np.array(df_in["steel_share_motor"])
    steel_share_other = np.array(df_in["steel_share_other"])
    steel_share_heat = np.array(df_in["steel_share_heat"])
    steel_motor_diesel = np.array(df_in["steel_motor_diesel"])
    steel_motor_pliqgas = np.array(df_in["steel_motor_pliqgas"])
    steel_motor_electric = np.array(df_in["steel_motor_electric"])
    steel_motor_hydrogen = np.array(df_in["steel_motor_hydrogen"])
    steel_other_electric = np.array(df_in["steel_other_electric"])
    steel_heat_coal = np.array(df_in["steel_heat_coal"])
    steel_heat_coke = np.array(df_in["steel_heat_coke"])
    steel_heat_electric = np.array(df_in["steel_heat_electric"])
    steel_heat_solar = np.array(df_in["steel_heat_solar"])
    steel_heat_pliqgas = np.array(df_in["steel_heat_pliqgas"])
    steel_heat_natural_gas = np.array(df_in["steel_heat_natural_gas"])
    steel_heat_biomass = np.array(df_in["steel_heat_biomass"])
    steel_heat_diesel = np.array(df_in["steel_heat_diesel"])
    steel_heat_fuel_oil = np.array(df_in["steel_heat_fuel_oil"])
    steel_heat_hydrogen = np.array(df_in["steel_heat_hydrogen"])
    steel_efficiency_motor_diesel = np.array(df_in["steel_efficiency_motor_diesel"])
    steel_efficiency_motor_pliqgas = np.array(df_in["steel_efficiency_motor_pliqgas"])
    steel_efficiency_motor_electric = np.array(df_in["steel_efficiency_motor_electric"])
    steel_efficiency_motor_hydrogen = np.array(df_in["steel_efficiency_motor_hydrogen"])
    steel_efficiency_other_electric = np.array(df_in["steel_efficiency_other_electric"])
    steel_efficiency_heat_coal = np.array(df_in["steel_efficiency_heat_coal"])
    steel_efficiency_heat_coke = np.array(df_in["steel_efficiency_heat_coke"])
    steel_efficiency_heat_electric = np.array(df_in["steel_efficiency_heat_electric"])
    steel_efficiency_heat_solar = np.array(df_in["steel_efficiency_heat_solar"])
    steel_efficiency_heat_pliqgas = np.array(df_in["steel_efficiency_heat_pliqgas"])
    steel_efficiency_heat_natural_gas = np.array(df_in["steel_efficiency_heat_natural_gas"])
    steel_efficiency_heat_biomass = np.array(df_in["steel_efficiency_heat_biomass"])
    steel_efficiency_heat_diesel = np.array(df_in["steel_efficiency_heat_diesel"])
    steel_efficiency_heat_fuel_oil = np.array(df_in["steel_efficiency_heat_fuel_oil"])
    steel_efficiency_heat_hydrogen = np.array(df_in["steel_efficiency_heat_hydrogen"])
    steel_emission_fact_diesel = np.array(df_in["steel_emission_fact_diesel"])
    steel_emission_fact_natural_gas = np.array(df_in["steel_emission_fact_natural_gas"])
    steel_emission_fact_coal = np.array(df_in["steel_emission_fact_coal"])
    steel_emission_fact_coke = np.array(df_in["steel_emission_fact_coke"])
    steel_emission_fact_pliqgas = np.array(df_in["steel_emission_fact_pliqgas"])
    steel_emission_fact_fueloil = np.array(df_in["steel_emission_fact_fueloil"])
    steel_plant_factor_sst = np.array(df_in["steel_plant_factor_sst"])
    steel_activity_motor = np.array(df_in["steel_activity_motor"])
    steel_activity_other = np.array(df_in["steel_activity_other"])
    steel_activity_heat = np.array(df_in["steel_activity_heat"])
    steel_investment_efficiency_improvement = np.array(df_in["steel_investment_efficiency_improvement"])

    # calculate useful total demand

    steel_useful_energy = steel_production * steel_intensity

    # calculate demand in Tcal by en use
    steel_dem_motor_diesel = steel_useful_energy * steel_share_motor * steel_motor_diesel / steel_efficiency_motor_diesel
    steel_dem_motor_pliqgas = steel_useful_energy * steel_share_motor * steel_motor_pliqgas / steel_efficiency_motor_pliqgas
    steel_dem_motor_electric = steel_useful_energy * steel_share_motor * steel_motor_electric / steel_efficiency_motor_electric
    steel_dem_motor_hydrogen = steel_useful_energy * steel_share_motor * steel_motor_hydrogen / steel_efficiency_motor_hydrogen

    steel_dem_other_electric = steel_useful_energy * steel_share_other * steel_other_electric / steel_efficiency_other_electric

    steel_dem_heat_coal = steel_useful_energy * steel_share_heat * steel_heat_coal / steel_efficiency_heat_coal
    steel_dem_heat_coke = steel_useful_energy * steel_share_heat * steel_heat_coke / steel_efficiency_heat_coke
    steel_dem_heat_electric = steel_useful_energy * steel_share_heat * steel_heat_electric / steel_efficiency_heat_electric
    steel_dem_heat_solar = steel_useful_energy * steel_share_heat * steel_heat_solar / steel_efficiency_heat_solar
    steel_dem_heat_pliqgas = steel_useful_energy * steel_share_heat * steel_heat_pliqgas / steel_efficiency_heat_pliqgas
    steel_dem_heat_natural_gas = steel_useful_energy * steel_share_heat * steel_heat_natural_gas / steel_efficiency_heat_natural_gas
    steel_dem_heat_biomass = steel_useful_energy * steel_share_heat * steel_heat_biomass / steel_efficiency_heat_biomass
    steel_dem_heat_diesel = steel_useful_energy * steel_share_heat * steel_heat_diesel / steel_efficiency_heat_diesel
    steel_dem_heat_fuel_oil = steel_useful_energy * steel_share_heat * steel_heat_fuel_oil / steel_efficiency_heat_fuel_oil
    steel_dem_heat_hydrogen = steel_useful_energy * steel_share_heat * steel_heat_hydrogen / steel_efficiency_heat_hydrogen

    # total demand by type of energy

    steel_dem_diesel = steel_dem_motor_diesel + steel_dem_heat_diesel
    steel_dem_natural_gas = steel_dem_heat_natural_gas
    steel_dem_electric = steel_dem_motor_electric + steel_dem_other_electric + steel_dem_heat_electric
    steel_dem_coal = steel_dem_heat_coal
    steel_dem_coke = steel_dem_heat_coke
    steel_dem_biomass = steel_dem_heat_biomass
    steel_dem_solar = steel_dem_heat_solar
    steel_dem_hydrogen = steel_dem_motor_hydrogen + steel_dem_heat_hydrogen
    steel_dem_pliqgas = steel_dem_motor_pliqgas + steel_dem_heat_pliqgas
    steel_dem_fueloil = steel_dem_heat_fuel_oil

    # calculate demand in Tcal by en use
    steel_emission_diesel = steel_dem_diesel * steel_emission_fact_diesel * fact / (10 ** 9)
    steel_emission_natural_gas = steel_dem_natural_gas * steel_emission_fact_natural_gas * fact / (10 ** 9)
    steel_emission_coal = steel_dem_coal * steel_emission_fact_coal * fact / (10 ** 9)
    steel_emission_coke = steel_dem_coke * steel_emission_fact_coke * fact / (10 ** 9)
    steel_emission_pliqgas = steel_dem_pliqgas * steel_emission_fact_pliqgas * fact / (10 ** 9)
    steel_emission_fueloil = steel_dem_fueloil * steel_emission_fact_fueloil * fact / (10 ** 9)
    steel_emission = steel_emission_diesel + steel_emission_natural_gas + steel_emission_coal + steel_emission_coke+ steel_emission_pliqgas + steel_emission_fueloil

    # electric demand to produce hydrogen
    electric_demand_hydrogen = electric_demand_hydrogen + steel_dem_hydrogen / electrolyzer_efficiency * share_electric_grid_to_hydrogen

    #############################################################################
    ################# COST INFORMATION ##########################################

    # capacity

    steel_capacity_motor_diesel = steel_dem_motor_diesel * fact2 * (10 ** 3) / steel_activity_motor
    steel_capacity_motor_pliqgas = steel_dem_motor_pliqgas * fact2 * (10 ** 3) / steel_activity_motor
    steel_capacity_motor_electric = steel_dem_motor_electric * fact2 * (10 ** 3) / steel_activity_motor
    steel_capacity_motor_hydrogen = steel_dem_motor_hydrogen * fact2 * (10 ** 3) / steel_activity_motor
    steel_capacity_heat_coal = steel_dem_heat_coal * fact2 * (10 ** 3) / steel_activity_heat
    steel_capacity_heat_coke = steel_dem_heat_coke * fact2 * (10 ** 3) / steel_activity_heat
    steel_capacity_heat_electric = steel_dem_heat_electric * fact2 * (10 ** 3) / steel_activity_heat
    steel_capacity_heat_solar = steel_dem_heat_solar * fact2 * (10 ** 3) / (8760*other_industries_plant_factor_sst)
    steel_capacity_heat_pliqgas = steel_dem_heat_pliqgas * fact2 * (10 ** 3) / steel_activity_heat
    steel_capacity_heat_natural_gas = steel_dem_heat_natural_gas * fact2 * (10 ** 3) / steel_activity_heat
    steel_capacity_heat_biomass = steel_dem_heat_biomass * fact2 * (10 ** 3) / steel_activity_heat
    steel_capacity_heat_diesel = steel_dem_heat_diesel * fact2 * (10 ** 3) / steel_activity_heat
    steel_capacity_heat_fuel_oil = steel_dem_heat_fuel_oil * fact2 * (10 ** 3) / steel_activity_heat
    steel_capacity_heat_hydrogen = steel_dem_heat_hydrogen * fact2 * (10 ** 3) / steel_activity_heat

    steel_capacity_motor_diesel = model_capacity(year, steel_capacity_motor_diesel)
    steel_capacity_motor_pliqgas = model_capacity(year, steel_capacity_motor_pliqgas)
    steel_capacity_motor_electric = model_capacity(year, steel_capacity_motor_electric)
    steel_capacity_motor_hydrogen = model_capacity(year, steel_capacity_motor_hydrogen)
    steel_capacity_heat_coal = model_capacity(year, steel_capacity_heat_coal)
    steel_capacity_heat_coke = model_capacity(year, steel_capacity_heat_coke)
    steel_capacity_heat_electric = model_capacity(year, steel_capacity_heat_electric)
    steel_capacity_heat_solar = model_capacity(year, steel_capacity_heat_solar)
    steel_capacity_heat_pliqgas = model_capacity(year, steel_capacity_heat_pliqgas)
    steel_capacity_heat_natural_gas = model_capacity(year, steel_capacity_heat_natural_gas)
    steel_capacity_heat_biomass = model_capacity(year, steel_capacity_heat_biomass)
    steel_capacity_heat_diesel = model_capacity(year, steel_capacity_heat_diesel)
    steel_capacity_heat_fuel_oil = model_capacity(year, steel_capacity_heat_fuel_oil)
    steel_capacity_heat_hydrogen = model_capacity(year, steel_capacity_heat_hydrogen)

    steel_delta_capacity_motor_diesel = model_delta_capacity(year, steel_capacity_motor_diesel)
    steel_delta_capacity_motor_pliqgas = model_delta_capacity(year, steel_capacity_motor_pliqgas)
    steel_delta_capacity_motor_electric = model_delta_capacity(year, steel_capacity_motor_electric)
    steel_delta_capacity_motor_hydrogen = model_delta_capacity(year, steel_capacity_motor_hydrogen)
    steel_delta_capacity_heat_coal = model_delta_capacity(year, steel_capacity_heat_coal)
    steel_delta_capacity_heat_coke = model_delta_capacity(year, steel_capacity_heat_coke)
    steel_delta_capacity_heat_electric = model_delta_capacity(year, steel_capacity_heat_electric)
    steel_delta_capacity_heat_solar = model_delta_capacity(year, steel_capacity_heat_solar)
    steel_delta_capacity_heat_pliqgas = model_delta_capacity(year, steel_capacity_heat_pliqgas)
    steel_delta_capacity_heat_natural_gas = model_delta_capacity(year, steel_capacity_heat_natural_gas)
    steel_delta_capacity_heat_biomass = model_delta_capacity(year, steel_capacity_heat_biomass)
    steel_delta_capacity_heat_diesel = model_delta_capacity(year, steel_capacity_heat_diesel)
    steel_delta_capacity_heat_fuel_oil = model_delta_capacity(year, steel_capacity_heat_fuel_oil)
    steel_delta_capacity_heat_hydrogen = model_delta_capacity(year, steel_capacity_heat_hydrogen)

    # OPEX
    steel_OPEX_diesel = steel_dem_diesel * industry_and_mining_fuel_price_diesel / (10 ** 6)
    steel_OPEX_natural_gas = steel_dem_natural_gas * industry_and_mining_fuel_price_natural_gas / (10 ** 6)
    steel_OPEX_electric = steel_dem_electric * industry_and_mining_fuel_price_electric / (10 ** 6)
    steel_OPEX_coal = steel_dem_coal * industry_and_mining_fuel_price_coal / (10 ** 6)
    steel_OPEX_coke = steel_dem_coke * industry_and_mining_fuel_price_coke / (10 ** 6)
    steel_OPEX_biomass = steel_dem_biomass * industry_and_mining_fuel_price_biomass / (10 ** 6)
    steel_OPEX_solar = steel_dem_solar * industry_and_mining_fuel_price_solar / (10 ** 6)
    steel_OPEX_hydrogen = steel_dem_hydrogen * industry_and_mining_fuel_price_hydrogen / (10 ** 6)
    steel_OPEX_pliqgas = steel_dem_pliqgas * industry_and_mining_fuel_price_pliqgas / (10 ** 6)
    steel_OPEX_fuel_oil = steel_dem_fueloil * industry_and_mining_fuel_price_fuel_oil / (10 ** 6)
    steel_OPEX = steel_OPEX_diesel + steel_OPEX_natural_gas + steel_OPEX_electric + steel_OPEX_coal + steel_OPEX_coke + steel_OPEX_biomass + steel_OPEX_solar + steel_OPEX_hydrogen + steel_OPEX_pliqgas + steel_OPEX_fuel_oil

    # CAPEX
    steel_CAPEX_motor_diesel = steel_delta_capacity_motor_diesel * industry_and_mining_investment_cost_motor_diesel / (10 ** 3)
    steel_CAPEX_motor_pliqgas = steel_delta_capacity_motor_pliqgas * industry_and_mining_investment_cost_motor_pliqgas / (10 ** 3)
    steel_CAPEX_motor_electric = steel_delta_capacity_motor_electric * industry_and_mining_investment_cost_motor_electric / (10 ** 3)
    steel_CAPEX_motor_hydrogen = steel_delta_capacity_motor_hydrogen * industry_and_mining_investment_cost_motor_hydrogen / (10 ** 3)
    steel_CAPEX_motor = steel_CAPEX_motor_diesel + steel_CAPEX_motor_pliqgas + steel_CAPEX_motor_electric + steel_CAPEX_motor_hydrogen

    steel_CAPEX_heat_coal = steel_delta_capacity_heat_coal * industry_and_mining_investment_cost_heat_coal / (10 ** 3)
    steel_CAPEX_heat_coke = steel_delta_capacity_heat_coke * industry_and_mining_investment_cost_heat_coke / (10 ** 3)
    steel_CAPEX_heat_electric = steel_delta_capacity_heat_electric * industry_and_mining_investment_cost_heat_electric / (10 ** 3)
    steel_CAPEX_heat_solar = steel_delta_capacity_heat_solar * industry_and_mining_investment_cost_heat_solar / (10 ** 3)
    steel_CAPEX_heat_pliqgas = steel_delta_capacity_heat_pliqgas * industry_and_mining_investment_cost_heat_pliqgas / (10 ** 3)
    steel_CAPEX_heat_natural_gas = steel_delta_capacity_heat_natural_gas * industry_and_mining_investment_cost_heat_natural_gas / (10 ** 3)
    steel_CAPEX_heat_biomass = steel_delta_capacity_heat_biomass * industry_and_mining_investment_cost_heat_biomass / (10 ** 3)
    steel_CAPEX_heat_diesel = steel_delta_capacity_heat_diesel * industry_and_mining_investment_cost_heat_diesel / (10 ** 3)
    steel_CAPEX_heat_fuel_oil = steel_delta_capacity_heat_fuel_oil * industry_and_mining_investment_cost_heat_fuel_oil / (10 ** 3)
    steel_CAPEX_heat_hydrogen = steel_delta_capacity_heat_hydrogen * industry_and_mining_investment_cost_heat_hydrogen / (10 ** 3)
    steel_CAPEX_heat = steel_CAPEX_heat_coal + steel_CAPEX_heat_coke+steel_CAPEX_heat_electric + steel_CAPEX_heat_solar + steel_CAPEX_heat_pliqgas + steel_CAPEX_heat_natural_gas + steel_CAPEX_heat_biomass + steel_CAPEX_heat_diesel + steel_CAPEX_heat_fuel_oil + steel_CAPEX_heat_hydrogen

    #CAPEX efficiency improvement
    steel_CAPEX_efficiency_improvement = steel_investment_efficiency_improvement * (steel_intensity_reference-steel_intensity) / (10 ** 6)

    # total CAPEX
    steel_CAPEX = steel_CAPEX_motor + steel_CAPEX_heat + steel_CAPEX_efficiency_improvement

    # update
    dict_emission.update({"steel": steel_emission})
    dict_electric_demand.update({"steel": steel_dem_electric * fact2})
    # CAPEX, OPEX
    dict_CAPEX.update({"steel": steel_CAPEX})
    dict_OPEX.update({"steel": steel_OPEX})

    ####################################################################################################################

    # SUB SECTOR: iron- Industria del hierro

    iron_production = np.array(df_in["iron_production"])
    iron_intensity = np.array(df_in["iron_intensity"])
    iron_intensity_reference = np.array(df_in["iron_intensity_reference"])
    iron_share_motor = np.array(df_in["iron_share_motor"])
    iron_share_other = np.array(df_in["iron_share_other"])
    iron_share_heat = np.array(df_in["iron_share_heat"])
    iron_motor_diesel = np.array(df_in["iron_motor_diesel"])
    iron_motor_pliqgas = np.array(df_in["iron_motor_pliqgas"])
    iron_motor_electric = np.array(df_in["iron_motor_electric"])
    iron_motor_hydrogen = np.array(df_in["iron_motor_hydrogen"])
    iron_other_electric = np.array(df_in["iron_other_electric"])
    iron_heat_coal = np.array(df_in["iron_heat_coal"])
    iron_heat_coke = np.array(df_in["iron_heat_coke"])
    iron_heat_electric = np.array(df_in["iron_heat_electric"])
    iron_heat_solar = np.array(df_in["iron_heat_solar"])
    iron_heat_pliqgas = np.array(df_in["iron_heat_pliqgas"])
    iron_heat_natural_gas = np.array(df_in["iron_heat_natural_gas"])
    iron_heat_biomass = np.array(df_in["iron_heat_biomass"])
    iron_heat_diesel = np.array(df_in["iron_heat_diesel"])
    iron_heat_fuel_oil = np.array(df_in["iron_heat_fuel_oil"])
    iron_heat_hydrogen = np.array(df_in["iron_heat_hydrogen"])
    iron_efficiency_motor_diesel = np.array(df_in["iron_efficiency_motor_diesel"])
    iron_efficiency_motor_pliqgas = np.array(df_in["iron_efficiency_motor_pliqgas"])
    iron_efficiency_motor_electric = np.array(df_in["iron_efficiency_motor_electric"])
    iron_efficiency_motor_hydrogen = np.array(df_in["iron_efficiency_motor_hydrogen"])
    iron_efficiency_other_electric = np.array(df_in["iron_efficiency_other_electric"])
    iron_efficiency_heat_coal = np.array(df_in["iron_efficiency_heat_coal"])
    iron_efficiency_heat_coke = np.array(df_in["iron_efficiency_heat_coke"])
    iron_efficiency_heat_electric = np.array(df_in["iron_efficiency_heat_electric"])
    iron_efficiency_heat_solar = np.array(df_in["iron_efficiency_heat_solar"])
    iron_efficiency_heat_pliqgas = np.array(df_in["iron_efficiency_heat_pliqgas"])
    iron_efficiency_heat_natural_gas = np.array(df_in["iron_efficiency_heat_natural_gas"])
    iron_efficiency_heat_biomass = np.array(df_in["iron_efficiency_heat_biomass"])
    iron_efficiency_heat_diesel = np.array(df_in["iron_efficiency_heat_diesel"])
    iron_efficiency_heat_fuel_oil = np.array(df_in["iron_efficiency_heat_fuel_oil"])
    iron_efficiency_heat_hydrogen = np.array(df_in["iron_efficiency_heat_hydrogen"])
    iron_emission_fact_diesel = np.array(df_in["iron_emission_fact_diesel"])
    iron_emission_fact_natural_gas = np.array(df_in["iron_emission_fact_natural_gas"])
    iron_emission_fact_coal = np.array(df_in["iron_emission_fact_coal"])
    iron_emission_fact_coke = np.array(df_in["iron_emission_fact_coke"])
    iron_emission_fact_pliqgas = np.array(df_in["iron_emission_fact_pliqgas"])
    iron_emission_fact_fueloil = np.array(df_in["iron_emission_fact_fueloil"])
    iron_plant_factor_sst = np.array(df_in["iron_plant_factor_sst"])
    iron_activity_motor = np.array(df_in["iron_activity_motor"])
    iron_activity_other = np.array(df_in["iron_activity_other"])
    iron_activity_heat = np.array(df_in["iron_activity_heat"])
    iron_investment_efficiency_improvement = np.array(df_in["iron_investment_efficiency_improvement"])

    # calculate useful total demand

    iron_useful_energy = iron_production * iron_intensity

    # calculate demand in Tcal by en use
    iron_dem_motor_diesel = iron_useful_energy * iron_share_motor * iron_motor_diesel / iron_efficiency_motor_diesel
    iron_dem_motor_pliqgas = iron_useful_energy * iron_share_motor * iron_motor_pliqgas / iron_efficiency_motor_pliqgas
    iron_dem_motor_electric = iron_useful_energy * iron_share_motor * iron_motor_electric / iron_efficiency_motor_electric
    iron_dem_motor_hydrogen = iron_useful_energy * iron_share_motor * iron_motor_hydrogen / iron_efficiency_motor_hydrogen

    iron_dem_other_electric = iron_useful_energy * iron_share_other * iron_other_electric / iron_efficiency_other_electric

    iron_dem_heat_coal = iron_useful_energy * iron_share_heat * iron_heat_coal / iron_efficiency_heat_coal
    iron_dem_heat_coke = iron_useful_energy * iron_share_heat * iron_heat_coke / iron_efficiency_heat_coke
    iron_dem_heat_electric = iron_useful_energy * iron_share_heat * iron_heat_electric / iron_efficiency_heat_electric
    iron_dem_heat_solar = iron_useful_energy * iron_share_heat * iron_heat_solar / iron_efficiency_heat_solar
    iron_dem_heat_pliqgas = iron_useful_energy * iron_share_heat * iron_heat_pliqgas / iron_efficiency_heat_pliqgas
    iron_dem_heat_natural_gas = iron_useful_energy * iron_share_heat * iron_heat_natural_gas / iron_efficiency_heat_natural_gas
    iron_dem_heat_biomass = iron_useful_energy * iron_share_heat * iron_heat_biomass / iron_efficiency_heat_biomass
    iron_dem_heat_diesel = iron_useful_energy * iron_share_heat * iron_heat_diesel / iron_efficiency_heat_diesel
    iron_dem_heat_fuel_oil = iron_useful_energy * iron_share_heat * iron_heat_fuel_oil / iron_efficiency_heat_fuel_oil
    iron_dem_heat_hydrogen = iron_useful_energy * iron_share_heat * iron_heat_hydrogen / iron_efficiency_heat_hydrogen

    # total demand by type of energy

    iron_dem_diesel = iron_dem_motor_diesel + iron_dem_heat_diesel
    iron_dem_natural_gas = iron_dem_heat_natural_gas
    iron_dem_electric = iron_dem_motor_electric + iron_dem_other_electric + iron_dem_heat_electric
    iron_dem_coal = iron_dem_heat_coal
    iron_dem_coke = iron_dem_heat_coke
    iron_dem_biomass = iron_dem_heat_biomass
    iron_dem_solar = iron_dem_heat_solar
    iron_dem_hydrogen = iron_dem_motor_hydrogen + iron_dem_heat_hydrogen
    iron_dem_pliqgas = iron_dem_motor_pliqgas + iron_dem_heat_pliqgas
    iron_dem_fueloil = iron_dem_heat_fuel_oil

    # calculate demand in Tcal by en use
    iron_emission_diesel = iron_dem_diesel * iron_emission_fact_diesel * fact / (10 ** 9)
    iron_emission_natural_gas = iron_dem_natural_gas * iron_emission_fact_natural_gas * fact / (10 ** 9)
    iron_emission_coal = iron_dem_coal * iron_emission_fact_coal * fact / (10 ** 9)
    iron_emission_coke = iron_dem_coke * iron_emission_fact_coke * fact / (10 ** 9)
    iron_emission_pliqgas = iron_dem_pliqgas * iron_emission_fact_pliqgas * fact / (10 ** 9)
    iron_emission_fueloil = iron_dem_fueloil * iron_emission_fact_fueloil * fact / (10 ** 9)
    iron_emission = iron_emission_diesel + iron_emission_natural_gas + iron_emission_coal + iron_emission_coke + iron_emission_pliqgas + iron_emission_fueloil

    # electric demand to produce hydrogen
    electric_demand_hydrogen = electric_demand_hydrogen + iron_dem_hydrogen / electrolyzer_efficiency * share_electric_grid_to_hydrogen

    ################# COST INFORMATION ##########################################

    # capacity

    iron_capacity_motor_diesel = iron_dem_motor_diesel * fact2 * (10 ** 3) / iron_activity_motor
    iron_capacity_motor_pliqgas = iron_dem_motor_pliqgas * fact2 * (10 ** 3) / iron_activity_motor
    iron_capacity_motor_electric = iron_dem_motor_electric * fact2 * (10 ** 3) / iron_activity_motor
    iron_capacity_motor_hydrogen = iron_dem_motor_hydrogen * fact2 * (10 ** 3) / iron_activity_motor
    iron_capacity_heat_coal = iron_dem_heat_coal * fact2 * (10 ** 3) / iron_activity_heat
    iron_capacity_heat_coke = iron_dem_heat_coke * fact2 * (10 ** 3) / iron_activity_heat
    iron_capacity_heat_electric = iron_dem_heat_electric * fact2 * (10 ** 3) / iron_activity_heat
    iron_capacity_heat_solar = iron_dem_heat_solar * fact2 * (10 ** 3) / (8760*other_industries_plant_factor_sst)
    iron_capacity_heat_pliqgas = iron_dem_heat_pliqgas * fact2 * (10 ** 3) / iron_activity_heat
    iron_capacity_heat_natural_gas = iron_dem_heat_natural_gas * fact2 * (10 ** 3) / iron_activity_heat
    iron_capacity_heat_biomass = iron_dem_heat_biomass * fact2 * (10 ** 3) / iron_activity_heat
    iron_capacity_heat_diesel = iron_dem_heat_diesel * fact2 * (10 ** 3) / iron_activity_heat
    iron_capacity_heat_fuel_oil = iron_dem_heat_fuel_oil * fact2 * (10 ** 3) / iron_activity_heat
    iron_capacity_heat_hydrogen = iron_dem_heat_hydrogen * fact2 * (10 ** 3) / iron_activity_heat

    iron_capacity_motor_diesel = model_capacity(year, iron_capacity_motor_diesel)
    iron_capacity_motor_pliqgas = model_capacity(year, iron_capacity_motor_pliqgas)
    iron_capacity_motor_electric = model_capacity(year, iron_capacity_motor_electric)
    iron_capacity_motor_hydrogen = model_capacity(year, iron_capacity_motor_hydrogen)
    iron_capacity_heat_coal = model_capacity(year, iron_capacity_heat_coal)
    iron_capacity_heat_coke = model_capacity(year, iron_capacity_heat_coke)
    iron_capacity_heat_electric = model_capacity(year, iron_capacity_heat_electric)
    iron_capacity_heat_solar = model_capacity(year, iron_capacity_heat_solar)
    iron_capacity_heat_pliqgas = model_capacity(year, iron_capacity_heat_pliqgas)
    iron_capacity_heat_natural_gas = model_capacity(year, iron_capacity_heat_natural_gas)
    iron_capacity_heat_biomass = model_capacity(year, iron_capacity_heat_biomass)
    iron_capacity_heat_diesel = model_capacity(year, iron_capacity_heat_diesel)
    iron_capacity_heat_fuel_oil = model_capacity(year, iron_capacity_heat_fuel_oil)
    iron_capacity_heat_hydrogen = model_capacity(year, iron_capacity_heat_hydrogen)

    iron_delta_capacity_motor_diesel = model_delta_capacity(year, iron_capacity_motor_diesel)
    iron_delta_capacity_motor_pliqgas = model_delta_capacity(year, iron_capacity_motor_pliqgas)
    iron_delta_capacity_motor_electric = model_delta_capacity(year, iron_capacity_motor_electric)
    iron_delta_capacity_motor_hydrogen = model_delta_capacity(year, iron_capacity_motor_hydrogen)
    iron_delta_capacity_heat_coal = model_delta_capacity(year, iron_capacity_heat_coal)
    iron_delta_capacity_heat_coke = model_delta_capacity(year, iron_capacity_heat_coke)
    iron_delta_capacity_heat_electric = model_delta_capacity(year, iron_capacity_heat_electric)
    iron_delta_capacity_heat_solar = model_delta_capacity(year, iron_capacity_heat_solar)
    iron_delta_capacity_heat_pliqgas = model_delta_capacity(year, iron_capacity_heat_pliqgas)
    iron_delta_capacity_heat_natural_gas = model_delta_capacity(year, iron_capacity_heat_natural_gas)
    iron_delta_capacity_heat_biomass = model_delta_capacity(year, iron_capacity_heat_biomass)
    iron_delta_capacity_heat_diesel = model_delta_capacity(year, iron_capacity_heat_diesel)
    iron_delta_capacity_heat_fuel_oil = model_delta_capacity(year, iron_capacity_heat_fuel_oil)
    iron_delta_capacity_heat_hydrogen = model_delta_capacity(year, iron_capacity_heat_hydrogen)

    # OPEX
    iron_OPEX_diesel = iron_dem_diesel * industry_and_mining_fuel_price_diesel / (10 ** 6)
    iron_OPEX_natural_gas = iron_dem_natural_gas * industry_and_mining_fuel_price_natural_gas / (10 ** 6)
    iron_OPEX_electric = iron_dem_electric * industry_and_mining_fuel_price_electric / (10 ** 6)
    iron_OPEX_coal = iron_dem_coal * industry_and_mining_fuel_price_coal / (10 ** 6)
    iron_OPEX_coke = iron_dem_coke * industry_and_mining_fuel_price_coke / (10 ** 6)
    iron_OPEX_biomass = iron_dem_biomass * industry_and_mining_fuel_price_biomass / (10 ** 6)
    iron_OPEX_solar = iron_dem_solar * industry_and_mining_fuel_price_solar / (10 ** 6)
    iron_OPEX_hydrogen = iron_dem_hydrogen * industry_and_mining_fuel_price_hydrogen / (10 ** 6)
    iron_OPEX_pliqgas = iron_dem_pliqgas * industry_and_mining_fuel_price_pliqgas / (10 ** 6)
    iron_OPEX_fuel_oil = iron_dem_fueloil * industry_and_mining_fuel_price_fuel_oil / (10 ** 6)
    iron_OPEX = iron_OPEX_diesel + iron_OPEX_natural_gas + iron_OPEX_electric + iron_OPEX_coal + iron_OPEX_coke + iron_OPEX_biomass + iron_OPEX_solar + iron_OPEX_hydrogen + iron_OPEX_pliqgas + iron_OPEX_fuel_oil

    # CAPEX
    iron_CAPEX_motor_diesel = iron_delta_capacity_motor_diesel * industry_and_mining_investment_cost_motor_diesel / (10 ** 3)
    iron_CAPEX_motor_pliqgas = iron_delta_capacity_motor_pliqgas * industry_and_mining_investment_cost_motor_pliqgas / (10 ** 3)
    iron_CAPEX_motor_electric = iron_delta_capacity_motor_electric * industry_and_mining_investment_cost_motor_electric / (10 ** 3)
    iron_CAPEX_motor_hydrogen = iron_delta_capacity_motor_hydrogen * industry_and_mining_investment_cost_motor_hydrogen / (10 ** 3)
    iron_CAPEX_motor = iron_CAPEX_motor_diesel + iron_CAPEX_motor_pliqgas + iron_CAPEX_motor_electric + iron_CAPEX_motor_hydrogen

    iron_CAPEX_heat_coal = iron_delta_capacity_heat_coal * industry_and_mining_investment_cost_heat_coal / (10 ** 3)
    iron_CAPEX_heat_coke = iron_delta_capacity_heat_coke * industry_and_mining_investment_cost_heat_coke / (10 ** 3)
    iron_CAPEX_heat_electric = iron_delta_capacity_heat_electric * industry_and_mining_investment_cost_heat_electric / (10 ** 3)
    iron_CAPEX_heat_solar = iron_delta_capacity_heat_solar * industry_and_mining_investment_cost_heat_solar / (10 ** 3)
    iron_CAPEX_heat_pliqgas = iron_delta_capacity_heat_pliqgas * industry_and_mining_investment_cost_heat_pliqgas / (10 ** 3)
    iron_CAPEX_heat_natural_gas = iron_delta_capacity_heat_natural_gas * industry_and_mining_investment_cost_heat_natural_gas / (10 ** 3)
    iron_CAPEX_heat_biomass = iron_delta_capacity_heat_biomass * industry_and_mining_investment_cost_heat_biomass / (10 ** 3)
    iron_CAPEX_heat_diesel = iron_delta_capacity_heat_diesel * industry_and_mining_investment_cost_heat_diesel / (10 ** 3)
    iron_CAPEX_heat_fuel_oil = iron_delta_capacity_heat_fuel_oil * industry_and_mining_investment_cost_heat_fuel_oil / (10 ** 3)
    iron_CAPEX_heat_hydrogen = iron_delta_capacity_heat_hydrogen * industry_and_mining_investment_cost_heat_hydrogen / (10 ** 3)
    iron_CAPEX_heat = iron_CAPEX_heat_coal + iron_CAPEX_heat_coke + iron_CAPEX_heat_electric + iron_CAPEX_heat_solar + iron_CAPEX_heat_pliqgas + iron_CAPEX_heat_natural_gas + iron_CAPEX_heat_biomass + iron_CAPEX_heat_diesel + iron_CAPEX_heat_fuel_oil + iron_CAPEX_heat_hydrogen

    # CAPEX efficiency improvement
    iron_CAPEX_efficiency_improvement = iron_investment_efficiency_improvement * (iron_intensity_reference - iron_intensity) / (10 ** 6)

    # total CAPEX
    iron_CAPEX = iron_CAPEX_motor + iron_CAPEX_heat + iron_CAPEX_efficiency_improvement

    # update
    dict_emission.update({"iron": iron_emission})
    dict_electric_demand.update({"iron": iron_dem_electric * fact2})
    # CAPEX, OPEX
    dict_CAPEX.update({"iron": iron_CAPEX})
    dict_OPEX.update({"iron": iron_OPEX})


    ####################################################################################################################

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

    ####################################################################################################################

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

    ####################################################################################################################

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

    ####################################################################################################################

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

    ####################################################################################################################

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

    # add OPEX to master output
    vec_total_OPEX = 0
    for k in dict_OPEX.keys():
        # new key conveys emissions
        k_new = (dict_sector_abv["industry_and_mining"]) + "-OPEX_" + str(k) + "-MMUSD"
        # add to output
        dict_out.update({k_new: dict_OPEX[k].copy()})
        # update total
        vec_total_OPEX = vec_total_OPEX + np.array(dict_OPEX[k])

    # add CAPEX to master output
    vec_total_CAPEX = 0
    for k in dict_CAPEX.keys():
        # new key conveys emissions
        k_new = (dict_sector_abv["industry_and_mining"]) + "-CAPEX_" + str(k) + "-MMUSD"
        # add to output
        dict_out.update({k_new: dict_CAPEX[k].copy()})
        # update total
        vec_total_CAPEX = vec_total_CAPEX + np.array(dict_CAPEX[k])

    # add totals
    dict_out.update({
        (dict_sector_abv["industry_and_mining"] + "-emissions_total-mtco2e"): vec_total_emissions,
        (dict_sector_abv["industry_and_mining"] + "-electricity_total_demand-gwh"): vec_total_demand_electricity,
        (dict_sector_abv["industry_and_mining"] + "-electricity_hydrogen-gwh"): electric_demand_hydrogen,
        (dict_sector_abv["industry_and_mining"] + "-OPEX-MMUSD"): vec_total_OPEX,
        (dict_sector_abv["industry_and_mining"] + "-CAPEX-MMUSD"): vec_total_CAPEX,
    })

    # return
    return dict_out  # dict_emission,dict_electric_demand
