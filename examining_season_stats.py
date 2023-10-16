import math
import statistics
import collections
import ast
import os
import matplotlib.pyplot as plt
# import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request


#constants
script_directory = str(os.path.dirname(os.path.realpath(__file__)))
file_name = "league_stats_avgs_savefile.txt"
path_to_file = script_directory + '\\' + file_name
file_name2 = "examinning_in_season_stats.txt"
path_to_second_file = script_directory + '\\' + file_name2
universalURL = 'https://afltables.com/afl/stats/yearly.html'
rdsURL = "https://afltables.com/afl/stats/teams/{}/{}_gbg.html"
year_started = 1965
this_season = 2021

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
    "Brisbane Lions": "olive", 
    "Port Adelaide":"cyan", 
    "West Coast":"darkgoldenrod", 
    "Sydney":"deeppink", 
    "Adelaide":"darkOrchid",
    "Brisbane Bears": "green"
    } #ugh takes so long to write out

def getURL(url):
    stream = urllib.request.urlopen(url)
    text = stream.read().decode('utf-8')
    stream.close()
    return text

class Club(object):
    def __init__(self, name, abbreviation, halfway_abbreviation, year_entered_comp):
        self._name = name
        self._abbreviation = abbreviation
        self._halfway_abbreviation = halfway_abbreviation
        self._colour = colours[name]
        self._year_entered_comp = year_entered_comp
        self._stats = {}

class Match(object):
    def __init__(self, away_team, home_team_score, away_team_score, venue=None):
        self._venue = venue
        self._home_team = home_team
        self._away_team = away_team
        self._home_team_score = home_team_score
        self._away_team_score = away_team_score
        self._margin = abs(home_team_score - away_team_score)
        self._winner = "draw"
        if self._margin > 0:
            self._winner = self._home_team 
        elif self._margin < 0:
            self._winner = self._away_team

Richmond = Club("Richmond", "RI", "richmond", 1950)
WC = Club("West Coast", "WC", "westcoast", 1987)
GC = Club("Gold Coast", "GC", "goldcoast", 2011)
Brisbane = Club("Brisbane Lions", "BL", "brisbanel", 1997)
Bears = Club("Brisbane Bears", "BB", "brisbaneb", 1987)
STK = Club("St Kilda", "SK", "stkilda", 1950)
Fremantle = Club("Fremantle", "FR", "fremantle", 1995)
Collingwood = Club("Collingwood", "CW", "collingwood", 1950)
Melbourne = Club("Melbourne", "ME", "melbourne", 1950)
Carlton = Club("Carlton", "CA", "carlton", 1950)
Essendon = Club("Essendon", "ES", "essendon", 1950)
Hawthorn = Club("Hawthorn", "HW", "hawthorn", 1950)
Adelaide = Club("Adelaide", "AD", "adelaide", 1991)
PA = Club("Port Adelaide", "PA", "padelaide", 1997)
Sydney = Club("Sydney", "SY", "swans", 1982)
GWS = Club("Greater Western Sydney", "GW", "gws", 2012)
NM = Club("North Melbourne", "NM", "kangaroos", 1950)
WB = Club("Western Bulldogs", "WB", "bullldogs", 1950)
Geelong = Club("Geelong", "GE", "geelong", 1950)
Fitzroy = Club("Fitzroy", "FI", "fitzroy", 1950)

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

stats_key = {
    "K":"Kicks",
    "D":"Disposals",
    "M":"Marks",
    "HB":"Handballs",
    "G":"Goals",
    "B":"Behinds",
    "HO":"Hit Outs",
    "T":"Tackles",
    "R":"Rebounds",
    "I":"Inside 50s",
    "CL":"Clearances",
    "CG":"Clangers",
    "FF":"Frees",
    "FA":"Frees Against",
    "CP":"Contested Possessions",
    "UP":"Uncontested Possessions",
    "CM":"Contested Marks",
    "MI":"Marks Inside 50",
    "1%":"One Percenters",
    "BO":"Bounces",
    "GA":"Goal Assists"
    }

