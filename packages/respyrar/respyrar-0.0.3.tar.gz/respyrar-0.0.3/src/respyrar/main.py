import ee
import pandas as pd
import numpy as np
#import geopandas as gpd
#import shapefile #?
import isoweek 
import json
#from dateutil.relativedelta import relativedelta #?
import datetime
import matplotlib
import matplotlib.cm as mpl
import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs             
import cartopy.feature as cfeature           
import cartopy.io.shapereader as shapereader
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.feature.nightshade import Nightshade
from copy import deepcopy
from scipy.stats import pearsonr
import statsmodels.api as sm


def initialize():
    try:
        ee.Initialize()
    except Exception as e:
        ee.Authenticate()
        ee.Initialize()

initialize()

def get_collection(ini,fin, sat = 'COPERNICUS/S5P/OFFL/L3_NO2', column ='tropospheric_NO2_column_number_density'):
    collection=ee.ImageCollection(sat).select(column).filterDate(ini,fin)
    return collection

def compare_csv(filename1, filename2):
    t1 = open(filename1, 'r')
    t2 = open(filename2, 'r')
    fileone = t1.readlines()
    filetwo = t2.readlines()
    t1.close()
    t2.close()

    return (fileone == filetwo)


def create_reduce_region_function(geometry,
                                  reducer=ee.Reducer.mean(),
                                  scale=1000,
                                  crs='EPSG:4326',
                                  bestEffort=True,
                                  maxPixels=1e13,
                                  tileScale=4):

    def reduce_region_function(img):

        stat = img.reduceRegion(
            reducer=reducer,
            geometry=geometry,
            scale=scale,
            crs=crs,
            bestEffort=bestEffort,
            maxPixels=maxPixels,
            tileScale=tileScale)

        return ee.Feature(geometry, stat).set({'millis': img.date().millis()})
    return reduce_region_function

def fc_to_dict(fc):
    prop_names = fc.first().propertyNames()
    prop_lists = fc.reduceColumns(
        reducer=ee.Reducer.toList().repeat(prop_names.size()),
      selectors=prop_names).get('list')

    return ee.Dictionary.fromLists(prop_names, prop_lists)

# Function to add date variables to DataFrame.
def add_date_info(df):
    df['Timestamp'] = pd.to_datetime(df['millis'], unit='ms')
    df['Year'] = pd.DatetimeIndex(df['Timestamp']).year
    df['Month'] = pd.DatetimeIndex(df['Timestamp']).month
    df['Day'] = pd.DatetimeIndex(df['Timestamp']).day
    df['Weekday']=pd.DatetimeIndex(df['Timestamp']).weekday
    return df

def geometry_rectangle(lon_w,lat_s,lon_e,lat_n):
    return ee.Geometry.Rectangle([lon_w,lat_s,lon_e,lat_n],geodesic= False,proj='EPSG:4326')

""" coming soon
def geometry_polygon(filename):
    shape = gpd.read_file(filename)
    js = json.loads(shape.to_json())
    roi_fc = ee.FeatureCollection(js)
    roi = roi_fc.geometry()
    return roi
"""

def time_series_df(roi, start, end, filename = 'NO2trop_series.csv', reducers = [ee.Reducer.mean()], red_names = ['NO2_trop_mean'], collection = None):
    
    assert(len(reducers) == len(red_names))
    #satelite COPERNICUS, modo offline, elijo el no2 // para tiempor real elegir NRTI en vez de OFFL
    collection_name = 'COPERNICUS/S5P/OFFL/L3_NO2'
    #dentro de eso elijo la densidad de columna troposferica:
    variable  = 'tropospheric_NO2_column_number_density'
    var_name  = 'NO2_trop_mean'

    df = pd.DataFrame({"millis": []})

    if collection == None:
        collection_filter = get_collection(start,end)
    else:
        collection_filter = collection.filterDate(start,end)
    
    i=0
    for reducer in reducers:
        reduce_function = create_reduce_region_function(geometry=roi, reducer=reducer, scale=1113.2, crs='EPSG:4326')
        collection_fc = ee.FeatureCollection(collection_filter.map(reduce_function)).filter(ee.Filter.notNull(collection_filter.first().bandNames()))
        collection_dict=fc_to_dict(collection_fc).getInfo()
        
        new_df = pd.DataFrame(collection_dict)
        new_df = new_df.rename(columns={variable: red_names[i]}).drop(columns=['system:index'])
        df = pd.merge(df, new_df, on='millis', how='outer')
        i += 1 
    
    df = add_date_info(df)
    df = df.drop(columns=['millis'])
    df.to_csv(filename,index=False)
    return df

