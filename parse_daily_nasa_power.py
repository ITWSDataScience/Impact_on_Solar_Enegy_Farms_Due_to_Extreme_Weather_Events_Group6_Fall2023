"""
Created on Wed Dec 2 12:38:23 2023

@author: savidd
"""
import pandas as pd 
import matplotlib.pyplot as plt
import glob

def line_equation(x):
	return -4/5*x-57


def parse_files():
	file_pattern = "POWER_Regional_Daily*.csv"
	files_list = glob.glob(file_pattern)

	df = pd.concat([pd.read_csv(file, header=9) for file in files_list])

	df.reset_index(drop=True, inplace=True)
	lat1 = 39
	lon1 = -120
	lat2 = 35
	lon2 = -115
	filtered_df = df[(df['LON'] <= lon1) | ((df['LON'] > lon1) & (df['LON'] <= lon2) & (df['LAT'] < line_equation(df['LON'])))]
	return filtered_df

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
    radi_frame = parse_files()
    power_frame = pd.read_csv('cali_powerplant_out.csv')
    # print(radi_frame)
    # print(power_frame)

    merged_df = merge_on_coord(radi_frame, power_frame)
    # print(merged_df)
    return merged_df

def combine_disaster_by_county_date(combined_solar):
    combined_solar['COUNTY'] = combined_solar['County'].str.upper()
    combined_solar.drop(columns=['X', 'Y', 'OBJECTID', 'StartDate'], inplace=True)
    risk_data = pd.read_csv('risk_data.csv')
    risk_data = risk_data.iloc[:, 1:]
    risk_data['COUNTY'] = risk_data['COUNTY'].str.upper()
    print(combined_solar.columns)
    print(risk_data.columns)
    merged_date = pd.DataFrame()
    for index, row in risk_data.iterrows():
    	for date in row['DISASTER_DATE'].split(','):
    		parsed_date = pd.to_datetime(date).date()
    		print(parsed_date)
    		matches = combined_solar[(combined_solar['COUNTY']==row['COUNTY'])&(pd.to_datetime(combined_solar[['YEAR','MO','DY']]).dt.date==parsed_date)]
    		for match_index, match_row in matches.iterrows():
    			combined_row = match_row.to_dict()
    			combined_row.update(row.to_dict())
    			merged_data = merged_data.append(combined_row, ignore_index=True)

df = combine_solar_plant_locations()
combine_disaster_by_county_date(df)