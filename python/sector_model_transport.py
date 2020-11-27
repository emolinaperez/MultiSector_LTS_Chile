# Transport energy model developed by Centro de Energia U. de Chile using RAND python framework
# version 0.7 september 2020

import os, os.path
import time
import pandas as pd
import numpy as np
from econometric_models import model_transport_gasoline_demand, model_transport_pkm_aviation, model_transport_pkm_saturacion

###################
#    TRANSPORT    #
###################

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

	############################################
	#    ROAD PASSENGER  - PRIVATE TRANSPORT   #
	############################################

	# Read input parameters defined in parameter_ranges.csv
	year = np.array(df_in["year"])  # vector years
	population = np.array(df_in["poblacion"])
	gdp = np.array(df_in["pib"]) * np.array(df_in["pib_scalar_transpiort"])

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

	frac_taxi_gasoline = np.array(df_in["transport_frac_taxi_gasoline"])
	frac_taxi_electric = np.array(df_in["transport_frac_taxi_electric"])

	frac_bus_diesel = np.array(df_in["transport_frac_bus_diesel"])
	frac_bus_electric = np.array(df_in["transport_frac_bus_electric"])

	intensity_private_gasoline = np.array(df_in["transport_intensity_private_gasoline"])
	intensity_private_electric = np.array(df_in["transport_intensity_private_electric"])
	intensity_taxi_gasoline = np.array(df_in["transport_intensity_taxi_gasoline"])
	intensity_taxi_electric = np.array(df_in["transport_intensity_taxi_electric"])
	intensity_bus_diesel = np.array(df_in["transport_intensity_bus_diesel"])
	intensity_bus_electric = np.array(df_in["transport_intensity_bus_electric"])
	intensity_train_electric = np.array(df_in["transport_intensity_train_electric"])

	occupancy_rate_private = np.array(df_in["transport_occupancy_rate_private"])
	occupancy_rate_taxi = np.array(df_in["transport_occupancy_rate_taxi"])
	occupancy_rate_bus = np.array(df_in["transport_occupancy_rate_bus"])
	occupancy_rate_train = np.array(df_in["transport_occupancy_rate_train"])

	emission_fact_gasoline = np.array(df_in["transport_emission_fact_gasoline"])
	emission_fact_diesel = np.array(df_in["transport_emission_fact_diesel"])

	# econometric model to project private demand of gasoline (light and medium vehicle) -auxiliar variable
	transport_private_gasoline_demand = model_transport_gasoline_demand(year, gdp)

	# calculate total number of private trips (trips/day/person)
	transport_trips_private = transport_private_gasoline_demand * intensity_private_gasoline * occupancy_rate_private / (
				365 * population * trip_distance_private) / den_gasoline / pc_gasoline * (10 ** 9)

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
	transport_dem_private_gasoline = veh_km_private_gasoline / intensity_private_gasoline * den_gasoline * pc_gasoline / (
				10 ** 9)
	transport_dem_private_electric = veh_km_private_electric / intensity_private_electric / fact2 / (10 ** 6)
	# taxis
	transport_dem_taxi_gasoline = veh_km_private_to_taxi_gasoline / intensity_taxi_gasoline * den_gasoline * pc_gasoline / (
				10 ** 9)
	transport_dem_taxi_electric = veh_km_private_to_taxi_electric / intensity_taxi_electric / fact2 / (10 ** 6)
	# buses
	transport_dem_bus_diesel_aux = veh_km_private_to_bus_diesel / intensity_bus_diesel * den_diesel * pc_diesel / (
				10 ** 9)
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
	transport_dem_bus_diesel = transport_bus_veh_km * frac_bus_diesel / intensity_bus_diesel * den_diesel * pc_diesel / (
				10 ** 9)
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
	transport_tkm = transport_truck_diesel_aux * intensity_truck_diesel * load_average_truck / den_diesel / pc_diesel * (
				10 ** 9)
	transport_tkm_truck = transport_tkm * modal_split_truck
	transport_tkm_truck_to_train = transport_tkm * modal_split_truck_to_train

	# calculate demand in Tcal
	transport_dem_truck_diesel = transport_tkm_truck * frac_truck_diesel / intensity_truck_diesel / load_average_truck * den_diesel * pc_diesel / (
				10 ** 9)
	transport_dem_truck_hydrogen = transport_tkm_truck * frac_truck_hydrogen / intensity_truck_hydrogen / load_average_truck * pc_hydrogen / (
				10 ** 9)
	transport_dem_freight_trail_diesel = transport_tkm_truck_to_train / intensity_train_freight_diesel / load_average_freight_train * den_diesel * pc_diesel / (
				10 ** 9)

	# emission truck
	transport_emission_truck_diesel = transport_dem_truck_diesel * fact * emission_fact_diesel / (10 ** 9)
	transport_emission_truck = transport_emission_truck_diesel

	###########################
	#    FREIGHT TRAIN TRANSPORT    #
	###########################
	transport_tkm_train = np.array(df_in["transport_tkm_freight_train"])
	transport_dem_freight_trail_diesel = transport_tkm_truck_to_train + transport_tkm_train / intensity_train_freight_diesel / load_average_freight_train * den_diesel * pc_diesel / (
				10 ** 9)

	# emission freight train
	transport_emission_train_diesel = transport_dem_freight_trail_diesel * fact * emission_fact_diesel / (10 ** 9)
	transport_emission_train = transport_emission_train_diesel

	############################################
	#    PRIVATE TRANSPORT OTHER DIESEL DEMANDS  #
	############################################

	transport_share_diesel_private_aux = np.array(df_in["transport_share_diesel_private"])
	intensity_private_diesel = np.array(df_in["transport_intensity_private_diesel"])

	# veh-km
	veh_km_private_diesel = transport_diesel_demand * transport_share_diesel_private_aux * intensity_private_diesel / den_diesel / pc_diesel * (
				10 ** 9)

	# calculate demand in Tcal
	transport_dem_private_diesel = veh_km_private_diesel * (
				1 - frac_private_electric) / intensity_private_diesel * den_diesel * pc_diesel / (10 ** 9)
	transport_dem_private_electric = transport_dem_private_electric + veh_km_private_diesel * frac_private_electric / intensity_private_electric / fact2 / (
				10 ** 6)

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

	# pkm= f(GDP), pending
	transport_pkm_aviation = model_transport_pkm_aviation(year, gdp)

	intensity_aviation_kerosene = np.array(df_in["transport_intensity_aviation_kerosene"])
	emission_fact_kerosene_aviation = np.array(df_in["transport_emission_fact_kerosene_aviation"])
	transport_saturation_aviation = np.array(df_in["transport_saturation_aviation"])

	# calculate demand in Tcal
	transport_demand_aviation_kerosene = transport_pkm_aviation * intensity_aviation_kerosene / (10 ** 3)

	transport_demand_aviation_kerosene = model_transport_pkm_saturacion(year, transport_demand_aviation_kerosene,
																		transport_saturation_aviation)

	# calculate emission
	transport_emission_aviation = transport_demand_aviation_kerosene * fact * emission_fact_kerosene_aviation / (
				10 ** 9)

	# summary
	# export emission
	dict_emission = {"transport_private": transport_emission_private, "transport_taxi": transport_emission_taxi,
					 "transport_bus": transport_emission_bus, "transport_truck": transport_emission_truck,
					 "transport_train": transport_emission_train, "transport_aviation": transport_emission_aviation,
					 "transport_maritime": transport_emission_maritime}

	# export electric demand in GWh
	transport_dem_electric = transport_dem_private_electric + transport_dem_bus_electric + transport_dem_taxi_electric + transport_dem_train_electric
	transport_dem_electric = transport_dem_electric * fact2
	dict_electric_demand = {"transport": transport_dem_electric}

	# electric demand to produce hydrogen
	electric_demand_hydrogen = transport_dem_truck_hydrogen / electrolyzer_efficiency * share_electric_grid_to_hydrogen
	# WARNING: factor de correccion, a al espera de aclarar supuestos de modelacion
	fact_correccion = 0.5
	electric_demand_hydrogen = electric_demand_hydrogen * fact2 * fact_correccion

	##  final output dictionary

	dict_out = {}

	vec_total_emissions = 0
	# add emissions to master output
	for k in dict_emission.keys():
		# new key conveys emissions
		k_new = str(k).replace("transport_", (dict_sector_abv["transport"] + "-emissions_")) + "-mtco2e"
		# add to output
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

	# add totals
	dict_out.update({
		(dict_sector_abv["transport"] + "-emissions_total-mtco2e"): vec_total_emissions,
		(dict_sector_abv["transport"] + "-electricity_total_demand-gwh"): vec_total_demand_electricity,
		(dict_sector_abv["transport"] + "-electricity_hydrogen-gwh"): electric_demand_hydrogen,
	})

	# return
	return dict_out  # dict_emission,dict_electric_demand
