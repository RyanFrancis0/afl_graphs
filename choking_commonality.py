#help("modules") #
import urllib.request
import math
import statistics
import collections
import ast
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

"""
Hypothesis 2: A refutation of the more wins and/or better percentage is equivalent to a better side 
theory. By natural extension, that they are directly related (e.g. 10 more wins is a better side 
than 2 more).

1st:
This could be proven to be true by looking at how often the team with more wins beats a team in
finals with less wins. You would also expect a side with 5 more relative wins to come out on top
more often than a side with 1 more win. Percentage will be analysed at the same time but reported
separately to see if or to waht extent it differs.
I will only analyse finals games, because that is easier. But I do know that teams with lots of wins
lose to others during h&a as well. How often I don't know (in high winning sides the losses are more 
memorable, same for wins in losing sides).
This is based on the premise that who wins in a direct match between two sides is the ultimate
proof of which is the better side. This is, of course, wrong, as no premiership side has ever had
an unbeaten season, but they could definetely be decribed as better sides than those (at least the
majority of those) they lost to that year. 
However, everyone is really only interested in premierships as a measure of a side's quality or the
best measure, and this is predicated on beating a side in one game in very specific circumstances
as the best way to prove which is a better side. You would expect an upset to happen exactly as often
as they were "upset" in the home and away season.
"""

