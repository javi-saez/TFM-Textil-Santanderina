import pandas as pd
import openpyxl
import xlrd
import numpy as np
import glob
import datetime
from math import cos, sin, pi 

## we want no cientific notation numbers:
np.set_printoptions(suppress=True)

def df_family(product_family,list_directories):
    
    seasonability_1 = np.empty(0)
    seasonability_2 = np.empty(0)
    
    pmf = np.empty(0)
    empty_array = np.empty(0)
    
    trend = np.empty(0)
    number_weeks = range(1,49)
    
    first_week = np.arange(1,49)
    second_week = np.arange(9,17)
    third_week = np.arange(17,25)
    fourth_week = np.arange(25,32)

    first_week_february = np.arange(1,8)
    second_week_february = np.arange(8, 15)
    third_week_february = np.arange(15, 22)
    fourth_week_february = np.arange(22, 30)
    

    for year in list_directories:
        for data in year:
            ## we open each year and then each excel related to each month:
                df = pd.read_excel(data, engine='openpyxl')

                ## we filter the date info inside the fecha column:
                df['year'] = pd.DatetimeIndex(df['Fecha']).year
                df['month'] = pd.DatetimeIndex(df['Fecha']).month
                df['day'] = pd.DatetimeIndex(df['Fecha']).day

                ## we filter only the bill lines which are commercial invices (values 'F' of the 'TipoDoc' Column):
                df_f = df.loc[df['TipoDoc'].isin(['F'])]


                ## we filter for the first family of products:
                df_g = df_f.loc[df_f['GrupoArticulo'].isin([product_family])]

                if df['month'][0] == 2:

                        ## the amount billed for every week in february:
                        df_w1 = df_g.loc[df_g['day'].isin(first_week_february)]
                        df_w2 = df_g.loc[df_g['day'].isin(second_week_february)]
                        df_w3 = df_g.loc[df_g['day'].isin(third_week_february)]
                        df_w4 = df_g.loc[df_g['day'].isin(fourth_week_february)]

#                         ## we save the information of the month:
#                         dt_circ_base = (2/12)*2*pi # entre 0 y 2*pi
#                         features_dt_circ = [cos(dt_circ_base), sin(dt_circ_base)] # 2 valores, a rellenar en 2 columnas de features

                else:

                        ## the amount billed for every 
                        df_w1 = df_g.loc[df_g['day'].isin(first_week)]
                        df_w2 = df_g.loc[df_g['day'].isin(second_week)]
                        df_w3 = df_g.loc[df_g['day'].isin(third_week)]
                        df_w4 = df_g.loc[df_g['day'].isin(fourth_week)]

#                         ## we save the information of the month:
#                         dt_circ_base = (df['month'][0]/12)*2*pi # entre 0 y 2*pi
#                         features_dt_circ = [cos(dt_circ_base), sin(dt_circ_base)] # 2 valores, a rellenar en 2 columnas de features


                ## HERE WE STORE THE VALUES OF OUR COLUMNS:

                ## we generate for each total week the total billed quantity, by filtering the column:
                first_week_importe = df_w1['Importe'].sum()
                second_week_importe = df_w2['Importe'].sum()
                third_week_importe = df_w3['Importe'].sum()
                fourth_week_importe = df_w4['Importe'].sum()

                ## we store the last fourth arrays in one called fm (facturacion del mes, billed amount of the month):
                fm = np.array([first_week_importe,second_week_importe, third_week_importe,fourth_week_importe])

                ## we append to the general array the result of the fourth weeks of the loaded month:
                pmf = np.append(pmf, fm)

        ## we store the trend info (passage of time):
        ## we store the year:
        for week in number_weeks:
            y = df['year'][0]
            trd = y + (week - 1)/48

            ## then we store this trend number into an array:
            trend = np.append(trend, trd)
            
            ## we save the information of the month:
            dt_circ_base = (week/48)*2*pi # entre 0 y 2*pi
            features_dt_circ = [cos(dt_circ_base), sin(dt_circ_base)] # 2 valores, a rellenar en 2 columnas de features
            
            ## we store the info of the cos:
            seasonability_1 = np.append(seasonability_1, features_dt_circ[0])

            ## and the info  of the sin:
            seasonability_2 = np.append(seasonability_2, features_dt_circ[1])
                      
    ##here after the iterations are done we store the arrays generated:
    yTrain = pd.DataFrame({'target':pmf})
    
    xTrain = pd.DataFrame({'seasonability_circ_cos':seasonability_1,'seasonability_circ_sin':seasonability_2, 'time':trend, 'y_t-1':yTrain.target.shift(1),})
    return yTrain, xTrain

def predict_with_last_year(target, time_units_year):
    """
    Returns the last year of a temporal serie as a prediction for the next year.
    
        Parameters:
            target (array/list/pd.Serie): An array of (n,1) dimensions
            time_units_year (int): An integer to determine the number of units in which we divide each year (e.g 12 in the case of months)
        
        Returns:
            target_predicted(array): prediction for the future and unknow year
    """
    y = np.asarray(target)
    y = y.reshape(len(y),1)
    
    target_predicted = y[-time_units_year:]
    return target_predicted

def predict_with_ema(target, time_units_year, alpha):
    """
    Returns Exponential Moving Average for any single time segmentation of our predicted time serie.
    
        Parameters:
            target (array/list/pd.Serie): An array of (n,1) dimensions
            time_units_year (int): An integer to determine the number of units in which we divide each year (e.g 12 in the case of months)
            alpha (float): its value should be between 0 and 1, is the importance we give to our most recent observation, thus been (1-alpha) the importance to the rest of observations
        Returns:
            target_predicted(array): prediction for  of an unknow (next) year. Note that each of the 
    """
    y = np.asarray(target)
    y = y.reshape(len(y),1)
    
    ## to know the number of years we have in our training time serie:
    ## we change its type as integer for the future iterations:
    num_years = int(len(y)/time_units_year)
    
    ## we need to split our training target information in a different array for each year:
    y_divided = np.array_split(y,num_years)
    
    ## now we iterate the process of calculating the EMA for each time unit
    ## taking as references the same times in different years:
    target_predicted = np.empty(0)
    for time_unit_i in range(0, time_units_year):
        same_time_array = np.empty(0)
        for year_serie in range(0,num_years):
            same_time = y_divided[year_serie][time_unit_i]
            same_time_array = np.append(same_time_array,same_time)
        same_time_array = pd.Series(same_time_array)
        ema_unit_time = same_time_array.ewm(alpha=alpha, adjust=False).mean()[-1:]
        target_predicted = np.append(target_predicted, ema_unit_time)
        
    return target_predicted