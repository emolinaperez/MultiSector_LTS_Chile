# -*- coding: utf-8 -*-
"""
"""

# Compendio de funciones que aplican los modelos econometricos a las variables
# sectoriales
# IN: 2 arreglos numpy (years y gdp), uno con los años del dataframe (years)
#    y el otro con el GDP (gdp)
# OUT: retorna el arreglo con la demanda energetica (demand_energy)

import numpy as np


# @jit(nopython=True)
def model_other_industries_new(year, gdp):
	# econometric coeficients
	a = 0.2579
	b = 0.4540
	c = 2.5886
	dem_2017 = 33099.16  # [Tcal]

	# Creacion de la variable a contener la demanda energetica
	demand_energy = np.ones(len(year))

	for i in range(len(year)):
		if year[i] == 2015:
			demand_energy[i] = dem_2017
		elif year[i] == 2016:
			demand_energy[i] = dem_2017
		elif year[i] == 2017:
			demand_energy[i] = dem_2017
		else:
			demand_energy[i] = np.exp(a * np.log(gdp[i]) + b * np.log(demand_energy[i - 1]) + c)

	return demand_energy


def model_other_industries(year, gdp_growth, elasticity):
	# econometric coeficients
	a = 0.2579
	b = 0.4540
	c = 2.5886
	dem_2015 = 33449.82  # [Tcal]
	dem_2016 = 32217.88  # [Tcal]
	dem_2017 = 33099.16  # [Tcal]

	# Creacion de la variable a contener la demanda energetica
	demand_energy = np.ones(len(year))

	for i in range(len(year)):
		if year[i] == 2015:
			demand_energy[i] = dem_2015
		elif year[i] == 2016:
			demand_energy[i] = dem_2016
		elif year[i] == 2017:
			demand_energy[i] = dem_2017
		else:
			demand_energy[i] = demand_energy[i - 1] * (1 + gdp_growth[i] * elasticity[i])

	return demand_energy


def model_commercial(year, gdp_growth, elasticity):
	dem_2015 = 13819.9  # [Tcal]
	dem_2016 = 15599.5  # [Tcal]
	dem_2017 = 15875.2  # [Tcal]

	# Creacion de la variable a contener la demanda energetica
	demand_energy = np.ones(len(year))

	for i in range(len(year)):
		if year[i] == 2015:
			demand_energy[i] = dem_2015
		elif year[i] == 2016:
			demand_energy[i] = dem_2016
		elif year[i] == 2017:
			demand_energy[i] = dem_2017
		else:
			demand_energy[i] = demand_energy[i - 1] * (1 + gdp_growth[i] * elasticity[i])

	return demand_energy


def model_transport_gasoline_demand(year, gdp):
	# econometric coeficients

	a = 0.13085
	b = 0.8636
	c = -0.10389

	dem_2015 = 34476.1  # [Tcal]
	dem_2016 = 36829.5  # [Tcal]
	dem_2017 = 37057.5  # [Tcal]

	# Creacion de la variable a contener la demanda energetica
	demand_energy = np.ones(len(year))

	for i in range(len(year)):
		if year[i] == 2015:
			demand_energy[i] = dem_2015
		elif year[i] == 2016:
			demand_energy[i] = dem_2016
		elif year[i] == 2017:
			demand_energy[i] = dem_2017
		else:
			demand_energy[i] = np.exp(a * np.log(gdp[i]) + b * np.log(demand_energy[i - 1]) + c)

	return demand_energy


def model_transport_pkm_aviation(year, gdp):
	# econometric coeficients

	a = 0.3113
	b = 0.8437
	c = -1.0978

	pkm_2015 = 10862059  # [pkm]
	pkm_2016 = 12200515  # [pkm]
	pkm_2017 = 13134871  # [pkm]

	# Creacion de la variable a contener la demanda energetica
	pkm_aviation = np.ones(len(year))

	for i in range(len(year)):
		if year[i] == 2015:
			pkm_aviation[i] = pkm_2015
		elif year[i] == 2016:
			pkm_aviation[i] = pkm_2016
		elif year[i] == 2017:
			pkm_aviation[i] = pkm_2017
		else:
			pkm_aviation[i] = np.exp(a * np.log(gdp[i]) + b * np.log(pkm_aviation[i - 1]) + c)

	return pkm_aviation


def model_transport_pkm_saturacion(year, transport_demand_aviation_kerosene, transport_saturation_aviation):
	for i in range(len(year)):
		if (transport_demand_aviation_kerosene[i] > transport_saturation_aviation[i]) & (year[i] > 2017):
			transport_demand_aviation_kerosene[i] = transport_demand_aviation_kerosene[i - 1] * 1.001

	return transport_demand_aviation_kerosene


def model_delta_capacity(year, capacity):
	# Creacion de la variable que contiene aumento de capacidad
	delta_capacity = np.ones(len(year))

	for i in range(len(year)):
		if year[i] == 2015:
			delta_capacity[i] = capacity[i]
		elif capacity[i] > capacity[i-1]:
			delta_capacity[i] = capacity[i]-capacity[i-1]
		else:
			delta_capacity[i] = 0

	return delta_capacity

def model_capacity(year, capacity):
	# Creacion de la variable que contiene aumento de capacidad
	adjusted_capacity = np.ones(len(year))

	for i in range(len(year)):
		if year[i] == 2015:
			adjusted_capacity[i] = capacity[i]
		elif capacity[i] > adjusted_capacity[i-1]:
			adjusted_capacity[i] = capacity[i]
		else:
			adjusted_capacity[i] = adjusted_capacity[i-1]

	return adjusted_capacity