year_started = 1990 #<- dont'change to 2000!!!!!! see far below
script_directory = str(os.path.dirname(os.path.realpath(__file__)))
file_name = "choking_commonality_savefile.txt"
path_to_file = script_directory + '\\' + file_name
"""#Uncomment this section to update info
#constants
universalURL = 'https://afltables.com/afl/seas/{}.html' 
this_season = 2020#<-this is a manually used value, see last_season below which is autoupdated
teams_in_comp = []
finals_cutoff = []
teams = {}
colours = {"Fitzroy":"Grey", "Gold Coast":"orangered", "Geelong":"royalblue", "Essendon":"red", "Carlton":"navy", "Collingwood":"black", "Melbourne":"lime", "Hawthorn":"brown", "Fitzroy":"grey", "St Kilda":"crimson", "Richmond":"yellow", "North Melbourne":"blue", "Western Bulldogs":"green", "Fremantle":"purple","Greater Western Sydney":"orange", "Brisbane Lions": "orangered", "Port Adelaide":"cyan", "West Coast":"darkgoldenrod", "Sydney":"deeppink", "Adelaide":"royalblue"} #ugh takes so long to write out
running_colours = []
for i in teams:
    running_colours.append(colours[i])

def getURL(url):
    stream = urllib.request.urlopen(url)
    text = stream.read().decode('utf-8')
    stream.close()
    return text

class Season(object):
    def __init__(self, year):
        self._year = year
        self._games_in_season = 0
        self._teams_in_season = 0
        self._total_matches = []
        self._home_and_away_matches = []
        self._finals_matches = []
        self.n_home_and_away_wins = 0
        self._n_total_wins = 0
        self._home_and_away_win_percentage = 0.0
        self._percentage = 0.0
        self._home_and_away_ladder_position = 0
        self._finals_percentage = 0.0
        self._final_ladder_position = 0
    def get_form(self, round):
        '''Returns w/l record of 5 rounds immediately before selected one'''
        if round < 5:
            return [0, 0, 0, 0, 0]
        return []
    def do_calcs(self):
        return

class Club(object):
    def __init__(self, name, home_grounds, interstate):
        '''Club(str, str)'''
        self._name = name
        self._colour = colours[name]
        self._home_grounds = home_grounds
        self._interstate = interstate
        self._seasons = {}
    #def get_season(self, year):
    #    return self._seasons[year - 2000]
victoria = ["M.C.G.", "Princes Park", "Docklands", "Kardinia Park"]

# == multiple home grounds in this stretch actually
Richmond = Club("Richmond", ["M.C.G."], False)
WC = Club("West Coast", ["Subiaco", "W.A.C.A", "Perth Statdium"], True)#
GC = Club("Gold Coast", ["Carrara"], True)
Brisbane = Club("Brisbane Lions", ["Gabba"], True)
STK = Club("St Kilda", ["Docklands"], False)
Fremantle = Club("Fremantle", ["Subiaco", "W.A.C.A", "Perth Statdium"], True)#
Collingwood = Club("Collingwood", ["M.C.G."], False)
Melbourne = Club("Melbourne", ["M.C.G."], False)
Carlton = Club("Carlton", ["Princes Park", "M.C.G."], False)#
Essendon = Club("Essendon", ["M.C.G."], False)#
Hawthorn = Club("Hawthorn", ["M.C.G."], False)
Adelaide = Club("Adelaide", ["Football Park", "Adelaide Oval"], True)#
PA = Club("Port Adelaide", ["Football Park", "Adelaide Oval"], True)#
Sydney = Club("Sydney", ["S.C.G."], True)
GWS = Club("Greater Western Sydney", ["Sydney Showground"], True)
NM = Club("North Melbourne", ["Docklands"], False)
WB = Club("Western Bulldogs", ["Docklands"], False)
Geelong = Club("Geelong", ["Kardinia Park"], False)
Fitzroy = Club("Fitzroy", ["M.C.G."], False)

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
    "Brisbane Bears": Brisbane,
    "Fitzroy": Fitzroy,
    "Hawthorn": Hawthorn,
    "Adelaide": Adelaide,
    "Port Adelaide": PA,
    "Sydney": Sydney,
    "Greater Western Sydney": GWS,
    "Western Bulldogs": WB,
    "Geelong": Geelong
    }

current_clubs = set(clubs.values())

class Match(object):
    def __init__(self, home_team, away_team, home_team_score, away_team_score, venue):
        self._home_team = home_team
        self._away_team = away_team
        self._home_team_score = home_team_score
        self._away_team_score = away_team_score
        self._margin = home_team_score - away_team_score
        self._winner = "draw"
        self._loser = "draw"
        if self._margin > 0:
            self._winner = self._home_team 
            self._loser = self._away_team 
        elif self._margin < 0:
            self._winner = self._away_team
            self._loser = self._home_team 
        self._venue = venue

finals_home_and_away_differentials = [] # (win differential, percentage differential, h&a ladder position of winner)

for year in range(year_started, this_season + 1):
    text = getURL(universalURL.format(year))
    soup = BeautifulSoup(text, 'html.parser')
    tables = soup.findAll('table')
    last_season = this_season# int(tables[0].find('tr').find('a').text) - 1
    tables.reverse()
    #create seasons for every club
    for i in current_clubs:
        i._seasons[year] = Season(year) 
    normal = -20
    if year == 2010:
        normal -= 2
    elif year < 1994:
        normal += 4
    rows = BeautifulSoup(getURL(universalURL.format(year)), features="lxml").findChildren('table')[normal].findChildren('tr')[2:-1]
    for i in rows:
        collumns = i.findAll('td')
        club = collumns[1].text
        if club not in clubs.keys():
            break
        season = clubs[club]._seasons[year]
        #season._games_in_season = int(collumns[2].text) + len(season._finals_matches)
        season._teams_in_season = len(rows)
        season.n_home_and_away_wins = float(collumns[3].text)
        draws = str(collumns[4].text).strip()
        if draws != '':
            season.n_home_and_away_wins += float(collumns[4].text) / 2
        '''
            season._n_total_wins = season.n_home_and_away_wins
            score_for = 0
            score_against = 0
            for j in season._finals_matches:
                if (j._home_team == club and j._margin > 0) or (j._away_team == club and j._margin < 0):
                    season._n_total_wins += 1
                if j._home_team == club:
                    score_for += j._home_team_score
                    score_against += j._away_team_score
                else:
                    score_for += j._away_team_score
                    score_against += j._home_team_score
            if score_against != 0:
                season._finals_percentage = score_for / score_against
        '''
        season._home_and_away_win_percentage = float(collumns[13].text[:3]) / (4 * float(collumns[2].text))#%of games played that were wins. Note! this line will reject a perfect 100% win season as a 10% one
        season._percentage = float(collumns[12].text)
        season._home_and_away_ladder_position = int(collumns[0].text)
    '''#home and away games
    for i in tables[x + 5:]:
        links = i.findAll('a')
        if len(links) != 4 and len(links) != 3:
            continue
        #print(links)
        rows = i.findAll('tr')
        #print(rows)
        team1 = links[0].text
        venue = links[1].text
        team2 = links[2].text
        if len(rows) > 2:
            continue
        team1_score = int(rows[0].findAll('td')[2].text)
        team2_score = int(rows[1].findAll('td')[2].text)
        match = Match(team1, team2, team1_score, team2_score, venue)
        if match._inter_match:
            inter_standard_games += 1
            if team1_score == team2_score:
                inter_inter_standard_wins += 0.5
            elif clubs[match._winner]._interstate:
                inter_inter_standard_wins += 1
            if clubs[team1] == WC or clubs[team2] == WC:
                wc_standard_games += 1
                if team1_score == team2_score:
                    wc_standard_wins += 0.5
                elif clubs[match._winner] == WC:
                    wc_standard_wins += 1
        clubs[team1]._seasons[year]._total_matches.append(match)
        clubs[team1]._seasons[year]._home_and_away_matches.append(match)
        clubs[team2]._seasons[year]._total_matches.append(match)
        clubs[team2]._seasons[year]._home_and_away_matches.append(match)
    '''
    x = 0
    for i in tables[::2]:
        links = i.findAll('a')
        team1 = links[0].text
        venue = links[1].text
        team2 = links[2].text
        rows = i.findAll('tr')
        team1_score = int(rows[0].findAll('td')[2].text)
        team2_score = int(rows[1].findAll('td')[2].text)
        match = Match(team1, team2, team1_score, team2_score, venue)
        clubs[team1]._seasons[year]._total_matches.append(match)
        clubs[team1]._seasons[year]._finals_matches.append(match)
        clubs[team2]._seasons[year]._total_matches.append(match)
        clubs[team2]._seasons[year]._finals_matches.append(match)
        if team1_score > team2_score:
            clubs[team1]._seasons[year]._final_ladder_position = x + 1
            clubs[team2]._seasons[year]._final_ladder_position = x + 2
        elif team2_score > team1_score:
            clubs[team1]._seasons[year]._final_ladder_position = x + 2
            clubs[team2]._seasons[year]._final_ladder_position = x + 1
        if match._winner != "draw":
            win_differential = clubs[match._winner]._seasons[year].n_home_and_away_wins - clubs[match._loser]._seasons[year].n_home_and_away_wins
            percentage_differential = round(clubs[match._winner]._seasons[year]._percentage - clubs[match._loser]._seasons[year]._percentage, 2)
            winner_ladder_position = clubs[match._winner]._seasons[year]._home_and_away_ladder_position
            loser_ladder_position = clubs[match._loser]._seasons[year]._home_and_away_ladder_position
            finals_home_and_away_differentials.append((win_differential, percentage_differential, winner_ladder_position, loser_ladder_position, x == 0))
            if winner_ladder_position == 0:
                print("wtf?", match._winner, match._margin)
        #If this is the gf and its not a draw
        if team1_score != team2_score and (clubs[team1]._seasons[year]._final_ladder_position == 1 or clubs[team2]._seasons[year]._final_ladder_position == 1) and (clubs[team1]._interstate or clubs[team2]._interstate):
            pass
        if tables[x + 2].text == "Finals":
            break
        x += 2

    '''
        total_sides = 0
        for i in current_clubs:
            season = i._seasons[year]
            if len(season._total_matches) > 0:
                total_sides += 1
                if len(season._finals_matches) > 0:
                        pass
    '''
    print(year)

stored_info = {"key": finals_home_and_away_differentials} # {year:[tables, bs]}
with open(path_to_file, "w") as f:
    f.write(str(stored_info))
#since 2000 there have been 189 finals, so len(finals) - 189 == index of 2000
#"""
#"""
with open(path_to_file, "r") as f:
    stored_info = ast.literal_eval(f.read())