def ts_dailydf(df, filename='dailymean_df.csv', statistic = 'mean'):
    assert(statistic == 'mean' or statistic == 'median')
    if statistic == 'mean' :
        df_daily=df.groupby(['Year','Month','Day']).mean(numeric_only = True).reset_index()
    elif statistic == 'median':
        df_daily=df.groupby(['Year','Month','Day']).median(numeric_only = True).reset_index()
    df_daily_c=df.groupby(['Year','Month','Day']).count().reset_index()
    df_daily['N_obs']=df_daily_c[df.columns[0]]
    df_daily['Fecha_datetime']=pd.to_datetime(df_daily['Year'].astype(str)+'-'+df_daily['Month'].astype(str)+'-'+df_daily['Day'].astype(str),format='%Y-%m-%d')
    t=df_daily.Fecha_datetime.values
    dias_completos=pd.date_range(start=t[0], end=t[-1]).to_frame(name='Fecha_datetime')
    df_daily=dias_completos.merge(df_daily, how='left',on='Fecha_datetime')
    df_daily['Year']=df_daily['Fecha_datetime'].dt.year
    df_daily['Month']=df_daily['Fecha_datetime'].dt.month
    df_daily['Day']=df_daily['Fecha_datetime'].dt.day
    df_daily['Weekday']=df_daily['Fecha_datetime'].dt.weekday
    df_daily['N_obs']=df_daily['N_obs'].fillna(0).astype(int)
    df_daily.to_csv(filename,index=False)
    return df_daily

def ts_monthlydf(df, filename='monthlymean_df.csv', statistic = 'mean'):
    assert(statistic == 'mean' or statistic == 'median')
    df_daily=ts_dailydf(df, statistic = statistic)
    if statistic == 'mean' :
        df_monthly=df_daily.groupby(['Year','Month']).mean(numeric_only = True).reset_index()
    elif statistic == 'median':
        df_monthly=df_daily.groupby(['Year','Month']).median(numeric_only = True).reset_index()
    df_monthly_c=df_daily.groupby(['Year','Month']).count().reset_index()
    df_monthly['Fecha_datetime']=pd.to_datetime(df_monthly['Year'].astype(str)+'-'+df_monthly['Month'].astype(str),format='%Y-%m')
    df_monthly.drop(columns=['Day','Weekday','N_obs'],inplace=True)
    df_monthly['N_days']=df_monthly_c[df.columns[0]]
    df_monthly.to_csv(filename,index=False)
    return df_monthly

def ts_weeklydf(df, filename='weeklymean_df.csv', statistic = 'mean'):
    assert(statistic == 'mean' or statistic == 'median')
    df_daily=ts_dailydf(df, statistic = statistic)
    #retrocedo tantos días según el día de la semana que sea
    df_daily['Fecha_datetime']= df_daily['Fecha_datetime'] - df_daily['Weekday'].apply(lambda x : datetime.timedelta(days=x))
    #df_daily['WeekOfYear']=[isoweek.Week.withdate(d) for d in day]
    #df_daily['WeekOfYear']=pd.DatetimeIndex(df_daily['Fecha_datetime']).week
    df_daily['WeekOfYear']=pd.Index(pd.DatetimeIndex(df_daily['Fecha_datetime']).isocalendar().week)
    if statistic == 'mean' :
        df_weekly=df_daily.groupby(['WeekOfYear','Fecha_datetime']).mean(numeric_only = True).reset_index()
    if statistic == 'median':
        df_weekly=df_daily.groupby(['WeekOfYear','Fecha_datetime']).median(numeric_only = True).reset_index()
    df_weekly_c=df_daily.groupby(['WeekOfYear']).count().reset_index()
    df_weekly['N_days']=df_weekly_c[df.columns[0]].astype(int)
    #df_weekly['Fecha_datetime']=[isoweek.Week.monday(s) for s in df_weekly.WeekOfYear.values]
    #df_weekly['Fecha_datetime']=df_weekly['WeekOfYear'].apply(lambda x : x+1)
    df_weekly.drop(columns=['Year','Month','Day','Weekday','N_obs'],inplace=True)
    df_weekly.to_csv(filename,index=False)
    return df_weekly


