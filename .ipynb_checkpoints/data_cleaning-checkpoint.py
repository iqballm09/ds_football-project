#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 22:30:11 2022

@author: iqballm09
"""

# Import libraries
import os
import re
import pandas as pd
import numpy as np

# Import scraped data
directory = "scraper_data" # directory location

raw_data = []
for filename in os.listdir(directory) :
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        # print(f)
        filedata = open(f, "r").readlines()
        for data in filedata: raw_data.append(data)
        
# Extract match stats in raw data
unlist_data = [data[15:-3].split("], [") for data in raw_data]

result = []
for data in unlist_data:
    subresult2 = []
    for subdata in data:
        subresult1 = []
        for x in subdata.split(", "):
            subresult1.append(x[1:-1])
        subresult2.append(subresult1)
    result.append(subresult2)
    
# Find length of data
len_result = [len(data) for data in result]
print("Unique values:", set(len_result))

# Find min and max stat categories
min_stat_cat = [data for data in result if len(data) == 14]
max_stat_cat = [data for data in result if len(data) == 19]

# Find stat categories
def create_cats(list_vals):
    full_cats = []
    for val in list_vals:
        z = ""
        if len(val[1:-1]) > 1:
            for subval in val[1:-2]:
                z += subval.lower()
                z += "_"
            z += val[-2].lower()
        else:
            z += val[1:-1][0].lower()
        full_cats.append(z)
    return full_cats

def add_cats(dict_data, list_cats, list_data, final_cats):
    for cat in final_cats:
        if cat in list_cats:
            idx = list_cats.index(cat)
            dict_data[cat].append(list_data[idx])
        else:
            dict_data[cat].append(np.nan)
    return dict_data

# Create list of categories
list_cats = []
for stat_data in result:
    cats_result = create_cats(stat_data)
    for cat in cats_result:
        list_cats.append(cat)
final_cats = list(set(list_cats))
print("Final variables:", final_cats)

# Initialize empty dictionary
data_dict = {}
for cat in final_cats:
    data_dict[cat] = []
data_dict["match_id"] = []

# Extract match id
unlist_id = [data.split(", [")[0].replace("[","") for data in raw_data]

# Add all of data to dict
for stat_data in result:
    list_data = []
    for data in stat_data:
        list_data.append(data[0] + " - " + data[-1])
    cats_result = create_cats(stat_data)
    
    # Add data to dictionary
    data_dict = add_cats(data_dict, cats_result, list_data, final_cats)

# Add match_id
data_dict["match_id"] = unlist_id

# Create datatable from dict
datatable = pd.DataFrame(data_dict)

# Remove "(", ")", and "%"
datatable['half-time_score'] = datatable['half-time_score'].apply(lambda x: \
                                         x.replace("(","").replace(")",""))
datatable['ball_possession'] = datatable['ball_possession'].apply(lambda x: \
                                         x.replace("%","").replace("'",""))

# Change order of cols in datatable
datatable = datatable[['match_id','half-time_score', 'ball_possession', 'goal_attempts', 
                       'shots_on_goal', 'shots_off_goal', 'dangerous_attacks',
                       'blocked_shots', 'corner_kicks', 'fouls', 'yellow_cards',
                       'red_cards', 'total_passes', 'completed_passes',
                       'goalkeeper_saves', 'throw-in', 'offsides', 'free_kicks',
                       'tackles', 'attacks', 'full-time_score']]

# Save datatable to csv format
datatable.to_csv("halftime_finalstats.csv", index=False)
