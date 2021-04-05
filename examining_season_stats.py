
# import math
# import statistics
# import collections
import ast
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request


#constants
script_directory = str(os.path.dirname(os.path.realpath(__file__)))
file_name = "league_stats_avgs_savefile.txt"
path_to_file = script_directory + '\\' + file_name
universalURL = 'https://afltables.com/afl/stats/yearly.html'
year_started = 1965
this_season = 2021
teams_in_comp = []
finals_cutoff = []
teams = {}
colours = {
    "Fitzroy":"Grey", 
    "Gold Coast":"orangered", 
    "Geelong":"royalblue", 
    "Essendon":"red", 
    "Carlton":"navy", 
    "Collingwood":"black", 
    "Melbourne":"lime", 
    "Hawthorn":"brown", 
    "Fitzroy":"grey", 
    "St Kilda":"crimson", 
    "Richmond":"yellow", 
    "North Melbourne":"blue", 
    "Western Bulldogs":"green", 
    "Fremantle":"purple", 
    "Greater Western Sydney":"orange", 
    "Brisbane Lions": "orangered", 
    "Port Adelaide":"cyan", 
    "West Coast":"darkgoldenrod", 
    "Sydney":"deeppink", 
    "Adelaide":"royalblue",
    "Brisbane Bears": "green"
    } #ugh takes so long to write out
running_colours = []
for i in teams:
    running_colours.append(colours[i])

def getURL(url):
    stream = urllib.request.urlopen(url)
    text = stream.read().decode('utf-8')
    stream.close()
    return text

class Club(object):
    def __init__(self, name, abbreviation):
        self._name = name
        self._abbreviation = abbreviation
        self._colour = colours[name]
        self._stats = {}

Richmond = Club("Richmond", "RI")
WC = Club("West Coast", "WC")
GC = Club("Gold Coast", "GC")
Brisbane = Club("Brisbane Lions", "BL")
Bears = Club("Brisbane Bears", "BB")
STK = Club("St Kilda", "SK")
Fremantle = Club("Fremantle", "FR")
Collingwood = Club("Collingwood", "CW")
Melbourne = Club("Melbourne", "ME")
Carlton = Club("Carlton", "CA")
Essendon = Club("Essendon", "ES")
Hawthorn = Club("Hawthorn", "HW")
Adelaide = Club("Adelaide", "AD")
PA = Club("Port Adelaide", "PA")
Sydney = Club("Sydney", "SY")
GWS = Club("Greater Western Sydney", "GW")
NM = Club("North Melbourne", "NM")
WB = Club("Western Bulldogs", "WB")
Geelong = Club("Geelong", "GE")
Fitzroy = Club("Fitzroy", "FI")

stats_key = {
    "K":"Kicks", 
    "D":"Disposals", 
    "M":"Marks",
    "GA":"Goal Assists", 
    "HB":"Handballs", 
    "G":"Goals", 
    "B":"Behinds", 
    "HO":"Hit Outs", 
    "T":"Tackles", 
    "I":"Inside 50s", 
    "R":"Rebounds", 
    "CL":"Clearances", 
    "CG":"Clangers", 
    "FF":"Frees", 
    "FA":"Frees Against", 
    "CM":"Contested Marks", 
    "MI":"Marks Inside 50", 
    "1%":"One Percenters", 
    "BO":"Bounces", 
    "GA":"Goal Assists", 
    "UP":"Uncontested Possessions", 
    "CP":"Contested Possessions"
    }

clubs = {
    "Richmond": Richmond,
    "West Coast": WC,
    "Gold Coast": GC,
    "Brisbane Lions": Brisbane,
    "St Kilda": STK,
    "Fremantle": Fremantle,
    "Collingwood": Collingwood,
    "Melbourne": Melbourne,
    "Carlton": Carlton,
    "Essendon": Essendon,
    "North Melbourne": NM,
    "Kangaroos": NM,
    "Footscray": WB,
    "Brisbane Bears": Bears,
    "Fitzroy": Fitzroy,
    "Hawthorn": Hawthorn,
    "Adelaide": Adelaide,
    "Port Adelaide": PA,
    "Sydney": Sydney,
    "Greater Western Sydney": GWS,
    "Western Bulldogs": WB,
    "Geelong": Geelong
    }
keys = [i for i in clubs.keys()]
for i in keys:
    clubs[clubs[i]._abbreviation] = clubs[i]
    del clubs[i]
ordered_clubs = ['AD', 'BB', 'BL', 'CA', 'CW', 'ES', 'FI', 'FR', 'GE', 'GC', 'GW', 'HW', 'ME', 'NM', 'PA', 'RI', 'SK', 'SY', 'WC', 'WB']#sorted(clubs.keys())
# current_clubs = set(clubs.values())
# current_clubs.remove(Fitzroy)

#"""
with open(path_to_file, "r") as f:
    stored_info = ast.literal_eval(f.read())