def space_data_meshgrid(roi, start, end, collection = None, statistic = 'mean', export = False):

    if collection == None:
        collection= get_collection(start,end)
    else:
        collection = collection.filterDate(start,end)
    
    if statistic == 'mean': 
        collection_img=collection.mean().setDefaultProjection(collection.first().projection())
    elif statistic == 'median':
        collection_img=collection.median().setDefaultProjection(collection.first().projection())
    else:
        print("Error: statistic not valid")

    if export:
        task = ee.batch.Export.image.toDrive(collection_img.toFloat(), 
                                              description=start,
                                              folder='NO2',
                                              fileNamePrefix= "NO2_"+start,
                                              region = roi,
                                              #dimensions = (256,256), ##ESTA BIEN? 
                                              fileFormat = 'GeoTIFF',
                                              maxPixels = 1e10) ##ESTA BIEN?
        task.start()


    latlon=ee.Image.pixelLonLat().addBands(collection_img)
    latlon_new = latlon.reduceRegion(reducer=ee.Reducer.toList(), geometry=roi, maxPixels=1e13,scale=1113.2,bestEffort = True)
    
    no2 = np.array((ee.Array(latlon_new.get('tropospheric_NO2_column_number_density')).getInfo()))
    lats = np.array((ee.Array(latlon_new.get("latitude")).getInfo()))
    lons = np.array((ee.Array(latlon_new.get("longitude")).getInfo()))  

    ##reshape para que quede tres matrices tipo meshgrid
    uniqueLats = np.unique(lats)
    uniqueLons = np.unique(lons)
    ncols = len(uniqueLons)    
    nrows = len(uniqueLats)

    no2=no2.reshape(nrows,ncols)
    LATS=lats.reshape(nrows,ncols)
    LONS=lons.reshape(nrows,ncols)

    return no2, LATS, LONS


def interanual_variation(df_m, year1, year2, month_num, column = 'NO2_trop_mean'):

    month_idx = month_num-1 
    no2_year1 = df_m[df_m.Year==year1][column].values
    no2_year2 = df_m[df_m.Year==year2][column].values
    
    var =np.round(100*(no2_year2[month_idx]-no2_year1[month_idx])/no2_year1[month_idx],decimals=2)
    return var

# Figures

def plot_map(no2, lats, lons, shapefile, title = 'Concentración media de NO2 troposférico (mol/m2)', filename = 'entero.png', width = 8, height = 6, font_size = 15, save = True, show = False):

    data = shapereader.Reader(shapefile)

    vmax=np.max(no2)

    ##colores
    cmap=mpl.get_cmap('seismic',100)  

    fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()},figsize=(width,height))

    ax.add_feature(cartopy.feature.COASTLINE)
    ax.add_feature(cartopy.feature.BORDERS)
    ax.add_geometries(data.geometries(), crs=ccrs.Geodetic(), edgecolor='k', facecolor='none')
    delta = 0
    ax.set_extent([np.min(lons)-delta, np.max(lons)+delta, np.min(lats)-delta, np.max(lats)+delta])
    cs=ax.pcolormesh(lons,lats,no2,vmin=0,vmax=vmax, cmap=cmap)
    
    raw_fig = deepcopy(fig) 
    raw_ax = deepcopy(ax)
    
    #fig.subplots_adjust(top=0.89,right=0.87,wspace=0.05, hspace=0.07)

    fig.suptitle(title,fontsize=font_size)

    #color bar
    cbar_ax = fig.add_axes([0.88, 0.15, 0.02, 0.7])
    fmt = matplotlib.ticker.ScalarFormatter(useMathText=True)
    fmt.set_powerlimits((0, 0))
    fig.colorbar(cs, cax=cbar_ax,ticks=np.linspace(0,vmax,10),format=fmt)
    
    plt.close(raw_fig)
    plt.close(plt.figure(3))

    if save:
        fig.savefig(filename,dpi=500)   
    if show:
        plt.show()
    return raw_fig, raw_ax