#MAIN:
#"""#RETRIEVE DATA
finals_home_and_away_differentials = stored_info["key"][len(stored_info["key"]) - 189:] #<-To start from 2000. Else starts 1990
print(finals_home_and_away_differentials)
print("# of finals since " + str(year_started) + ": ", len(finals_home_and_away_differentials))
'''
unique_wins_drequency = {}
for i in finals_home_and_away_differentials:
    unique_wins_commonality.get(i[0], 0) += 1
'''
counter = collections.Counter([i[0] for i in finals_home_and_away_differentials])
print("frequency of diff between h&a wins of finalists:", counter)
avg_ladder_diff = 0
for i in counter.most_common():
    avg_ladder_diff += i[0] * i[1]
counter2 = collections.Counter([i[2] for i in finals_home_and_away_differentials])
print("frequency of winning ladder positions:", counter2)
counter3 = collections.Counter([round(round(i[1]) / 10) * 10 for i in finals_home_and_away_differentials])
print("percentage diff rounded to nearest 10s:", counter3)
sign = lambda x: (1, -1)[x < 0]
counter4 = collections.Counter([math.floor(abs(i[1]) / 10) * 10 * sign(i[1]) for i in finals_home_and_away_differentials])
print("lower bound percentage diffs:", counter4)
counter5 = collections.Counter([i[0] for i in finals_home_and_away_differentials if i[4]])
print("Diff wins of premiers:", counter5)
prem_diff = 0
for i in counter5.most_common():
    prem_diff += i[0] * i[1]
