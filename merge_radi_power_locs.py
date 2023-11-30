"""
Created on Thu Nov 9 01:15:23 2023

@author: savidd
"""
import pandas as pd 
import matplotlib.pyplot as plt
import parse_nasa_power

def merge_on_coord(df1, df2):
    merged_rows = []
    threshold = .2
    for index, row_df2 in df2.iterrows():
        x, y = row_df2['X'], row_df2['Y']

        # Check for proximity within the threshold
        close_rows_df1 = df1[(abs(df1['LON'] - x) < threshold) & (abs(df1['LAT'] - y) < threshold)]
        
        # Append the matching rows to the result
        for index_df1, row_df1 in close_rows_df1.iterrows():
            merged_row = {**row_df2, **row_df1.to_dict()}
            merged_rows.append(merged_row)

    # Create a new dataframe from the merged rows
    merged_df = pd.DataFrame(merged_rows)
    merged_df = merged_df.sort_values(by=['X','Y'])
    return merged_df

def combine_solar_plant_locations():
    radi_frame = parse_nasa_power.average_coord_data()
    power_frame = pd.read_csv('cali_powerplant_out.csv')
    # print(radi_frame)
    # print(power_frame)

    merged_df = merge_on_coord(radi_frame, power_frame)
    # print(merged_df)
    return merged_df

def combine_risk_index_by_county(combined_solar):
    combined_solar['COUNTY'] = combined_solar['County'].str.upper()
    risk_data = pd.read_csv('risk_data.csv')
    risk_data = risk_data.iloc[:, 1:]
    risk_data['COUNTY'] = risk_data['COUNTY'].str.upper()
    merged_df = pd.merge(combined_solar, risk_data, on='COUNTY', how='left')
    merged_df.drop(columns=['X', 'Y', 'OBJECTID', 'StartDate', 'YEAR', 'County'], inplace=True)
    merged_df.to_csv('risk_solar_locations_combined.csv')


df = combine_solar_plant_locations()
combine_risk_index_by_county(df)