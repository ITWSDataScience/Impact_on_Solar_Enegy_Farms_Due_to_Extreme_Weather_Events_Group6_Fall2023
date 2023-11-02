# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 12:05:49 2023

@author: ghpan
"""

import pandas as pd 

def parse(gen_csv = False):
    df = pd.read_csv("California_Power_Plants.csv")
    # Filter out Primary Energy Source that isn't sun
    df = df[df["PriEnergySource"] == "SUN"]
    # Filter Retired plants out
    df = df[df["Retired_Plant"] == 0]
    
    df = df.drop(columns = ["Retired_Plant", "OperatorCompanyID", "PriEnergySource", "Units"])
    
    df = df.reset_index(drop=True)
    if gen_csv:
        df.to_csv("cali_powerplant_out.csv", index = False)
    else:
        print("Parsed the data")