#MAIN:
#"""#RETRIEVE DATA
"""
stored_info = {}
stored_info["info"] = getURL(universalURL)
with open(path_to_file, "w") as f:
    f.write(str(stored_info))
#"""

print("Converting raw data:")
#Convert data to searchable format
text = stored_info["info"]
soup = BeautifulSoup(text, features="lxml")
tables = soup.findChildren('table')
print("done.")
print("")

print("Initialising:")
#Initialise everything
years = range(1965, 1965 + len(tables[1].findAll('tr')) - 3)

year_by_year_master_averages = {}

master_average_rows = tables[2].findAll('tr')[1:-1]
for ea_stat in master_average_rows[0].findAll('th')[1:]:
    year_by_year_master_averages[stats_key[ea_stat.text.strip()]] = []
year_by_year_master_averages["Disposals"] = []
year_by_year_master_averages["(avg_goals*6+avg_behinds)"] = []

for ea_stat in year_by_year_master_averages:
    for ea_club in ordered_clubs:
        clubs[ea_club]._stats[ea_stat] = []

for ea_club in ordered_clubs:
    clubs[ea_club]._stats["Disposals"] = []
    clubs[ea_club]._stats["(avg_goals*6+avg_behinds)"] = []

#Get comp avg year by year
for ea_row in master_average_rows[1:]:
    columns = ea_row.findAll('td')[1:]
    for idx, key in enumerate(year_by_year_master_averages):
        if key == "Disposals" or key == "(avg_goals*6+avg_behinds)":
            continue
        new_stat = columns[idx].text.strip()
        if new_stat:
            adjust = float(new_stat)
            if int(ea_row.find('td').text.strip()) == 2020:
                adjust *= 1.25
            year_by_year_master_averages[key].append(adjust)
    year_by_year_master_averages["Disposals"].append(year_by_year_master_averages["Kicks"][-1] + year_by_year_master_averages["Handballs"][-1])
    year_by_year_master_averages["(avg_goals*6+avg_behinds)"].append(year_by_year_master_averages["Goals"][-1] * 6 + year_by_year_master_averages["Behinds"][-1])
print("done.")
print("")

#Now go through ea stat avg for ea team
print("Converting data:")
for table in tables[3:]:
    rows = table.findAll('tr')
    stat = rows[0].text.split(" - ")[0].strip()
    #print(rows)
    for row in rows[2:]:
        columns = row.findAll('td')[1:]
        for idx, ea_club in enumerate(ordered_clubs):
            new_stat = columns[idx].text.strip()
            if new_stat:
                adjust = float(new_stat)
                if int(row.find('td').text.strip()) == 2020:
                    adjust *= 1.25
                clubs[ea_club]._stats[stat].append(adjust)
    print("...." + stat + " done.")
stat = "(avg_goals*6+avg_behinds)"
for ea_club in ordered_clubs:
    for idx in range(len(clubs[ea_club]._stats["Goals"])):
        clubs[ea_club]._stats[stat].append(clubs[ea_club]._stats["Goals"][idx] * 6 + clubs[ea_club]._stats["Behinds"][idx])
print("...." + stat + " done.")
print("Finally all done. Data now manipulatable/graphable.")
print("")

teams_to_analyse = [i for i in ordered_clubs if (i != "BB" and i != "FI")]#["SY", "GE", "ES"]

print("Drawing graphs for set teams (" + str(teams_to_analyse) + ") v league avgs:")
for stat in year_by_year_master_averages:
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xticks([i for i in range(1960, (years[-1] + (years[-1] % 10) + 10), 10)])
    ax.minorticks_on()
    ax.grid(which='minor')
    ax.grid(which='major', color="black")
    # avg = 5
    # moving_average = [round(i, 2) for i in pd.DataFrame(year_by_year_master_averages[stat]).rolling(avg).mean()[0].tolist()[avg - 1:]]
    # start = math.floor((avg - 1) / 2)
    # stop = len(x) - start
    # ax.plot(x[start:stop], moving_average, color='brown', label="Rolling " + str(avg) + " year league avg")#, where="post"
    for set_team in teams_to_analyse:
        ax.plot(years[len(years) - len(clubs[set_team]._stats[stat]):], clubs[set_team]._stats[stat], c=clubs[set_team]._colour, label=clubs[set_team]._name)#, where="post"
        ax.scatter(years[len(years) - len(clubs[set_team]._stats[stat]):], clubs[set_team]._stats[stat], c=clubs[set_team]._colour)
    x = years[len(years) - len(year_by_year_master_averages[stat]):]
    ax.plot(x, year_by_year_master_averages[stat], ls="--", c="k", label="League Avg")#, where="post"
    ax.scatter(x, year_by_year_master_averages[stat], c="k")
    plt.legend()
    plt.title("Avg " + stat + " per game")

print("done.")
print("")
print("Thank you afltables.com")
print("")
print("Displaying graphs for you now:")
plt.show()
print("")
print("All graphs closed. See you later.")