counter6 = collections.Counter([i[1] for i in finals_home_and_away_differentials if i[4]])
print("percentage of grand finalists winners:", counter6)
counter10 = collections.Counter([round(i[1] / 10) * 10 for i in finals_home_and_away_differentials if i[4]])
print("frequency of rounded percentage of grand finalists winners:", counter10)
counter8 = collections.Counter([i[2] for i in finals_home_and_away_differentials if i[4]])
print("Ladder positions of premiers: ", counter8)
counter9 = collections.Counter([i[3] for i in finals_home_and_away_differentials if i[4]])
print("Ladder positions of grand final losers: ", counter9)
ladder_pos = 0
for i in counter8.most_common():
    ladder_pos += i[0] * i[1]
ladder_pos2 = 0
for i in counter9.most_common():
    ladder_pos2 += i[0] * i[1]
print("avg premiers ladder pos:", ladder_pos, "avg gfls ladder pos:", ladder_pos2)
prem_perc = 0
for i in counter6.most_common():
    prem_perc += i[0] * i[1]
print("avg wins (ignoring 0s):", prem_diff, "avg percentages (ignoring 0s):", prem_perc)
counter7 = collections.Counter([i[3] - i[2] for i in finals_home_and_away_differentials])
print("frequency of difference between winner and loser ladder pos:", counter7)
avg_diff = 0
for i in counter7.most_common():
    avg_diff += i[0] * i[1]
'''
y = counter.most_common()
x = len(x)
for i in range(x):
    for k in range(x):
        if i != k and abs(y[i][0]) == abs(y[k][0]):
            y[i][1] += y[k][1]
            continue
print("overall of winning ")
'''
counter8 = collections.Counter([(i[2], i[3]) for i in finals_home_and_away_differentials])
print("Most common wins by ladder pos diff:", counter8)
print("avg diff (ignoring 0s):", avg_diff)
print("avg ladder diff:", statistics.mean([i[0] for i in finals_home_and_away_differentials]), avg_ladder_diff)
print("Most common ladder diff:", statistics.mode([i[0] for i in finals_home_and_away_differentials]))
print("avg percentage diff:", statistics.mean([i[1] for i in finals_home_and_away_differentials]))
print("Most common winners ladder position:", statistics.mode([i[2] for i in finals_home_and_away_differentials]))