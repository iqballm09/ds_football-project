# Data Science : Football Match Result Prediction
<img src="https://i.pinimg.com/originals/b4/90/05/b490053689e3026416d6417816f0a1fe.jpg" width="550" height="300" />

* Create model that can predict football match result (Win, Lose, Draw) based on half-time statistics.
* Scraped data over 2000 half-time match on top 6 football league in 2020/2021 season (Premier League, Serie A, La Liga, Bundesliga, Eredivisie, Ligue 1).
* dst

## Code and Resources Used
* Python Version: 3.9.7
* Packages: pandas, numpy, selenium
* dst

## Data Scraping
Scrape over 2000 match statistics half-time data from [flashscore.com](https://www.flashscore.com/ "flashscore.com") website using Selenium framework. For each match statistics, we got the following features:
* Half-time score
* Shots on goal
* Shots off goal
* Goal attempts
* Tackles
* Ball possession
* Blocked shots
* Offsides
* Yellow cards
* Red cards
* Corner kicks
* Free kicks
* Throw-in
* Dangerous attacks
* Goalkeeper saves
* Total passes
* Completed passes
* Fouls
* Attacks
* Full-time score

##	Data Cleaning
After scraping the data, this data needed to be cleaned up so that it was usable for modelling and analyze.
* Merged all match data from 6 football league
* Extracted stats value data for each stats categories
* Extracted categories / variable stats
* Created empty data dictionary for contain stats values with stats categories as keys
* Added all of stats data which had been extracted to dictionary
* Created dataframe from dictionary
* Removed symbols from half-time score and ball possession variables
* Saved datatable as csv format. 

