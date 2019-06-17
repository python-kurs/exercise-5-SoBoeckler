# Exercise 5
from pathlib import Path
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt

basedir = Path("C:/Users/Admin/Documents/GitHub/exercise-5-SoBoeckler")
input_dir = basedir / "data"
output_dir = basedir / "solution"


# 1. Go to http://surfobs.climate.copernicus.eu/dataaccess/access_eobs.php#datafiles
#    and download the 0.25 deg. file for daily mean temperature.
#    Save the file into the data directory but don't commit it to github!!! [2P]



# 2. Read the file using xarray. Get to know your data. What's in the file?
#    Calculate monthly means for the reference periode 1981-2010 for Europe (Extent: Lon_min:-13, Lon_max: 25, Lat_min: 30, Lat_max: 72). [2P]

tab = xr.open_dataset(input_dir / "tg_ens_mean_0.25deg_reg_v19.0e.nc")
tab_new1 = tab.sel(time=slice("1981-01-01", "2010-12-31"), latitude=slice(30,72), longitude=slice(-13,25))
tab_new1_mean = tab_new1.groupby("time.month").mean("time")



# 3. Calculate monthly anomalies from the reference period for the year 2018 (use the same extent as in #2).
#    Make a quick plot of the anomalies for the region. [2P]

tab_new2 = tab.sel(time=slice("2018", "2018"), latitude=slice(30,72), longitude=slice(-13,25))
tab_new2_mean = tab_new2.groupby("time.month").mean("time")
anom_2018 = tab_new2_mean - tab_new1_mean

anom_2018["tg"].plot()


# 4. Calculate the mean anomaly for the year 2018 for Europe (over all pixels of the extent from #2) 
#    Compare this overall mean anomaly to the anomaly of the pixel which contains Marburg. 
#    Is the anomaly of Marburg lower or higher than the one for Europe? [2P]

#I had a problem with my pc ram. So there was a memory mistake because my pc can't handle so much data. I tried everything but it didn't work.
#So there will be no solution (if its needed) but the way for it. Maybe incorrect because I couldn't test it. I know there is a way to split data or use all ram for python but i didn't found it yet.
#I think maybe with numpy?
tab_new1_mean_annual = tab_new1.mean("time")
tab_new2_mean_2018 = tab_new2.mean("time")
anom_2018_annual = tab_new2_mean_2018 - tab_new1_mean_annual
anom_2018_annual_new = anom_2018_annual.sel(latitude= 50.81, longitude=8.77, method="nearest") #these are the coordinates for marburg

if anom_2018_annual_new > anom_2018_annual:
    print("The value of the anomaly in Marburg is higher than the value for Europe.")
else:
    print("The value of the anomaly in Europe is higher than the value for Marburg.")
        

# 5. Write the monthly anomalies from task 3 to a netcdf file with name "europe_anom_2018.nc" to the solution directory.
#    Write the monthly anomalies for Marburg to a csv file with name "marburg_anom_2018.csv" to the solution directory. [2P]

anom_2018.to_netcdf(output_dir / "europe_anom_2018.nc")
anom_2018_monthly_MR = anom_2018.sel(latitude= 50.81, longitude=8.77, method="nearest").to_dataframe()
anom_2018_monthly_MR.to_csv(output_dir / "marburg_anom_2018.csv")