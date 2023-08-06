import src.main as rs
import matplotlib.pyplot as plt
import pandas as pd 
import ee

# Definitions

jan19 = '2019-01-01'
march19 = '2019-03-01'
may19 = '2019-05-01'

jan21 = '2021-01-01'

lat_n=-34.52
lat_s=-34.73
lon_w=-58.56
lon_e=-58.33

reds = [ee.Reducer.mean(), ee.Reducer.min()] # the spatial reducers we'll be using
names = ['NO2_trop_mean','NO2_trop_min'] # their names

arg_shapefile = "data/arg/departamento.shp" 

def test_time_series(start, end, roi):
    
    df = rs.time_series_df(roi,start,end,filename='raw.csv',reducers = reds, red_names = names)
    df_daily = rs.ts_dailydf(df, filename= 'daily.csv')
    df_weekly = rs.ts_weeklydf(df, filename= 'weekly.csv')
    df_monthly = rs.ts_monthlydf(df, filename= 'monthly.csv')

    return df, df_daily, df_weekly, df_monthly

def test_tseries_median(df):
    median_daily = rs.ts_dailydf(df, statistic = 'median')
    median_weekly = rs.ts_weeklydf(df, statistic = 'median')
    median_monthly = rs.ts_monthlydf(df, statistic = 'median')

    return median_daily, median_weekly, median_monthly

print("Create geometry of Buenos Aires")
ba_roi = rs.geometry_rectangle(lon_w,lat_s,lon_e,lat_n)

# Basics

print("Obtain dataframes with NO2 time series. Aggregate using mean")
df, df_d, df_w, df_m = test_time_series(march19, may19, ba_roi)

print("Show and save plots for these series")
fig, ax = rs.plot_series(df_d,show = True) #save with default name: series.png
rs.plot_series(df_w, filename = 'weekly.png', show = True)
rs.plot_series(df_m, filename = 'monthy.png', show = True)

print("Change title to matplotlib object and save again")
fig.suptitle("Daily series of tropospheric NO2")
fig.savefig('daily_again.png',bbox_inches='tight',dpi=500)

print("Recalculate NO2 time series, now using median to aggregate")
median_d, median_w, median_m = test_tseries_median(df)

print("Show or save plots for these series")
fig, ax = rs.plot_series(median_d,show = True) #show and save with default name: series.png
rs.plot_series(median_w, filename = 'median_weekly.png') #save, don't show
rs.plot_series(median_m, show = True, save = False) #show, don't save

print("Show autocorrelogram for daily series")
rs.plot_autocorr(df_d, lags = 22, show = True, save = False)

# Long case

print("Get series for 2019 and 2020")
long_df = rs.time_series_df(ba_roi,jan19,jan21,filename='long_raw.csv',reducers = reds, red_names = names)
long_monthly = rs.ts_monthlydf(long_df, filename= 'long_monthly.csv')

print("Load monthly series from csv and plot a bar plot comparing years")
df_monthly = pd.read_csv('long_monthly.csv')
rs.barplot_year_cmp(df_monthly, 2019, 2020, show = True) 

var = rs.interanual_variation(df_monthly, 2019, 2020, month_num = 4)
print("Interannual variation for april 2019-2020: ",var)

# Spatial data

print("Show and save plots for spatial distribution of NO2")
values, lon, lat = rs.space_data_meshgrid(ba_roi, jan19, may19, export = False)
map_fig, _ = rs.plot_map(values, lon, lat, arg_shapefile, show=True)
map_fig.suptitle("Concentrations of NO2 in Buenos Aires")
map_fig.savefig("map.png")

