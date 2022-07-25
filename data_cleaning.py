#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 14:48:33 2022

@author: iqballm09
"""

# Import libraries
import os
import re
import pandas as pd
import numpy as np

# Create class of data scraper
class DataScraper:
    def __init__(self, name_dir):
        self.dirname = name_dir
        self.raw_data = []
        self.unlist_data = []
        self.result = []
        self.final_cats = []
        self.data_dict = {}
        self.datatable = []
    
    def get_filedata(self):
        for filename in os.listdir(self.dirname):
            f = os.path.join(self.dirname, filename)
            if os.path.isfile(f):
                filedata = open(f, "r").readlines()
                for data in filedata:
                    self.raw_data.append(data)
                    
    def extract_rawdata(self):
        self.unlist_data = [data[15:-3].split("], [") for data in self.raw_data]
        for data in self.unlist_data:
            subresult2 = []
            for subdata in data:
                subresult1 = []
                for x in subdata.split(", "):
                    subresult1.append(x[1:-1])
                subresult2.append(subresult1)
            self.result.append(subresult2)
        
        len_result = [len(data) for data in self.result]
        print("Unique values:", set(len_result))
        
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
    
    def add_cats(self, list_cats, list_data):
        for cat in self.final_cats:
            if cat in list_cats:
                idx = list_cats.index(cat)
                self.data_dict[cat].append(list_data[idx])
            else:
                self.data_dict[cat].append(np.nan)
    
    def create_listcats(self):
        list_cats = []
        for stat_data in self.result:
            cats_result = DataScraper.create_cats(stat_data)
            for cat in cats_result:
                list_cats.append(cat)
        self.final_cats = list(set(list_cats))
        print("Final variables:", self.final_cats)
        
    def initialize_dict(finalCats):
        data_dict = {}
        for cat in finalCats:
            data_dict[cat] = []
        data_dict["match_id"] = []
        return data_dict
    
    def add_to_dict(self):
        # Define empty dict
        self.data_dict = DataScraper.initialize_dict(self.final_cats)
        
        # Extract match id
        unlist_id = [data.split(", [")[0].replace("[", "") for data in 
                     self.raw_data]
        
        for stat_data in self.result:
            list_data = []
            for data in stat_data:
                list_data.append(data[0] + " - " + data[-1])
            cats_result = DataScraper.create_cats(stat_data)
            
            # Add data to dict
            DataScraper.add_cats(self, cats_result, list_data)
        
        # Add match_id
        self.data_dict["match_id"] = unlist_id
        
    def create_datatable(self):
        # Define dataframe
        self.datatable = pd.DataFrame(self.data_dict)
        
        # Remove "(", ")", and "%"
        self.datatable['half-time_score'] = self.datatable['half-time_score'].apply(lambda x: \
                                                 x.replace("(","").replace(")",""))
        self.datatable['ball_possession'] = self.datatable['ball_possession'].apply(lambda x: \
                                                 x.replace("%","").replace("'",""))
    
        # Change order of cols in datatable
        self.datatable = self.datatable[['match_id','half-time_score', 'ball_possession', 'goal_attempts', 
                                         'shots_on_goal', 'shots_off_goal', 'dangerous_attacks',
                                         'blocked_shots', 'corner_kicks', 'fouls', 'yellow_cards',
                                         'red_cards', 'total_passes', 'completed_passes',
                                         'goalkeeper_saves', 'throw-in', 'offsides', 'free_kicks',
                                         'tackles', 'attacks', 'full-time_score']]
    
    def save_datatable(self):
        self.datatable.to_csv("halftime_finalstats1.csv", index=False)
    
# Run program
if __name__ == '__main__':
    dirname = "scraper_data" # directory location
    dataScraper = DataScraper(dirname)
    dataScraper.get_filedata()
    dataScraper.extract_rawdata()
    dataScraper.create_listcats()
    dataScraper.add_to_dict()
    dataScraper.create_datatable()
    dataScraper.save_datatable()
        

        
        
    
    
        