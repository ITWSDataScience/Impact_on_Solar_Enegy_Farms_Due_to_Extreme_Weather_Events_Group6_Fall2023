# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 12:33:38 2023

@author: ghpan
"""
import pandas as pd 

#def parse(gen_csv = False):
df = pd.read_csv("NRI_Table_Counties_California.csv")
    
df = df[["COUNTY", "ALR_VALB", "EAL_VALB", "EAL_VALT", "RISK_VALUE", 
         "RISK_SCORE", "RISK_SPCTL", "EAL_SPCTL", "BUILDVALUE", 
         "AREA"]]

df.to_csv("NRI_OUT.csv", index = False)