import os, os.path
import numpy as np
import time
import pandas as pd
import setup_runs as sr
import sector_models as sm
import shutil


##############
#    TEMP    #
##############

dir_out_gams = os.path.join(os.path.dirname(os.path.dirname(sr.dir_model)), "ssh", "download", "pmr_data_output_20201022")

df_gams_emissions = pd.read_csv(os.path.join(dir_out_gams, "solucion_emisiones_ge_co2e.csv"))

#pmr GEIs with non-zero emissions
all_emitters = set(df_gams_emissions[df_gams_emissions["emisiones"] > 0]["GEI"])
df_gams_emissions = df_gams_emissions[df_gams_emissions["GEI"].isin(all_emitters)]
df_gams_emissions["GEI"] = [x.replace(" ", "") for x in df_gams_emissions["GEI"]]
df_gams_emissions["sf_co2e"] = df_gams_emissions["GEI"].replace({"CO2": 1, "N2O": 310})
#TEMP
df_gams_emissions = df_gams_emissions[df_gams_emissions["GEI"] == "CO2"]
#multiply through
df_gams_emissions["emissions_co2e"] = np.array(df_gams_emissions["emisiones"]) * np.array(df_gams_emissions["sf_co2e"])
#aggregate
df_ge = df_gams_emissions[["agno", "emissions_co2e"]].groupby(by = ["agno"]).agg({"agno": "first", "emissions_co2e": "sum"})
df_ge = df_ge.reset_index(drop = True).rename(columns = {"emissions_co2e": "energy_pmr-total_emissions_mt_co2e", "agno": "year"})
df_ge["master_id"] = [0 for x in range(len(df_ge))]

df_ge.to_csv(os.path.join(sr.dir_out, "output_multi_sector_pmr.csv"), index = None, encoding = "UTF-8")
