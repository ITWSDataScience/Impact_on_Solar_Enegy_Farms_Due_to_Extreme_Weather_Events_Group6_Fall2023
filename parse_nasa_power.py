"""
Created on Thu Nov 2 01:15:23 2023

@author: savidd
"""
import pandas as pd 
import matplotlib.pyplot as plt


def line_equation(x):
    return -4/5*x-57

def parse_file():
    df = pd.read_csv("POWER_Regional_Monthly_2013_2022.csv", header = 9)
        
    lat1 = 39 
    lon1 = -120

    lat2 = 35 
    lon2 = -115

    # mask_california = (df['LON'] <= lon1)  (df['LAT'] >= line_equation(df['LON']))

    # california_data = df[mask_california]

    filtered_df = df[(df['LON'] <= lon1) | ((df['LON'] > lon1) & (df['LON'] <= lon2) & (df['LAT'] < line_equation(df['LON'])))]

    return filtered_df

def average_coord_data():
    cali_df = parse_file()
    grouped_avg = cali_df.groupby(['LAT', 'LON']).mean(numeric_only=True).reset_index()
    one_point = grouped_avg.loc[(grouped_avg['LAT']==32.75) & (grouped_avg['LON']==-114.75)]
    return grouped_avg

    # latitudes = filtered_df['LAT']
    # longitudes = filtered_df['LON']

    # plt.scatter(longitudes, latitudes, s=10, c='blue', marker='o', alpha=0.5)
    # plt.title('Coordinate Plot')
    # plt.xlabel('Longitude')
    # plt.ylabel('Latitude')
    # plt.grid(True)
    # plt.show()

    # plt.savefig('coordinate_plot.png')