# date format: YYYY-MM-DD
def plot_series(df, start = pd.Timestamp.min, end = pd.Timestamp.max, column = 'NO2_trop_mean', filename = 'series.png', width = 15, height = 4, show = False, save = True):

    gas = 'NO2_trop'
    column = 'NO2_trop_mean'
    gasname = 'NO2 troposferico'

    titulo = 'Serie de ' + gasname

    rango=np.logical_and(df['Fecha_datetime']>= start,df['Fecha_datetime']<=end)
    df=df[rango]
    df=df.sort_values(by = 'Fecha_datetime')

    figsize=(width,height)
    plt.close("all")
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(df.Fecha_datetime,df[column],'ro:')
    fig.suptitle(titulo)
    ax.grid(axis='y',alpha=0.4)
    plt.ylabel(gasname+ ' (mol/m2)')
    
    if save:
        fig.savefig(filename,bbox_inches='tight',dpi=500)
    if show:
        plt.show()
    return fig,ax


def plot_autocorr(df, lags, alpha = 0.01, width = 30, height=5, filename = 'autocorrelogram.png', column = 'NO2_trop_mean', show = False, save = True):

    titulo = 'Autocorrelograma de la serie diaria'
    df_autocor=df.loc[:,['Fecha_datetime','NO2_trop_mean']]

    for i in range(lags+1):
        df_autocor['lag_'+str(i)]=df_autocor[column].shift(i)

    figsize=(width,height)
    plt.close("all")
    fig, ax = plt.subplots(figsize=figsize)
    sm.graphics.tsa.plot_acf(df_autocor[column], ax=ax, lags=lags,missing='conservative')
    #ax.bar(np.arange(1,lags+1),rho[1:],color=color_no_sig,edgecolor='black')
    #ax.bar(np.arange(1,lags+1),rhoenmascarado[1:],color=color_significativo,edgecolor=color_significativo)
    ax.grid(color='black',alpha=0.4)
    ax.set_xlabel('Lags (dias)')
    ax.set_title(titulo)

    if save:
        fig.savefig(filename,bbox_inches='tight',dpi=500)
    if show:
        plt.show()
    return fig,ax

#df_m un df agrupado por mes, que contiene datos de (al menos) ambos años 
def barplot_year_cmp(df_m, year1, year2, width = 10, height=4, column = 'NO2_trop_mean', filename='compared_series.png', show = False, save = True):

    col_year1 = column+str(year1)
    col_year2 = column+str(year2)

    no2_year1 = df_m[df_m.Year==year1].rename(columns = {column : col_year1})
    no2_year2 = df_m[df_m.Year==year2].rename(columns = {column : col_year2})

    df_bar = pd.merge(no2_year1, no2_year2, on = 'Month', how = 'outer')[['Month',col_year1,col_year2]]
    df_bar = df_bar.set_index('Month')  
    
    barWidth = 0.35
    figsize=(width,height)
    fig, ax = plt.subplots(figsize=figsize)
    ax = plt.bar(no2_year1['Month'], no2_year1[col_year1], width = barWidth, color= 'tab:blue', label = col_year1)
    ax = plt.bar(no2_year2['Month']+barWidth, no2_year2[col_year2], width = barWidth, color= 'tab:orange', label = col_year2)
    plt.legend()
    plt.grid(axis='y',alpha=0.5)


    if save:
        fig.savefig(filename,bbox_inches='tight',dpi=500)
    if show:
        plt.show()
    return fig,ax