ordered_clubs = [
    'Adelaide',
    'Brisbane Bears',
    'Brisbane Lions',
    'Carlton',
    'Collingwood',
    'Essendon',
    'Fitzroy',
    'Fremantle',
    'Geelong',
    'Gold Coast',
    'Greater Western Sydney',
    'Hawthorn',
    'Melbourne',
    'North Melbourne',
    'Port Adelaide',
    'Richmond',
    'St Kilda',
    'Sydney',
    'West Coast',
    'Western Bulldogs'
    ]

#MAIN:
#Initialise everything
years = range(year_started, this_season + 1)#year_started + len(tables[1].findAll('tr')) - 3

DRAWING_ROUNDS_GRAPH = False

if DRAWING_ROUNDS_GRAPH:
    #"""#RETRIEVE DATA
    with open(path_to_second_file, "r") as f:
        new_stored_info = ast.literal_eval(f.read())
    #"""
    '''
    for year in years:
        #"""
        # if new_stored_info.get(year, "nope") != "nope":
        #     continue
        if year == this_season: 
            new_stored_info[year] = {}
            for club_name in clubs:
                club = clubs[club_name]
                if club._year_entered_comp > year or (year >= 1997 and (club == Bears or club == Fitzroy)):
                    continue
                new_stored_info[year][club_name] = {}
                url = rdsURL.format(club._halfway_abbreviation, year)
                print("")
                print("Just finished processing:", url)
                raw_data = getURL(url)
                soup = BeautifulSoup(raw_data, features="lxml")
                tables = soup.findChildren('table')
                only_need_calculate_this_once = True
                for table in tables[1:]:
                    rows = table.findAll('tr')
                    stat = rows[0].text.strip()
                    if year > 2000 and (stat == "% Played" or stat == "Subs"):
                        continue
                    if only_need_calculate_this_once:
                        rounds = [rd.text.strip() for rd in rows[1].findAll('th')[1:-1]]
                        new_stored_info[year][club_name]["rounds"] = rounds
                    stat_by_round = [float(sbr.text.strip()) for sbr in rows[-2].findAll('th')[1:-1]]
                    if only_need_calculate_this_once:
                        links_to_matches = ["https://afltables.com/afl/stats/games/" + ltm['href'][12:] for ltm in rows[-1].findAll('a')]
                        margins = []
                        for link in links_to_matches:
                            raw_data2 = getURL(link)
                            soup2 = BeautifulSoup(raw_data2, features="lxml")
                            tables2 = soup2.findChildren('table')
                            rows2 = tables2[0].findAll('tr')
                            home = rows2[1].findAll('td')
                            away = rows2[2].findAll('td')
                            home_team = home[0].text
                            home_score = int(home[-1].text.split('.')[-1])
                            away_score = int(away[-1].text.split('.')[-1])
                            margin = home_score - away_score if home_team == club_name else away_score - home_score
                            margins.append(margin)
                        new_stored_info[year][club_name]["margins"] = margins
                        only_need_calculate_this_once = False
                    new_stored_info[year][club_name][stat] = stat_by_round
        #"""
        """
        master_rounds = []
        for j in new_stored_info[year]:
            if j == "master_round" or j == "averages":
                continue
            master_rounds.append(new_stored_info[year][j]["rounds"])
        this_years_round = []
        for counter in range(max([len(i) for i in master_rounds]) + 1):
            actual_round = "Z"
            for rounds_set in master_rounds:
                if counter >= len(rounds_set):
                    continue
                elif actual_round == "Z":
                    actual_round = rounds_set[counter]
                    continue
                my_round = rounds_set[counter]
                if my_round == actual_round:
                    continue
                if my_round[0] == "R":
                    if actual_round[0] != "R":
                        actual_round = my_round
                    else:
                        actual_round = min(my_round, actual_round)            
                elif my_round[0] == "Q":
                    print("")
                    print("")
                    print(master_rounds)
                    if actual_round[0] == "R":
                        continue
                    if actual_round[0] == "E":
                        this_years_round.append(actual_round)
                    actual_round = my_round
                elif my_round[0] == "E":
                    if actual_round[0] == "Q" and this_years_round[-1][0] != "E" and actual_round[0] != "E":
                        this_years_round.append(my_round)
                    elif actual_round[0] == "S":
                        actual_round = my_round
                elif my_round[0] == "S":
                    if actual_round[0] == "R" or actual_round[0] == "Q" or actual_round[0] == "E" or actual_round[-1][0] == "S":
                        continue
                    actual_round = my_round
                elif my_round[0] == "P" and (actual_round[0] == "G" or actual_round[-1][0] == "S"):
                    actual_round = my_round
                elif my_round[0] == "G" and actual_round[0] == "P":
                    continue
                #else:
                #    actual_round = my_round
            if actual_round == "Z":
                continue
            this_years_round.append(actual_round)
        """
        this_years_round = []
        if year < 1968:
            this_years_round = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10', 'R11', 'R12', 'R13', 'R14', 'R15', 'R16', 'R17', 'R18', 'SF', 'PF', 'GF']
        elif year < 1970:
            this_years_round = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10', 'R11', 'R12', 'R13', 'R14', 'R15', 'R16', 'R17', 'R18', 'R19', 'R20', 'SF', 'PF', 'GF']
        elif year < 1972:
            this_years_round = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10', 'R11', 'R12', 'R13', 'R14', 'R15', 'R16', 'R17', 'R18', 'R19', 'R20', 'R21', 'R22', 'SF', 'PF', 'GF']
        elif year < 2011:
            this_years_round = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10', 'R11', 'R12', 'R13', 'R14', 'R15', 'R16', 'R17', 'R18', 'R19', 'R20', 'R21', 'R22', 'EF', 'QF', 'SF', 'PF', 'GF']
        elif year == 2011:
            this_years_round = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10', 'R11', 'R12', 'R13', 'R14', 'R15', 'R16', 'R17', 'R18', 'R19', 'R20', 'R21', 'R22', 'R23', 'R24', 'EF', 'QF', 'SF', 'PF', 'GF']
        elif year == 2020:
            this_years_round = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10', 'R11', 'R12', 'R13', 'R14', 'R15', 'R16', 'R17', 'R18', 'EF', 'QF', 'SF', 'PF', 'GF']
        elif year < this_season:
            this_years_round = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10', 'R11', 'R12', 'R13', 'R14', 'R15', 'R16', 'R17', 'R18', 'R19', 'R20', 'R21', 'R22', 'R23', 'EF', 'QF', 'SF', 'PF', 'GF']
        else:
            this_years_round = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10', 'R11', 'R12', 'R13', 'R14', 'R15', 'R16', 'R17', 'R18', 'R19', 'R20', 'R21', 'R22', 'R23', 'EF', 'QF', 'SF', 'PF', 'GF'][:len(new_stored_info[year]["Carlton"]["Goals"])]
        #"""
        if year < 2011:
            master_rounds = []
            for j in new_stored_info[year]:
                if j == "master_round" or j == "averages":
                    continue
                master_rounds.append(new_stored_info[year][j]["rounds"])
            for rounds_set in master_rounds:
                counter = dict(collections.Counter(rounds_set))
                for i in counter:
                    if counter[i] == 1 or dict(collections.Counter(this_years_round))[i] == 2:
                        continue
                    this_years_round.insert(this_years_round.index(i), i)
        #"""
        totals = {}
        averages = {}
        for stat in new_stored_info[year]["Carlton"]:
            if stat == "rounds":
                continue
            totals[stat] = [[0 for i in range(len(this_years_round))], [0 for i in range(len(this_years_round))]]
            averages[stat] = [0 for i in range(len(this_years_round))]
        for idx, rd in enumerate(this_years_round):
            for club in new_stored_info[year]:
                if club == "master_round" or club == "averages" or rd not in new_stored_info[year][club]["rounds"]:
                    continue
                idx2 = new_stored_info[year][club]["rounds"].index(rd)
                for stat in new_stored_info[year][club]:
                    if stat == "rounds":
                        continue
                    totals[stat][0][idx] += new_stored_info[year][club][stat][idx2]
                    totals[stat][1][idx] += 1
        for idx, rd in enumerate(this_years_round):
            for club in new_stored_info[year]:
                if club == "master_round" or club == "averages" or rd not in new_stored_info[year][club]["rounds"]:
                    continue
                idx2 = new_stored_info[year][club]["rounds"].index(rd) + 1
                for stat in new_stored_info[year][club]:
                    if stat == "rounds":
                        continue
                    averages[stat][idx] = round(sum(totals[stat][0][:idx2]) / sum(totals[stat][1][:idx2]), 2)
        new_stored_info[year]["averages"] = averages
        new_stored_info[year]["master_round"] = this_years_round
        """
        print("You know not what you ask!")
        quit()
        with open(path_to_second_file, "w") as f:
            f.write(str(new_stored_info))
        #"""
    #quit()
    #print(new_stored_info)
    #'''

    """
    #Checks Frees Ratio
    check = []
    for year in years:
        for club in clubs:
            if clubs[club]._year_entered_comp > year or club == "Footscray" or (year >= 1997 and (clubs[club] == Bears or clubs[club] == Fitzroy)):
                continue
            rd = 11 #len(new_stored_info[year][club]["Frees"])
            if year in [2019, 2020] and club == "Richmond":
                print(year, round(sum(new_stored_info[year][club]["Frees"][:rd]) / sum(new_stored_info[year][club]["Frees Against"][:rd]), 6) * 100) #str(+ '%)')
            if len(new_stored_info[year][club]["Frees"]) < rd or year == 2021:
                continue
            year_precentage = round(sum(new_stored_info[year][club]["Frees"][:rd]) / sum(new_stored_info[year][club]["Frees Against"][:rd]), 6) * 100 #str(+ '%)'
            check.append((year_precentage, club, year))
    check.append((69.91, 'Richmond', 2021))
    a = [(idx + 1, i) for idx, i in enumerate(sorted(check)[:30])]
    for i in a:
        print(str(i[1][2]), i[1][1], str(i[1][0]) + '%')
    quit()
    #"""

    selected_year = 2020
    selected_clubs = [i for i in clubs]#["Richmond", "Geelong"]#, "West Coast", "Geelong", "Hawthorn"]#
    rolling_games = 5
    print("Drawing Graphs")
    for stat in new_stored_info[selected_year]["Carlton"]:
        if stat == "rounds":
            continue
        fig = plt.figure()
        ax = fig.add_subplot(111)
        #ax.set_xticks([i for i in range(1960, (years[-1] + (years[-1] % 10) + 10), 10)])
        ax.minorticks_on()
        ax.grid(which='minor')
        ax.grid(which='major', color="black")
        x = new_stored_info[selected_year]["master_round"]
        league_avg = new_stored_info[selected_year]["averages"][stat]
        ax.plot(x, league_avg, c="k", label="League Avg After X Rounds. End Year: " + str(league_avg[-1]))#, ls=":"
        ax.scatter(x, league_avg, c="k")
        for club in selected_clubs:
            y = new_stored_info[selected_year].get(club, "not yet. or too late")
            if y == "not yet. or too late":
                continue
            proper_y = y[stat]
            proper_x = y["rounds"]
            ax.plot(proper_x, proper_y, c=clubs[club]._colour, ls=":", label=club + " Stat In Round X")#, where="post", ls=":"
            ax.scatter(proper_x, proper_y, c=clubs[club]._colour)
            avg = [sum(proper_y[:idx])/idx for idx in range(1, len(proper_y) + 1)]
            ax.plot(proper_x, avg, c=clubs[club]._colour, label=club + " Avg After X Rounds. End Year: " + str(round(avg[-1], 2)))#, where="post", ls=":", ls="--"
            if len(proper_x) > 11:
                moving_average = [round(i, 2) for i in pd.DataFrame(proper_y).rolling(rolling_games).mean()[0].tolist()[rolling_games - 1:]]
                # start = math.floor((rolling_games - 1) / 2)
                # stop = len(proper_x) - start
                for idx in range(math.floor(rolling_games / 2)):
                    moving_average.insert(idx, moving_average[idx])
                    moving_average.append(moving_average[-1])
                ax.plot(proper_x, moving_average, ls="--", color=clubs[club]._colour, label=club + " Rolling " + str(rolling_games) + " Games Avg (Ends Padded)")#[start:stop]
            for idx, x_point in enumerate(proper_x):
                colour = "grey"
                margin = y["margins"][idx]
                if margin > 0:
                    colour = "green"
                elif margin < 0:
                    colour = "red"
                ax.scatter(x_point, proper_y[idx], s=60, c=colour)#proper_y
        #plt.legend()
        plt.title(stat + " Per Game in the " + str(selected_year) + " Season")

