# Transport energy model developed by Centro de Energia U. de Chile using RAND python framework
# version 1.0 december 2020

import os, os.path
import time
import pandas as pd
import numpy as np
from econometric_models import model_transport_gasoline_demand, model_transport_pkm_aviation, model_transport_pkm_saturacion, model_delta_capacity,  model_capacity

###################
#    TRANSPORT    #
###################

scen_transport_private = -1  # -1 conservador, 0 moderado, 1 optimista

def sm_transport(df_in, dict_sector_abv, odel_transport_pkm_aviation = None):

    # conversion factor Tcal to TJ
    fact = 4.184
    # conversion factor Tcal to GWh
    fact2 = 1.162952
    # density gasoline (ton/m3)
    den_gasoline = 0.730
    # density diesel (ton/m3)
    den_diesel = 0.840
    # calorific power (kCal/kg)
    pc_gasoline = 11200
    pc_diesel = 10900
    pc_hydrogen = 28681

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
    transport_fuel_price_diesel = fuel_price_diesel * fuel_price_diesel_conversion
    fuel_price_natural_gas = np.array(df_in["fuel_price_natural_gas"])
    transport_fuel_price_natural_gas = fuel_price_natural_gas * fuel_price_natural_gas_conversion
    fuel_price_coal = np.array(df_in["fuel_price_coal"])
    transport_fuel_price_coal = fuel_price_coal * fuel_price_coal_conversion

    fuel_price_gasoline =transport_fuel_price_diesel * ratio_fuel_price_diesel_gasoline
    fuel_price_fuel_oil = transport_fuel_price_diesel * ratio_fuel_price_diesel_fuel_oil
    fuel_price_kerosene = transport_fuel_price_diesel * ratio_fuel_price_diesel_kerosene
    fuel_price_kerosene_aviation = transport_fuel_price_diesel * ratio_fuel_price_diesel_kerosene_aviation

    transport_fuel_price_fuel_oil = fuel_price_fuel_oil
    transport_fuel_price_kerosene = fuel_price_kerosene
    transport_fuel_price_gasoline = fuel_price_gasoline
    transport_fuel_price_kerosene_aviation = fuel_price_kerosene_aviation

    #cost information

    transport_fuel_price_electric = np.array(df_in["industry_and_mining_fuel_price_electric"])
    transport_fuel_price_hydrogen = np.array(df_in["industry_and_mining_fuel_price_hydrogen"])


    transport_private_investment_cost_gasoline = np.array(df_in["transport_private_investment_cost_gasoline"])
    transport_private_investment_cost_diesel = np.array(df_in["transport_private_investment_cost_diesel"])
    transport_private_investment_cost_electric = np.array(df_in["transport_private_investment_cost_electric"])
    transport_private_investment_cost_hyb = np.array(df_in["transport_private_investment_cost_hyb"])
    transport_bus_investment_cost_diesel = np.array(df_in["transport_bus_investment_cost_diesel"])
    transport_bus_investment_cost_electric = np.array(df_in["transport_bus_investment_cost_electric"])
    transport_truck_investment_cost_diesel = np.array(df_in["transport_truck_investment_cost_diesel"])
    transport_truck_investment_cost_hydrogen = np.array(df_in["transport_truck_investment_cost_hydrogen"])
    transport_aviation_investment_cost_kerosene = np.array(df_in["transport_aviation_investment_cost_kerosene"])
    transport_aviation_investment_cost_hydrogen = np.array(df_in["transport_aviation_investment_cost_hydrogen"])
    transport_investment_cost_modal_split_private_to_bus = np.array(df_in["transport_investment_cost_modal_split_private_to_bus"])
    transport_investment_cost_modal_split_private_to_train = np.array(df_in["transport_investment_cost_modal_split_private_to_train"])
    transport_investment_cost_modal_split_private_to_cycling = np.array(df_in["transport_investment_cost_modal_split_private_to_cycling"])
    transport_investment_cost_modal_split_private_to_telework = np.array(df_in["transport_investment_cost_modal_split_private_to_telework"])

    ############################################
    #    ROAD PASSENGER  - PRIVATE TRANSPORT   #
    ############################################

    # Read input parameters defined in parameter_ranges.csv
    year = np.array(df_in["year"])  # vector years
    population = np.array(df_in["poblacion"])
    gdp = np.array(df_in["pib"]) * np.array(df_in["pib_scalar_transport"])

    # average distance by trip
    trip_distance_private = np.array(df_in["transport_trip_distance_private"])

    # modal split changes from private transport to other modes
    modal_split_private_to_taxi = np.array(df_in["transport_modal_split_private_to_taxi"])
    modal_split_private_to_bus = np.array(df_in["transport_modal_split_private_to_bus"])
    modal_split_private_to_train = np.array(df_in["transport_modal_split_private_to_train"])
    modal_split_private_to_cycling = np.array(df_in["transport_modal_split_private_to_cycling"])
    modal_split_private_to_telework = np.array(df_in["transport_modal_split_private_to_telework"])

    frac_private_gasoline = np.array(df_in["transport_frac_private_gasoline"])
    frac_private_electric = np.array(df_in["transport_frac_private_electric"])
    frac_private_hyb = np.array(df_in["transport_frac_private_hyb"])

    frac_taxi_gasoline = np.array(df_in["transport_frac_taxi_gasoline"])
    frac_taxi_electric = np.array(df_in["transport_frac_taxi_electric"])

    frac_bus_diesel = np.array(df_in["transport_frac_bus_diesel"])
    frac_bus_electric = np.array(df_in["transport_frac_bus_electric"])

    intensity_private_gasoline = np.array(df_in["transport_intensity_private_gasoline"])
    intensity_private_electric = np.array(df_in["transport_intensity_private_electric"])
    intensity_private_hyb_electric = np.array(df_in["transport_intensity_private_hyb_electric"])
    intensity_private_hyb_gasoline = np.array(df_in["transport_intensity_private_hyb_gasoline"])
    intensity_taxi_gasoline = np.array(df_in["transport_intensity_taxi_gasoline"])
    intensity_taxi_electric = np.array(df_in["transport_intensity_taxi_electric"])
    intensity_bus_diesel = np.array(df_in["transport_intensity_bus_diesel"])
    intensity_bus_electric = np.array(df_in["transport_intensity_bus_electric"])
    intensity_train_electric = np.array(df_in["transport_intensity_train_electric"])

    transport_activity_taxi = np.array(df_in["transport_activity_taxi"])
    transport_activity_private = np.array(df_in["transport_activity_private"])
    transport_activity_bus = np.array(df_in["transport_activity_bus"])

    occupancy_rate_private = np.array(df_in["transport_occupancy_rate_private"])
    occupancy_rate_taxi = np.array(df_in["transport_occupancy_rate_taxi"])
    occupancy_rate_bus = np.array(df_in["transport_occupancy_rate_bus"])
    occupancy_rate_train = np.array(df_in["transport_occupancy_rate_train"])

    emission_fact_gasoline = np.array(df_in["transport_emission_fact_gasoline"])
    emission_fact_diesel = np.array(df_in["transport_emission_fact_diesel"])

    # econometric model to project private demand of gasoline (light and medium vehicle) -auxiliar variable
    transport_private_gasoline_demand = model_transport_gasoline_demand(year, gdp)

    # calculate total number of private trips (trips/day/person)
    transport_trips_private = transport_private_gasoline_demand * intensity_private_gasoline * occupancy_rate_private / (365 * population * trip_distance_private) / den_gasoline / pc_gasoline * (10 ** 9)

    # calculate total number of trips by mode of transport
    # taxis
    transport_trips_private_to_taxi = transport_trips_private * modal_split_private_to_taxi
    # bus
    transport_trips_private_to_bus = transport_trips_private * modal_split_private_to_bus
    # train
    transport_trips_private_to_train = transport_trips_private * modal_split_private_to_train
    # cycling
    transport_trips_private_to_cycling = transport_trips_private * modal_split_private_to_cycling
    # teleworking
    transport_trips_private_to_telework = transport_trips_private * modal_split_private_to_telework
    # private, updating according to modal changes
    transport_private_trips = transport_trips_private - transport_trips_private_to_taxi - transport_trips_private_to_bus - transport_trips_private_to_train - transport_trips_private_to_cycling - transport_trips_private_to_telework

    # calculate veh-km by mode of transport
    veh_km_private = transport_private_trips * 365 * population * trip_distance_private / occupancy_rate_private
    veh_km_private_to_taxi = transport_trips_private_to_taxi * 365 * population * trip_distance_private / occupancy_rate_taxi
    veh_km_private_to_bus = transport_trips_private_to_bus * 365 * population * trip_distance_private / occupancy_rate_bus
    veh_km_private_to_train = transport_trips_private_to_train * 365 * population * trip_distance_private / occupancy_rate_train
    veh_km_private_to_cycling = transport_trips_private_to_cycling * 365 * population * trip_distance_private
    veh_km_private_to_teleworking = transport_trips_private_to_telework * 365 * population * trip_distance_private

    # calculate veh-km by mode of transport and technology
    # private
    veh_km_private_gasoline = veh_km_private * frac_private_gasoline
    veh_km_private_electric = veh_km_private * frac_private_electric
    veh_km_private_hyb = veh_km_private * frac_private_hyb
    # taxis
    veh_km_private_to_taxi_gasoline = veh_km_private_to_taxi * frac_taxi_gasoline
    veh_km_private_to_taxi_electric = veh_km_private_to_taxi * frac_taxi_electric
    # buses
    veh_km_private_to_bus_diesel = veh_km_private_to_bus * frac_bus_diesel
    veh_km_private_to_bus_electric = veh_km_private_to_bus * frac_bus_electric
    # train
    veh_km_private_to_train_electric = veh_km_private_to_train

    # calculate demand in Tcal
    # private
    transport_dem_private_gasoline = veh_km_private_gasoline / intensity_private_gasoline * den_gasoline * pc_gasoline / (10 ** 9)
    transport_dem_private_electric = veh_km_private_electric / intensity_private_electric / fact2 / (10 ** 6)
    transport_dem_private_hyb_gasoline = veh_km_private_hyb / intensity_private_hyb_gasoline * den_gasoline * pc_gasoline / (10 ** 9)
    transport_dem_private_hyb_electric = veh_km_private_hyb / intensity_private_hyb_electric / fact2 / (10 ** 6)
    # taxis
    transport_dem_taxi_gasoline = veh_km_private_to_taxi_gasoline / intensity_taxi_gasoline * den_gasoline * pc_gasoline / (10 ** 9)
    transport_dem_taxi_electric = veh_km_private_to_taxi_electric / intensity_taxi_electric / fact2 / (10 ** 6)
    # buses
    transport_dem_bus_diesel_aux = veh_km_private_to_bus_diesel / intensity_bus_diesel * den_diesel * pc_diesel / (10 ** 9)
    transport_dem_bus_electric_aux = veh_km_private_to_bus_electric / intensity_bus_electric / fact2 / (10 ** 6)
    # train
    transport_dem_train_electric_aux = veh_km_private_to_train_electric / intensity_train_electric / fact2 / (10 ** 6)

    # calculate emission in millon tCO2
    transport_emission_private_gasoline = transport_dem_private_gasoline * fact * emission_fact_gasoline / (10 ** 9)

    transport_emission_taxi_gasoline = transport_dem_taxi_gasoline * fact * emission_fact_gasoline / (10 ** 9)
    transport_emission_taxi = transport_emission_taxi_gasoline

    ############################################
    #    ROAD PASSENGER  - PUBLIC TRANSPORT BUS  #
    ############################################
    # Read input parameters defined in parameter_ranges.csv
    # veh-km
    transport_bus_veh_km = np.array(df_in["transport_bus_veh_km"])
    frac_bus_diesel = np.array(df_in["transport_frac_bus_diesel"])
    frac_bus_electric = np.array(df_in["transport_frac_bus_electric"])


    # calculate demand in Tcal
    transport_dem_bus_diesel = transport_bus_veh_km * frac_bus_diesel / intensity_bus_diesel * den_diesel * pc_diesel / (10 ** 9)
    transport_dem_bus_electric = transport_bus_veh_km * frac_bus_electric / intensity_bus_electric / fact2 / (10 ** 6)
    # add demand related to modal change from private vehicles
    transport_dem_bus_diesel = transport_dem_bus_diesel + transport_dem_bus_diesel_aux
    transport_dem_bus_electric = transport_dem_bus_electric + transport_dem_bus_electric_aux

    # emission bus
    transport_emission_bus_diesel = transport_dem_bus_diesel * fact * emission_fact_diesel / (10 ** 9)
    transport_emission_bus = transport_emission_bus_diesel

    ############################################
    #    ROAD PASSENGER  - TRAIN TRANSPORT  #
    ############################################
    # it includes Metro de Santiago, Merval y Biotren

    intensity_pkm_train = np.array(df_in["transport_intensity_pkm_train"])
    train_VIII_pkm = np.array(df_in["transport_train8_pkm"])
    train_V_pkm = np.array(df_in["transport_train5_pkm"])
    train_RM_pkm = np.array(df_in["transport_train13_pkm"])

    # total train pkm
    transport_train_pkm = train_RM_pkm + train_V_pkm + train_VIII_pkm
    transport_dem_train_electric = transport_train_pkm * intensity_pkm_train / fact2 / (10 ** 6)
    # add modal change from private sector
    transport_dem_train_electric = transport_dem_train_electric + transport_dem_train_electric_aux

    ###########################
    #    FREIGHT ROAD TRANSPORT    #
    ###########################
    # Read input parameters defined in parameter_ranges.csv

    # modal split diesel demand of truck and private vehicles
    transport_share_diesel_truck_aux = np.array(df_in["transport_share_diesel_truck"])

    intensity_truck_diesel = np.array(df_in["transport_intensity_truck_diesel"])
    intensity_truck_hydrogen = np.array(df_in["transport_intensity_truck_hydrogen"])

    intensity_train_freight_diesel = np.array(df_in["transport_intensity_train_freight_diesel"])

    load_average_truck = np.array(df_in["transport_load_average_truck"])
    load_average_freight_train = np.array(df_in["transport_load_average_freight_train"])

    frac_truck_diesel = np.array(df_in["transport_frac_truck_diesel"])
    frac_truck_hydrogen = np.array(df_in["transport_frac_truck_hydrogen"])

    transport_activity_truck = np.array(df_in["transport_activity_truck"])

    # modal change
    modal_split_truck = np.array(df_in["transport_modal_split_truck"])
    modal_split_truck_to_train = np.array(df_in["transport_modal_split_truck_to_train"])

    # econometric model to project private demand of diesel (trucks + private vehicle)
    alfa = 0
    beta = 0.877412

    # calculate diesel demand in Tcal as function of GDP
    transport_diesel_demand = np.exp(alfa + beta * np.log(gdp))

    transport_truck_diesel_aux = transport_diesel_demand * transport_share_diesel_truck_aux

    # TKM
    transport_tkm = transport_truck_diesel_aux * intensity_truck_diesel * load_average_truck / den_diesel / pc_diesel * (10  ** 9)
    transport_tkm_truck = transport_tkm * modal_split_truck
    transport_tkm_truck_to_train = transport_tkm * modal_split_truck_to_train

    # calculate demand in Tcal
    transport_dem_truck_diesel = transport_tkm_truck * frac_truck_diesel / intensity_truck_diesel / load_average_truck * den_diesel * pc_diesel / (10 ** 9)
    transport_dem_truck_hydrogen = transport_tkm_truck * frac_truck_hydrogen / intensity_truck_hydrogen / load_average_truck * pc_hydrogen / (10 ** 9)
    transport_dem_freight_trail_diesel = transport_tkm_truck_to_train / intensity_train_freight_diesel / load_average_freight_train * den_diesel * pc_diesel / (10 ** 9)

    # emission truck
    transport_emission_truck_diesel = transport_dem_truck_diesel * fact * emission_fact_diesel / (10 ** 9)
    transport_emission_truck = transport_emission_truck_diesel

    ###########################
    #    FREIGHT TRAIN TRANSPORT    #
    ###########################
    transport_tkm_train = np.array(df_in["transport_tkm_freight_train"])
    transport_dem_freight_trail_diesel = transport_tkm_truck_to_train + transport_tkm_train / intensity_train_freight_diesel / load_average_freight_train * den_diesel * pc_diesel / (10 ** 9)

    # emission freight train
    transport_emission_train_diesel = transport_dem_freight_trail_diesel * fact * emission_fact_diesel / (10 ** 9)
    transport_emission_train = transport_emission_train_diesel

    ############################################
    #    PRIVATE TRANSPORT OTHER DIESEL DEMANDS  #
    ############################################

    transport_share_diesel_private_aux = np.array(df_in["transport_share_diesel_private"])
    intensity_private_diesel = np.array(df_in["transport_intensity_private_diesel"])

    # veh-km
    veh_km_private_diesel = transport_diesel_demand * transport_share_diesel_private_aux * intensity_private_diesel / den_diesel / pc_diesel * (10 ** 9)

    # calculate demand in Tcal
    transport_dem_private_diesel = veh_km_private_diesel * (1 - frac_private_electric) / intensity_private_diesel * den_diesel * pc_diesel / (10 ** 9)
    transport_dem_private_electric = transport_dem_private_electric + veh_km_private_diesel * frac_private_electric / intensity_private_electric / fact2 / (10 ** 6)

    # calculate emission in millon tCO2
    transport_emission_private_diesel = transport_dem_private_diesel * fact * emission_fact_diesel / (10 ** 9)
    transport_emission_private = transport_emission_private_gasoline + transport_emission_private_diesel

    ###########################
    #    MARITIME TRANSPORT    #
    ###########################
    # Read input parameters defined in parameter_ranges.csv

    transport_tkm_maritime = np.array(df_in["transport_tkm_maritime"])

    intensity_maritime = np.array(df_in["transport_intensity_maritime"])
    frac_maritime_diesel = np.array(df_in["transport_maritime_frac_diesel"])
    frac_maritime_fueloil = np.array(df_in["transport_maritime_frac_fueloil"])
    emission_fact_fueloil = np.array(df_in["transport_emission_fact_fueloil"])

    # calculate demand in Tcal
    transport_demand_maritime_diesel = transport_tkm_maritime * intensity_maritime * frac_maritime_diesel / (10 ** 3)
    transport_demand_maritime_fueloil = transport_tkm_maritime * intensity_maritime * frac_maritime_fueloil / (10 ** 3)

    # calculate emission
    transport_emission_maritime_diesel = transport_demand_maritime_diesel * fact * emission_fact_diesel / (10 ** 9)
    transport_emission_maritime_fueloil = transport_demand_maritime_fueloil * fact * emission_fact_fueloil / (10 ** 9)
    transport_emission_maritime = transport_emission_maritime_diesel + transport_emission_maritime_fueloil

    ###########################
    #    AVIATION TRANSPORT    #
    ###########################

    # Read input parameters defined in parameter_ranges.csv
    if True:
        intensity_aviation_kerosene = np.array(df_in["transport_intensity_aviation_kerosene"])
        intensity_aviation_hydrogen = np.array(df_in["transport_intensity_aviation_hydrogen"])
        transport_frac_aviation_kerosene = np.array(df_in["transport_frac_aviation_kerosene"])
        transport_frac_aviation_hydrogen = np.array(df_in["transport_frac_aviation_hydrogen"])
        emission_fact_kerosene_aviation = np.array(df_in["transport_emission_fact_kerosene_aviation"])
        transport_saturation_aviation = np.array(df_in["transport_saturation_aviation"])

        #pkm = f(GDP)
        transport_pkm_aviation = model_transport_pkm_aviation(year, gdp)
        #Saturation
        transport_pkm_aviation = model_transport_pkm_saturacion(year, transport_pkm_aviation, transport_saturation_aviation)
        
        # calculate demand in Tcal
        transport_demand_aviation_kerosene = transport_pkm_aviation * transport_frac_aviation_kerosene * intensity_aviation_kerosene / (10 ** 3)
        transport_demand_aviation_hydrogen = transport_pkm_aviation * transport_frac_aviation_hydrogen * intensity_aviation_hydrogen / (10 ** 3)

        # calculate emission
        transport_emission_aviation = transport_demand_aviation_kerosene * fact * emission_fact_kerosene_aviation / (10 ** 9)
    else:
    
        #
        #
        #   CONDITIONAL STATEMENT FROM J SYME ADDED TO ALLOW MODEL RUN ON 1/30
        #   --- THIS IS THE MODEL FROM 1/30 ---
        #   NOTE, COSTS MAY BE INCORRECT
        #

                # pkm= f(GDP), pending
        transport_pkm_aviation = model_transport_pkm_aviation(year, gdp)
        
        intensity_aviation_hydrogen = np.array(df_in["transport_intensity_aviation_hydrogen"])
        transport_frac_aviation_hydrogen = np.array(df_in["transport_frac_aviation_hydrogen"])
        transport_frac_aviation_kerosene = np.array(df_in["transport_frac_aviation_kerosene"])
        emission_fact_kerosene_aviation = np.array(df_in["transport_emission_fact_kerosene_aviation"])
        transport_saturation_aviation = np.array(df_in["transport_saturation_aviation"])
        transport_demand_aviation_hydrogen = transport_pkm_aviation * transport_frac_aviation_hydrogen * intensity_aviation_hydrogen / (10 ** 3)
        
        intensity_aviation_kerosene = np.array(df_in["transport_intensity_aviation_kerosene"])
        emission_fact_kerosene_aviation = np.array(df_in["transport_emission_fact_kerosene_aviation"])
        transport_saturation_aviation = np.array(df_in["transport_saturation_aviation"])

        # calculate demand in Tcal
        transport_demand_aviation_kerosene = transport_pkm_aviation * intensity_aviation_kerosene / (10 ** 3)

        transport_demand_aviation_kerosene = model_transport_pkm_saturacion(year, transport_demand_aviation_kerosene,transport_saturation_aviation)

        # calculate emission
        transport_emission_aviation = transport_demand_aviation_kerosene * fact * emission_fact_kerosene_aviation / (10 ** 9)


    #############################################################################
    ################# COST INFORMATION ##########################################

    #################### PRIVATE ################################################

    # OPEX (in millon US$)
    transport_OPEX_private_gasoline = transport_dem_private_gasoline * transport_fuel_price_gasoline / (10 ** 6)
    transport_OPEX_private_diesel = transport_dem_private_diesel * transport_fuel_price_diesel / (10 ** 6)
    transport_OPEX_private_electric = transport_dem_private_electric * transport_fuel_price_electric / (10 ** 6)
    transport_OPEX_private_hyb = (transport_dem_private_hyb_electric * transport_fuel_price_electric + transport_dem_private_hyb_gasoline * transport_fuel_price_gasoline) / (10 ** 6)
    transport_OPEX_private = transport_OPEX_private_gasoline+transport_OPEX_private_diesel+transport_OPEX_private_electric + transport_OPEX_private_hyb


    #Capacity

    transport_capacity_private_gasoline = transport_dem_private_gasoline / (den_gasoline * pc_gasoline) * intensity_private_gasoline * (10 ** 9) / transport_activity_private
    transport_capacity_private_diesel = transport_dem_private_diesel/ (den_diesel*pc_diesel) * intensity_private_diesel * (10**9)/ transport_activity_private
    transport_capacity_private_electric = transport_dem_private_electric * fact2 * intensity_private_electric * (10 ** 6) / transport_activity_private
    transport_capacity_private_hyb = (transport_dem_private_hyb_gasoline/ (den_gasoline * pc_gasoline) * intensity_private_hyb_gasoline * (10 ** 9) / transport_activity_private) + (transport_dem_private_hyb_electric * fact2 * intensity_private_hyb_electric * (10 ** 6) / transport_activity_private)

    transport_capacity_private_gasoline = model_capacity(year, transport_capacity_private_gasoline)
    transport_capacity_private_diesel = model_capacity(year, transport_capacity_private_diesel)
    transport_capacity_private_electric = model_capacity(year, transport_capacity_private_electric)
    transport_capacity_private_hyb = model_capacity(year, transport_capacity_private_hyb)

    transport_delta_capacity_private_gasoline = model_delta_capacity(year, transport_capacity_private_gasoline)
    transport_delta_capacity_private_diesel = model_delta_capacity(year, transport_capacity_private_diesel)
    transport_delta_capacity_private_electric = model_delta_capacity(year, transport_capacity_private_electric)
    transport_delta_capacity_private_hyb = model_delta_capacity(year, transport_capacity_private_hyb)

    # CAPEX (in millon US$)
    transport_CAPEX_private_gasoline = transport_delta_capacity_private_gasoline * transport_private_investment_cost_gasoline / (10 ** 6)
    transport_CAPEX_private_diesel = transport_delta_capacity_private_diesel * transport_private_investment_cost_diesel / (10 ** 6)
    transport_CAPEX_private_electric = transport_delta_capacity_private_electric * transport_private_investment_cost_electric / (10 ** 6)
    transport_CAPEX_private_hyb = transport_delta_capacity_private_hyb * transport_private_investment_cost_hyb / (10 ** 6)
    transport_CAPEX_private = transport_CAPEX_private_gasoline+transport_CAPEX_private_diesel+transport_CAPEX_private_electric + transport_CAPEX_private_hyb

    #CAPEX modal change
    pkm_modal_change_private_to_bus = veh_km_private_to_bus * occupancy_rate_bus
    pkm_modal_change_private_to_train= veh_km_private_to_train * occupancy_rate_train
    pkm_modal_change_private_to_cycling = veh_km_private_to_cycling
    pkm_modal_change_private_to_teleworking = veh_km_private_to_teleworking

    delta_pkm_modal_change_private_to_bus= model_delta_capacity(year, pkm_modal_change_private_to_bus)
    delta_pkm_modal_change_private_to_train = model_delta_capacity(year, pkm_modal_change_private_to_train)
    delta_pkm_modal_change_private_to_cycling = model_delta_capacity(year, pkm_modal_change_private_to_cycling)
    delta_pkm_modal_change_private_to_teleworking = model_delta_capacity(year, pkm_modal_change_private_to_teleworking)

    transport_CAPEX_modal_change_private_to_bus = transport_investment_cost_modal_split_private_to_bus * delta_pkm_modal_change_private_to_bus / (10 ** 6)
    transport_CAPEX_modal_change_private_to_train = transport_investment_cost_modal_split_private_to_train * delta_pkm_modal_change_private_to_train / (10 ** 6)
    transport_CAPEX_modal_change_private_to_cycling = transport_investment_cost_modal_split_private_to_cycling * delta_pkm_modal_change_private_to_cycling / (10 ** 6)
    transport_CAPEX_modal_change_private_to_telework = transport_investment_cost_modal_split_private_to_telework  * delta_pkm_modal_change_private_to_teleworking/ (10 ** 6)
    transport_CAPEX_private_modal_change = transport_CAPEX_modal_change_private_to_bus +transport_CAPEX_modal_change_private_to_train+ transport_CAPEX_modal_change_private_to_cycling+transport_CAPEX_modal_change_private_to_telework

    # CAPEX, OPEX
    dict_CAPEX = {"transport_private": transport_CAPEX_private}
    dict_OPEX = {"transport_private": transport_OPEX_private}

    dict_CAPEX.update({"transport_private_modal_change": transport_CAPEX_private_modal_change})

    #################### TAXI ################################################

    # OPEX (in millon US$)
    transport_OPEX_taxi_gasoline = transport_dem_taxi_gasoline * transport_fuel_price_gasoline / (10 ** 6)
    transport_OPEX_taxi_electric = transport_dem_taxi_electric * transport_fuel_price_electric / (10 ** 6)
    transport_OPEX_taxi = transport_OPEX_taxi_gasoline + transport_OPEX_taxi_electric

    # Capacity
    transport_capacity_taxi_gasoline = transport_dem_taxi_gasoline / (den_gasoline * pc_gasoline) * intensity_taxi_gasoline * (10 ** 9) / transport_activity_taxi
    transport_capacity_taxi_electric = transport_dem_taxi_electric * fact2 * intensity_taxi_electric * (10 ** 6) / transport_activity_taxi

    transport_capacity_taxi_gasoline = model_capacity(year, transport_capacity_taxi_gasoline)
    transport_capacity_taxi_electric = model_capacity(year, transport_capacity_taxi_electric)

    transport_delta_capacity_taxi_gasoline = model_delta_capacity(year, transport_capacity_taxi_gasoline)
    transport_delta_capacity_taxi_electric = model_delta_capacity(year, transport_capacity_taxi_electric)

    # CAPEX (in millon US$)
    transport_CAPEX_taxi_gasoline = transport_delta_capacity_taxi_gasoline * transport_private_investment_cost_gasoline / (10 ** 6)
    transport_CAPEX_taxi_electric = transport_delta_capacity_taxi_electric * transport_private_investment_cost_electric / (10 ** 6)
    transport_CAPEX_taxi =transport_CAPEX_taxi_gasoline+transport_CAPEX_taxi_electric

    # CAPEX, OPEX
    dict_CAPEX.update({"transport_taxi": transport_CAPEX_taxi})
    dict_OPEX.update ({"transport_taxi": transport_OPEX_taxi})

    #################### BUS ################################################

    # OPEX (in millon US$)
    transport_OPEX_bus_diesel = transport_dem_bus_diesel * transport_fuel_price_diesel / (10 ** 6)
    transport_OPEX_bus_electric = transport_dem_bus_electric * transport_fuel_price_electric / (10 ** 6)
    transport_OPEX_bus = transport_OPEX_bus_diesel + transport_OPEX_bus_electric

    # Capacity

    transport_capacity_bus_diesel = transport_dem_bus_diesel / (den_diesel * pc_diesel) * intensity_bus_diesel * (10 ** 9) / transport_activity_bus
    transport_capacity_bus_electric = transport_dem_bus_electric * fact2 * intensity_bus_electric * (10 ** 6) / transport_activity_bus

    transport_capacity_bus_diesel = model_capacity(year, transport_capacity_bus_diesel)
    transport_capacity_bus_electric = model_capacity(year, transport_capacity_bus_electric)

    transport_delta_capacity_bus_diesel = model_delta_capacity(year, transport_capacity_bus_diesel)
    transport_delta_capacity_bus_electric = model_delta_capacity(year, transport_capacity_bus_electric)

    # CAPEX (in millon US$)
    transport_CAPEX_bus_diesel = transport_delta_capacity_bus_diesel * transport_bus_investment_cost_diesel / (10 ** 6)
    transport_CAPEX_bus_electric = transport_delta_capacity_bus_electric * transport_bus_investment_cost_electric / (10 ** 6)
    transport_CAPEX_bus = transport_CAPEX_bus_diesel + transport_CAPEX_bus_electric

    # CAPEX, OPEX
    dict_CAPEX.update({"transport_bus": transport_CAPEX_bus})
    dict_OPEX.update({"transport_bus": transport_OPEX_bus})

    #################### TRUCK ################################################

    # OPEX (in millon US$)
    transport_OPEX_truck_diesel = transport_dem_truck_diesel * transport_fuel_price_diesel / (10 ** 6)
    transport_OPEX_truck_hydrogen = transport_dem_truck_hydrogen * transport_fuel_price_hydrogen / (10 ** 6)
    transport_OPEX_truck =  transport_OPEX_truck_diesel + transport_OPEX_truck_hydrogen

    # Capacity

    transport_capacity_truck_diesel = transport_dem_truck_diesel / (den_diesel * pc_diesel) * intensity_truck_diesel * (10 ** 9) / transport_activity_truck
    transport_capacity_truck_hydrogen = transport_dem_truck_hydrogen / pc_hydrogen * intensity_truck_hydrogen * (10 ** 9) / transport_activity_truck

    transport_capacity_truck_diesel = model_capacity(year, transport_capacity_truck_diesel)
    transport_capacity_truck_hydrogen = model_capacity(year, transport_capacity_truck_hydrogen)

    transport_delta_capacity_truck_diesel = model_delta_capacity(year, transport_capacity_truck_diesel)
    transport_delta_capacity_truck_hydrogen = model_delta_capacity(year, transport_capacity_truck_hydrogen)

    # CAPEX (in millon US$)
    transport_CAPEX_truck_diesel = transport_delta_capacity_truck_diesel * transport_truck_investment_cost_diesel / (10 ** 6)
    transport_CAPEX_truck_hydrogen = transport_delta_capacity_truck_hydrogen * transport_truck_investment_cost_hydrogen / (10 ** 6)
    transport_CAPEX_truck = transport_CAPEX_truck_diesel + transport_CAPEX_truck_hydrogen

    # CAPEX, OPEX
    dict_CAPEX.update({"transport_truck": transport_CAPEX_truck})
    dict_OPEX.update({"transport_truck": transport_OPEX_truck})

    #########################AVIATION#############################################
    # OPEX (in millon US$)
    transport_OPEX_aviation_diesel = transport_demand_aviation_kerosene * transport_fuel_price_kerosene_aviation / (10 ** 6)
    transport_OPEX_aviation_hydrogen = transport_demand_aviation_hydrogen * transport_fuel_price_hydrogen / (10 ** 6)
    transport_OPEX_aviation = transport_OPEX_aviation_diesel + transport_OPEX_aviation_hydrogen
    
    # Capacity

    transport_capacity_aviation_kerosene = model_capacity(year, transport_pkm_aviation * transport_frac_aviation_kerosene)
    transport_capacity_aviation_hydrogen = model_capacity(year,transport_pkm_aviation * transport_frac_aviation_hydrogen)

    transport_delta_capacity_aviation_kerosene = model_delta_capacity(year, transport_capacity_aviation_kerosene)
    transport_delta_capacity_aviation_hydrogen = model_delta_capacity(year, transport_capacity_aviation_hydrogen)

    # CAPEX (in millon US$)
    transport_CAPEX_aviation_kerosene = transport_delta_capacity_aviation_kerosene * transport_aviation_investment_cost_kerosene / (10 ** 6)
    transport_CAPEX_aviation_hydrogen = transport_delta_capacity_aviation_hydrogen * transport_aviation_investment_cost_hydrogen / (10 ** 6)
    transport_CAPEX_aviation = transport_CAPEX_aviation_kerosene + transport_CAPEX_aviation_hydrogen

    # CAPEX, OPEX
    dict_CAPEX.update({"transport_aviation": transport_CAPEX_aviation})
    dict_OPEX.update({"transport_aviation": transport_OPEX_aviation})
    ##############################################################################

    # summary
    # export emission
    dict_emission = {"transport_private": transport_emission_private, "transport_taxi": transport_emission_taxi,
                     "transport_bus": transport_emission_bus, "transport_truck": transport_emission_truck,
                     "transport_train": transport_emission_train, "transport_aviation": transport_emission_aviation,
                     "transport_maritime": transport_emission_maritime}

    # export electric demand in GWh
    transport_dem_electric = transport_dem_private_electric + transport_dem_private_hyb_electric + transport_dem_bus_electric + transport_dem_taxi_electric + transport_dem_train_electric
    transport_dem_electric = transport_dem_electric * fact2
    dict_electric_demand = {"transport": transport_dem_electric}

    # electric demand to produce hydrogen
    electric_demand_hydrogen = (transport_dem_truck_hydrogen+transport_OPEX_aviation_hydrogen) / electrolyzer_efficiency * share_electric_grid_to_hydrogen
    # WARNING: factor de correccion, a al espera de aclarar supuestos de modelacion (se supuso share electric grid igual a 0.5 en vez de 1)
    fact_correccion = 1
    electric_demand_hydrogen = electric_demand_hydrogen * fact2 * fact_correccion

    ##  final output dictionary

    dict_out = {}

    vec_total_emissions = 0
    # add emissions to master output
    for k in dict_emission.keys():
        # new key conveys emissions
        k_new = str(k).replace("transport_", (dict_sector_abv["transport"] + "-emissions_")) + "-mtco2e"
        # add to outputaz
        dict_out.update({k_new: dict_emission[k].copy()})
        # update total
        vec_total_emissions = vec_total_emissions + np.array(dict_emission[k])

    vec_total_demand_electricity = 0
    # add electric demand to master output
    for k in dict_electric_demand.keys():
        # new key conveys emissions
        k_new = str(k).replace(k, dict_sector_abv[k]) + "-electricity_total_demand-gwh"
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
        k_new = (dict_sector_abv["transport"]) + "-OPEX_" + str(k) + "-MMUSD"
        # add to output
        dict_out.update({k_new: dict_OPEX[k].copy()})
        # update total
        vec_total_OPEX = vec_total_OPEX + np.array(dict_OPEX[k])

    # add OPEX to master output
    vec_total_CAPEX = 0
    for k in dict_CAPEX.keys():
        # new key conveys emissions
        k_new = (dict_sector_abv["transport"]) + "-CAPEX_" + str(k) + "-MMUSD"
        # add to output
        dict_out.update({k_new: dict_CAPEX[k].copy()})
        # update total
        vec_total_CAPEX = vec_total_CAPEX + np.array(dict_CAPEX[k])

    # add totals
    dict_out.update({
        (dict_sector_abv["transport"] + "-emissions_total-mtco2e"): vec_total_emissions,
        (dict_sector_abv["transport"] + "-electricity_total_demand-gwh"): vec_total_demand_electricity,
        (dict_sector_abv["transport"] + "-electricity_hydrogen-gwh"): electric_demand_hydrogen,
        (dict_sector_abv["transport"] + "-OPEX-MMUSD"): vec_total_OPEX,
        (dict_sector_abv["transport"] + "-CAPEX-MMUSD"): vec_total_CAPEX,
    })
        
    # return
    return dict_out  # dict_emission,dict_electric_demand
