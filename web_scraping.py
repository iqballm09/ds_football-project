#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 22:00:49 2022

@author: iqballm09
"""

# Import libraries
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Set environment and driver
os.environ['PATH'] = "/usr/bin/"
driver1 = webdriver.Chrome()
driver1.get("https://www.flashscore.com/football/spain/laliga-2020-2021/results/")

# Find ids match results
elements = driver1.find_elements(By.XPATH, '//*[@id]')
ids = []
for element in elements:
    if element.get_attribute("id")[:4] == "g_1_":
        ids.append(element.get_attribute("id"))
        
# ids = ids[6:]


# Find matches
i = 0
matches = []
for id in ids[i:]:
    result = []
    # Get match score
    match = driver1.find_element(By.ID, id)
    match_score = match.text.split()
    # Enable cookies
    url_link = "https://www.flashscore.com/match/"+id[4:]+"/#/match-summary/match-statistics/1"
    driver2 = webdriver.Chrome()
    driver2.get(url_link)
    time.sleep(2)
    driver2.find_element(By.CSS_SELECTOR, "#onetrust-accept-btn-handler").click()
    # Get match statistic of half-time
    for row in driver2.find_elements(By.CLASS_NAME, "stat__row"):
        stats = row.find_element(By.CLASS_NAME, "stat__category")
        result.append(stats.text.split())
    # Add score result
    result.append([match_score[-2], "half-time", "score", match_score[-1]])
    result.append([match_score[-4], "full-time", "score", match_score[-3]])
    result.append([id])
    matches.append(result)
    i = i + 1
    print("Iterasi ke",i)

# Write to file
filename = "ligueone2020-2021.txt"
file = open(filename, "w")
for match in matches:
    file.write(str(match) + "\n")
file.close()