DRAW_YEAR_GRAPH = True

if DRAW_YEAR_GRAPH:
    stored_info = {}
    grab_new_data = False
    if grab_new_data:
        stored_info["info"] = getURL(universalURL)
        with open(path_to_file, "w") as f:
            f.write(str(stored_info))
    with open(path_to_file, "r") as f:
        stored_info = ast.literal_eval(f.read())
    print("Converting raw data:")
    #Convert data to searchable format
    text = stored_info["info"]
    soup = BeautifulSoup(text, features="lxml")
    tables = soup.findChildren('table')
    print("done.")
    print("")

    print("Initialising:")
    year_by_year_master_averages = {}

    master_average_rows = tables[2].findAll('tr')[1:-1]
    for ea_stat in master_average_rows[0].findAll('th')[1:]:
        year_by_year_master_averages[stats_key[ea_stat.text.strip()]] = []
    year_by_year_master_averages["Disposals"] = []
    year_by_year_master_averages["(avg_goals*6+avg_behinds)"] = []
    year_by_year_master_averages["(avg_goals+avg_behinds)"] = []
    year_by_year_master_averages["(avg_frees_for-avg_frees_against)"] = []
    #year_by_year_master_averages["(avg_frees_for/avg_frees_against)"] = []

    for ea_stat in year_by_year_master_averages:
        for ea_club in ordered_clubs:
            clubs[ea_club]._stats[ea_stat] = []

    for ea_club in ordered_clubs:
        clubs[ea_club]._stats["Disposals"] = []
        clubs[ea_club]._stats["(avg_goals*6+avg_behinds)"] = []
        clubs[ea_club]._stats["(avg_goals+avg_behinds)"] = []
        clubs[ea_club]._stats["(avg_frees_for-avg_frees_against)"] = []

    #Get comp avg year by year
    for ea_row in master_average_rows[1:]:
        columns = ea_row.findAll('td')[1:]
        for idx, key in enumerate(year_by_year_master_averages):
            if key == "Disposals" or key == "(avg_goals*6+avg_behinds)" or key == "(avg_goals+avg_behinds)" or key == "(avg_frees_for-avg_frees_against)":
                continue
            new_stat = columns[idx].text.strip()
            if new_stat:
                adjust = float(new_stat)
                if int(ea_row.find('td').text.strip()) == 2020:
                    adjust *= 1.25
                year_by_year_master_averages[key].append(adjust)
        year_by_year_master_averages["Disposals"].append(year_by_year_master_averages["Kicks"][-1] + year_by_year_master_averages["Handballs"][-1])
        year_by_year_master_averages["(avg_goals*6+avg_behinds)"].append(year_by_year_master_averages["Goals"][-1] * 6 + year_by_year_master_averages["Behinds"][-1])
        year_by_year_master_averages["(avg_goals+avg_behinds)"].append(year_by_year_master_averages["Goals"][-1] + year_by_year_master_averages["Behinds"][-1])
        year_by_year_master_averages["(avg_frees_for-avg_frees_against)"].append(year_by_year_master_averages["Frees"][-1] - year_by_year_master_averages["Frees Against"][-1])
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
                # else:
                #     print(ea_club)
                #     clubs[ea_club]._stats[stat].append(0)
        print("...." + stat + " done.")
    stat = "(avg_goals*6+avg_behinds)"
    for ea_club in ordered_clubs:
        for idx in range(len(clubs[ea_club]._stats["Goals"])):
            clubs[ea_club]._stats[stat].append(clubs[ea_club]._stats["Goals"][idx] * 6 + clubs[ea_club]._stats["Behinds"][idx])
    print("...." + stat + " done.")
    stat = "(avg_goals+avg_behinds)"
    for ea_club in ordered_clubs:
        for idx in range(len(clubs[ea_club]._stats["Goals"])):
            clubs[ea_club]._stats[stat].append(clubs[ea_club]._stats["Goals"][idx] + clubs[ea_club]._stats["Behinds"][idx])
    print("...." + stat + " done.")
    stat = "(avg_frees_for-avg_frees_against)"
    for ea_club in ordered_clubs:
        for idx in range(len(clubs[ea_club]._stats["Frees"])):
            clubs[ea_club]._stats[stat].append(clubs[ea_club]._stats["Frees"][idx] - clubs[ea_club]._stats["Frees Against"][idx])
    print("...." + stat + " done.")
    print("")
    print("Calculating standard deviations (of avgs):")
    standard_deviations_of_averages = {}
    medians = {}
    for stat in year_by_year_master_averages:
        standard_deviations_of_averages[stat] = [[] for i in range(len(clubs[ea_club]._stats[stat]))]
        medians[stat] = [[] for i in range(len(clubs[ea_club]._stats[stat]))]
        for ea_club in ordered_clubs:
            for idx in range(len(clubs[ea_club]._stats[stat])):
                standard_deviations_of_averages[stat][idx].append(clubs[ea_club]._stats[stat][idx])
                medians[stat][idx].append(clubs[ea_club]._stats[stat][idx])
        standard_deviations_of_averages[stat] = [statistics.stdev(standard_deviations_of_averages[stat][i]) for i in range(len(standard_deviations_of_averages[stat]))]
        medians[stat] = [statistics.median(medians[stat][i]) for i in range(len(medians[stat]))]
    print("done")
    print("Finally all done. Data now manipulatable/graphable.")
    print("")

    teams_to_analyse = ["Richmond"] #[i for i in ordered_clubs if (i != "Brisbane Bears" and i != "Fitzroy")]#["Richmond", "Western Bulldogs"]# ["Richmond", "West Coast"]# 

    # print("Deep dive into 1 particular team:")
    # particular_team = "Richmond"
    # n_years_2_go_back = 10
    # for stat in year_by_year_master_averages:
    #     years = []
    #     for i in range(n_years_2_go_back):
    #         team_numbers = []
    #         for ea_club in teams_to_analyse:
    #             team_numbers.append((clubs[ea_club]._stats[stat][-1 * (i + 1)], ea_club))
    #             for idx in range(len(clubs[ea_club]._stats[stat])):
    #                 break
    #         team_numbers = sorted(team_numbers, reverse=True)
    #         position = [idx for idx, (stat2, team) in enumerate(team_numbers) if team == particular_team][0] + 1
    #         years.append(position)
    #     averages = []
    #     for z in years:
    #         averages.append(statistics.mean(years[:-1]))
    #     print(stat + ": #" + str(position) + ", " + "different from last year")
    # print("done")
    # print("")
    # quit()


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
            ax.plot(years[len(years) - len(clubs[set_team]._stats[stat]):], clubs[set_team]._stats[stat], c=clubs[set_team]._colour, label=clubs[set_team]._name + " Mean")#, where="post", ls=":"
            ax.scatter(years[len(years) - len(clubs[set_team]._stats[stat]):], clubs[set_team]._stats[stat], c=clubs[set_team]._colour)
        x = years[len(years) - len(year_by_year_master_averages[stat]):]
        ax.plot(x, year_by_year_master_averages[stat], c="b", label="League Mean", ls=":")#, where="post"
        ax.scatter(x, year_by_year_master_averages[stat], c="b")
        # ax.plot(x, medians[stat], c="k", label="League Median", ls=":")
        # ax.scatter(x, medians[stat], c="k")
        # ax.plot(x, [year_by_year_master_averages[stat][i] - standard_deviations_of_averages[stat][i] for i in range(len(year_by_year_master_averages[stat]))], c="r", label="League Avg - One Std Deviation")#, where="post"
        # ax.scatter(x, [year_by_year_master_averages[stat][i] - standard_deviations_of_averages[stat][i] for i in range(len(year_by_year_master_averages[stat]))], c="r")
        # ax.plot(x, [year_by_year_master_averages[stat][i] + standard_deviations_of_averages[stat][i] for i in range(len(year_by_year_master_averages[stat]))], c="green", label="League Avg + One Std Deviation")#, where="post"
        # ax.scatter(x, [year_by_year_master_averages[stat][i] + standard_deviations_of_averages[stat][i] for i in range(len(year_by_year_master_averages[stat]))], c="green")
        ax.plot(x, [min([clubs[j]._stats[stat][i - (len(clubs["Carlton"]._stats[stat]) - len(clubs[j]._stats[stat]))] for j in [k for k in ordered_clubs if (k != "Brisbane Bears" and k != "Fitzroy")] if i - (len(clubs["Carlton"]._stats[stat]) - len(clubs[j]._stats[stat])) >= 0]) for i in range(len(year_by_year_master_averages[stat]))], c="r", label="Avg of lowest team that year")#, where="post"
        ax.scatter(x, [min([clubs[j]._stats[stat][i - (len(clubs["Carlton"]._stats[stat]) - len(clubs[j]._stats[stat]))] for j in [k for k in ordered_clubs if (k != "Brisbane Bears" and k != "Fitzroy")] if i - (len(clubs["Carlton"]._stats[stat]) - len(clubs[j]._stats[stat])) >= 0]) for i in range(len(year_by_year_master_averages[stat]))], c="r")
        ax.plot(x, [max([clubs[j]._stats[stat][i - (len(clubs["Carlton"]._stats[stat]) - len(clubs[j]._stats[stat]))] for j in [k for k in ordered_clubs if (k != "Brisbane Bears" and k != "Fitzroy")] if i - (len(clubs["Carlton"]._stats[stat]) - len(clubs[j]._stats[stat])) >= 0]) for i in range(len(year_by_year_master_averages[stat]))], c="green", label="Avg of highest team that year")#, where="post"
        ax.scatter(x, [max([clubs[j]._stats[stat][i - (len(clubs["Carlton"]._stats[stat]) - len(clubs[j]._stats[stat]))] for j in [k for k in ordered_clubs if (k != "Brisbane Bears" and k != "Fitzroy")] if i - (len(clubs["Carlton"]._stats[stat]) - len(clubs[j]._stats[stat])) >= 0]) for i in range(len(year_by_year_master_averages[stat]))], c="green")
        plt.legend()
        plt.title("Avg " + stat + " Per Game")

    print("done.")
    print("")

print("Thank you afltables.com")
print("")
print("Displaying graphs for you now:")
plt.show()
print("")
print("All graphs closed. See you later.")