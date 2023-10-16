
import math
import statistics
import ast
import collections
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request

"""
Hypothesis 1: 
A refutation of the interstate sides suffer more than melbourne based ones theory.
In the AFL, lack of co-residents (and possibly more experience) at a ground is a bigger advantage
than extra travel is a disadvantage. As in interstate teams (+geelong) have an advantage over
the melbourne based teams by virtue of the extremely unfortunate concentration of clubs in 
melbourne.

Two ways to prove: 
1st: Examine ladder positions of interstate sides of the past 20-30 years and compare.
2nd: Examine win to loss ratio of interstate sides at different grounds in the last 20-30 years
        and compare.

Sub pthingy 1: (predicate?)
As sides go through their natural rise and fall, sometimes there will be periods where a majority
of interstate sides are perfectly naturally just doing well all around the same time
(2001-2007???) and vice versa (2008-2011???). Solar and lunar exlipses if you will (or their
opposite??). This might skew the results if too small a pool of data is examined (i.e. proof 1).
So both proofs must be done. 
Sub pthingy 2:
A factor of Geelong's success by virtue of being only one at home ground dand virtue of experience
and low travel to other melbourne grounds (being given "home games" they don't want at melbourne
grounds). - I do not think this is provable as other clubs have had sustained periods of success
(west coast, sydney, going further back hawthorn).
Sub pthingy 3:
The 'cumulative weariness' theory. That while the effets of trave lmay not be noticeable one week
to the next, it accumulates throughout a season and by finals time interstae sides are , causing
them to have finals losses they shouldn't. So the data must be analysed for 
This may or may not be offset by the pre-finals bye, depending on which accredited school of
philosophy one ascribes to. The low numbers of finals statistics for interstate sides makes this 
whole sub thingy optimistic to be proven one way or another.
Sub pthingy 4:
Length of trip may be a factor. Purely on the basis that 1. I can't be quite that bothered and 2.
out of all the clubs WC has the best win rate at the gabba, I will not be exploring this or taking
it into account in my study.
Sub pthingy 5:
When GC and GWS were introduced, they were both atrocious for a few seasons, for reasons that 
obviously had nothing to do with home ground advantage. This may skew the results. Will need to
examine changes without them.
Sub pthingy 6:
For the last ~20 years Carlton and Essendon have split home games evenly between the MCG and
Docklands. On the experience argument, one would expect them to lose at those grounds more often
than permanent tennants. This probably influences their home ground advantage in some way.
Sub pthingy 7:
Its obviously not going to be a big advantage either way. Interstate sides and melbourne sides
both go through extended ups and downs, or flash in the pan ups and downs.
Sub pthingy 8:
I should really go back over ptests (different p I'm 99% sure) again.
"""

"""
Hypothesis 2: A refutation of the more wins and/or better percentage is equivalent to a better side 
theory. By natural extension, that they are directly related (e.g. 10 more wins better side 
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

#constants
script_directory = str(os.path.dirname(os.path.realpath(__file__)))
file_name = "interstate_savefile.txt"
path_to_file = script_directory + '\\' + file_name
universalURL = 'https://afltables.com/afl/seas/{}.html' 
year_started = 1982#1982#1990 #1897 #1982
this_season = 2023#<-this is a manually used value, see last_season below which is autoupdated
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
        """Returns w/l record of 5 rounds immediately before selected one"""
        if round < 5:
            return [0, 0, 0, 0, 0]
        return []
    def do_calcs(self):
        return

class Club(object):
    def __init__(self, name, home_grounds, interstate, year_entered_comp = None):
        """Club(str, str)"""
        self._name = name
        self._colour = colours[name]
        self._home_grounds = home_grounds
        self._interstate = interstate
        self._seasons = {}
        self._year_entered_comp = year_entered_comp
        self._expected_premierships = []
        self._premierships = []
    #def get_season(self, year):
    #    return self._seasons[year - 2000]

victoria = ["M.C.G.", "Princes Park", "Docklands", "Kardinia Park", "Victoria Park", "Moorabbin Oval", "Victoria Park", "Junction Oval", "Arden St", "Waverley Park", "Western Oval", "Windy Hill"]

# == multiple home grounds in this stretch actually
IS_INTERSTATE = True
IS_VICTORIAN = False
Richmond = Club("Richmond", ["M.C.G."], IS_VICTORIAN, 1982)#False
WC = Club("West Coast", ["Subiaco", "W.A.C.A", "Perth Stadium"], IS_INTERSTATE, 1987)#True
GC = Club("Gold Coast", ["Carrara"], IS_INTERSTATE, 2011)#True
Brisbane = Club("Brisbane Lions", ["Gabba"], IS_INTERSTATE, 1987)#1997?#True
STK = Club("St Kilda", ["Docklands", "Moorabbin Oval", "Junction Oval"], IS_VICTORIAN, 1982)#False
Fremantle = Club("Fremantle", ["Subiaco", "W.A.C.A", "Perth Statdium"], IS_INTERSTATE, 1995)#False
Collingwood = Club("Collingwood", ["M.C.G.", "Victoria Park"], IS_VICTORIAN, 1982)#False
Melbourne = Club("Melbourne", ["M.C.G."], IS_VICTORIAN, 1982)#False
Carlton = Club("Carlton", ["Princes Park", "M.C.G.", "Docklands"], IS_VICTORIAN, 1982)#False
Essendon = Club("Essendon", ["M.C.G.", "Docklands", "Windy Hill"], IS_VICTORIAN, 1982)#False
Hawthorn = Club("Hawthorn", ["M.C.G.", "Waverley Park"], IS_VICTORIAN, 1982)#False
Adelaide = Club("Adelaide", ["Football Park", "Adelaide Oval"], IS_INTERSTATE, 1991)#True
PA = Club("Port Adelaide", ["Football Park", "Adelaide Oval"], IS_INTERSTATE, 1997)#True
Sydney = Club("Sydney", ["S.C.G.", "Stadium Australia"], IS_INTERSTATE, 1982)#True#1982
GWS = Club("Greater Western Sydney", ["Sydney Showground"], IS_INTERSTATE, 2012)#True
NM = Club("North Melbourne", ["Docklands", "Arden St"], IS_VICTORIAN, 1982)#False
WB = Club("Western Bulldogs", ["Docklands", "Western Oval"], IS_VICTORIAN, 1982)#False
Geelong = Club("Geelong", ["Kardinia Park"], IS_VICTORIAN, 1982)#False
Fitzroy = Club("Fitzroy", ["M.C.G."], IS_VICTORIAN, 1982)#False

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

DRAW = "draw"

class Match(object):
    def __init__(self, home_team, away_team, home_team_score, away_team_score, venue):
        self._home_team = home_team
        self._away_team = away_team
        self._home_team_score = home_team_score
        self._away_team_score = away_team_score
        self._margin = home_team_score - away_team_score
        self._winner = DRAW
        if self._margin > 0:
            self._winner = self._home_team 
        elif self._margin < 0:
            self._winner = self._away_team
        self._inter_match = (clubs[self._home_team]._interstate and not clubs[self._away_team]._interstate) or (clubs[self._away_team]._interstate and not clubs[self._home_team]._interstate)
        self._venue = venue

melbournian_averages = []
interstate_and_geelong_averages = []
victorian = []
victorian_finals = []
interstate_finals = []
interstate = []
clubs_averages = []

just_inter_games_vic_home = []
just_inter_games_inter_home = []
just_inter_games_vic_finals = []
just_inter_games_inter_finals = []
interstate_premierships = []
interstate_v_vic_grand_finals = []
number_of_interstate_sides_per_year = []

total_standard_games = 0
total_finals = 0
all_inter_haa_wins = 0
all_inter_finals_wins = 0

west_coast_finals_wins_per_year = []
all_west_coast_finals_v_vic = 0
WC_inter_finals_wins = 0

wc_home_and_away = []
all_wc_haa = 0
all_wc_haa_wins = 0

years = range(year_started, this_season + 1)
current_clubs = set(clubs.values())
interstate_clubs = [i for i in current_clubs if i._interstate]

r_hg_record_haa = [[0.0, 0]]
g_hg_record_haa = [[0.0, 0]]
wc_hg_record_haa = [[0.0, 0]]

all_inter_win_percentage_over_time = []
finals_inter_win_percentage_over_time = []
haagames_per_year = []
finals_per_year = []
finals_qualifiers_per_year = [0 for i in years]
expected_finals_qualifiers_per_year = []

n_i_s_p_y = []

finalists_ladder_positions = [[] for i in years]
non_finalists_ladder_positions = [[] for i in years]

all_inter_home_games = []

haa_home_side_advantage = 0
haa_n_all_games = 0

#"""
with open(path_to_file, "r") as f:
    stored_info = ast.literal_eval(f.read())
#MAIN:
    #"""#RETRIEVE DATA
    #"""
DOWNLOAD_NEW_SEASON = False
if DOWNLOAD_NEW_SEASON:
    stored_info = {} # {year:[text]}
    for year in years:
        stored_info[year] = getURL(universalURL.format(year))
        print(year)
    with open(path_to_file, "w") as f:
        f.write(str(stored_info))
    #"""

for year in years:
    last_season = this_season# int(tables[0].find('tr').find('a').text) - 1
    for i in current_clubs:
        i._seasons[year] = Season(year)
    text = stored_info[year] #getURL(universalURL.format(year))
    soup = BeautifulSoup(text, 'html.parser')
    tables = soup.findAll('table')
    tables.reverse()
    #create seasons for every club
    x = 0
    #do finals first
    inter_inter_finals_wins = 0
    inter_finals_games = 0
    inter_inter_standard_wins = 0
    inter_standard_games = 0
    inter_standard_home_games = 0
    wc_finals_games = 0
    wc_finals_wins = 0
    wc_standard_games = 0
    wc_standard_wins = 0
    for i in tables[::2]:
        links = i.findAll('a')
        team1 = links[0].text
        venue = links[1].text
        team2 = links[2].text
        rows = i.findAll('tr')
        team1_score = int(rows[0].findAll('td')[2].text)
        team2_score = int(rows[1].findAll('td')[2].text)
        match = Match(team1, team2, team1_score, team2_score, venue)
        if match._inter_match:
            inter_finals_games += 1
            if team1_score == team2_score:
                inter_inter_finals_wins += 0.5
            elif clubs[match._winner]._interstate:
                inter_inter_finals_wins += 1
            if clubs[team1] == WC or clubs[team2] == WC:
                wc_finals_games += 1
                if team1_score == team2_score:
                    wc_finals_wins += 0.5
                elif clubs[match._winner] == WC:
                    wc_finals_wins += 1
        clubs[team1]._seasons[year]._total_matches.append(match)
        clubs[team1]._seasons[year]._finals_matches.append(match)
        clubs[team2]._seasons[year]._total_matches.append(match)
        clubs[team2]._seasons[year]._finals_matches.append(match)
        if team1_score > team2_score:
            if clubs[team1]._seasons[year]._final_ladder_position == 0:
                clubs[team1]._seasons[year]._final_ladder_position = x + 1
            if clubs[team2]._seasons[year]._final_ladder_position == 0:
                clubs[team2]._seasons[year]._final_ladder_position = x + 2
        elif team2_score > team1_score:
            if clubs[team1]._seasons[year]._final_ladder_position == 0:
                clubs[team1]._seasons[year]._final_ladder_position = x + 2
            if clubs[team2]._seasons[year]._final_ladder_position == 0:
                clubs[team2]._seasons[year]._final_ladder_position = x + 1
        #If this is the gf and its not a draw and at least one of the teams is interstate
        if team1_score != team2_score and x == 0:# and year not in interstate_v_vic_grand_finals and (year not in interstate_premierships or not clubs[match._winner]._interstate):
            if (clubs[team1]._interstate or clubs[team2]._interstate):
                if (clubs[team1]._interstate and not clubs[team2]._interstate) or (clubs[team2]._interstate and not clubs[team1]._interstate):
                    interstate_v_vic_grand_finals.append(year)
                if clubs[match._winner]._interstate:
                    interstate_premierships.append(year)
                    if len(clubs[match._winner]._premierships) == 0:
                        clubs[match._winner]._premierships.append(1)
                    else:
                        clubs[match._winner]._premierships.append(clubs[match._winner]._premierships[-1] + 1)
            for i in current_clubs:
                if i._interstate and year >= i._year_entered_comp and i != clubs[match._winner]:
                    if len(i._premierships) == 0:
                        i._premierships.append(0)
                    else:
                        i._premierships.append(i._premierships[-1])
        if tables[x + 2].text == "Finals":
            break
        x += 2
    if wc_finals_games > 0:
        west_coast_finals_wins_per_year.append(100 * wc_finals_wins / wc_finals_games)
        all_west_coast_finals_v_vic += wc_finals_games
        WC_inter_finals_wins += wc_finals_wins
    bs = BeautifulSoup(text, features="lxml").findChildren('table')[-x - 4]#getURL(universalURL.format(year))
    finals_cutoff.append(len(bs.findChildren('tr', {"bgcolor":"#dddddd"})))
    rows = bs.findChildren('tr')[2:-1]
    for i in rows:
        collumns = i.findAll('td')
        club = collumns[1].text
        if club not in clubs.keys():
            break
        season = clubs[club]._seasons[year]
        season._games_in_season = int(collumns[2].text) + len(season._finals_matches)
        season._teams_in_season = len(rows)
        season.n_home_and_away_wins = int(collumns[3].text)
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
        #for j in range()
        season._home_and_away_win_percentage = float(collumns[13].text[:3]) / (4 * float(collumns[2].text))#%of games played that were wins, this line will reject a 100% season as a 10% one
        #if clubs[club]._interstate:
        #    print(club, float(collumns[13].text[:3]), (4 * float(collumns[2].text)), season._home_and_away_win_percentage)
        season._percentage = float(collumns[12].text)
        season._home_and_away_ladder_position = int(collumns[0].text)
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
        REIGNING_PREMIERS_LOSSES = False
        if REIGNING_PREMIERS_LOSSES == True:
            if year >= 1983 and match._margin != 0:
                #print(year, clubs[team1]._seasons[year - 1]._final_ladder_position, match._winner, team2)
                if clubs[team1]._seasons[year]._final_ladder_position == 1 and match._winner == team2:
                    print(year, team1, "lost to " + team2 + ", who finished", clubs[team2]._seasons[year]._home_and_away_ladder_position, "that year, by", abs(match._margin), "points at the", venue, "in round", clubs[team1]._seasons[year]._games_in_season - len(clubs[team1]._seasons[year]._finals_matches) - len(clubs[team1]._seasons[year]._home_and_away_matches))
                    if abs(match._margin) >=45: #clubs[team2]._seasons[year]._home_and_away_ladder_position >= season._teams_in_season - 2:
                        print("////////////////////////////// the bye isnt taken into account btws", season._teams_in_season)
                elif clubs[team2]._seasons[year]._final_ladder_position == 1 and match._winner == team1:
                    print(year, team2, "lost to " + team1 + ", who finished", clubs[team1]._seasons[year]._home_and_away_ladder_position, "that year, by", abs(match._margin), "points at the", venue, "in round", clubs[team1]._seasons[year]._games_in_season - len(clubs[team1]._seasons[year]._finals_matches) - len(clubs[team1]._seasons[year]._home_and_away_matches))
                    if abs(match._margin) >=45: #clubs[team1]._seasons[year]._home_and_away_ladder_position >= season._teams_in_season - 2:
                        print("//////////////////////////////", season._teams_in_season)
        '''
        desirables = ["West Coast", "Richmond", "Geelong"]
        if (team1 in desirables or team2 in desirables):
            actual_home_ground_team = None
            if team1 in desirables and venue in clubs[team1]._home_grounds:
                actual_home_ground_team = team1
            elif team2 in desirables and venue in clubs[team2]._home_grounds:
                actual_home_ground_team = team2
            if actual_home_ground_team != None:
                plus_value = 0.5 if (match._winner == DRAW) else 1.0 if (match._winner == actual_home_ground_team) else 0.0
                if actual_home_ground_team == desirables[2]:
                    if len(g_hg_record_haa) <= year - year_started:
                        g_hg_record_haa.append([plus_value, 1])
                    else:
                        g_hg_record_haa[year - year_started][0] += plus_value
                        g_hg_record_haa[year - year_started][1] += 1
                elif actual_home_ground_team == desirables[1]:
                    if len(r_hg_record_haa) <= (year - year_started) - 5:
                        r_hg_record_haa.append([plus_value, 1])
                    else:
                        if year > 1986:
                            r_hg_record_haa[year - year_started - 5][0] += plus_value
                            r_hg_record_haa[year - year_started - 5][1] += 1
                elif actual_home_ground_team == desirables[0]:
                    if len(wc_hg_record_haa) <= year - year_started - 5:
                        wc_hg_record_haa.append([plus_value, 1])
                    else:
                        wc_hg_record_haa[year - year_started - 5][0] += plus_value
                        wc_hg_record_haa[year - year_started - 5][1] += 1
        '''
        if match._winner == match._home_team:
            haa_home_side_advantage += 1
        haa_n_all_games += 1
        if match._inter_match:
            #if clubs[team1]._year_entered_comp == year or clubs[team2]._year_entered_comp == year:
            #    continue
            inter_standard_games += 1
            if clubs[team1]._interstate:
                inter_standard_home_games += 1
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
    if wc_standard_games > 0:
        wc_home_and_away.append(100 * wc_standard_wins / wc_standard_games)
        all_wc_haa += wc_standard_games
        all_wc_haa_wins += wc_standard_wins
    just_inter_games_inter_home.append(100 * inter_inter_standard_wins / inter_standard_games)
    just_inter_games_vic_home.append(100 * (inter_standard_games - inter_inter_standard_wins) / inter_standard_games)
    if inter_finals_games > 0:
        just_inter_games_inter_finals.append(100 * inter_inter_finals_wins / inter_finals_games)
        just_inter_games_vic_finals.append(100 * (inter_finals_games - inter_inter_finals_wins) / inter_finals_games)
    else:
        just_inter_games_inter_finals.append(None)
        just_inter_games_vic_finals.append(None)
    for i in current_clubs:
        i._seasons[year]._total_matches.reverse()
        i._seasons[year]._finals_matches.reverse()
        i._seasons[year]._home_and_away_matches.reverse()
    melboune_win_percentages = []
    interstate_win_percentages = []
    just_interstate = []
    just_interstate_finals = []
    just_victorian = []
    just_victorian_finals = []
    number_of_interstate_sides = 0
    total_sides = 0
    for i in current_clubs:
        season = i._seasons[year]
        if len(season._total_matches) > 0:
            total_sides += 1
            if len(i._expected_premierships) == 0:
                i._expected_premierships.append(1 / season._teams_in_season)
            else:
                i._expected_premierships.append(1 / season._teams_in_season + i._expected_premierships[-1])
            if i._interstate:
                number_of_interstate_sides += 1
                interstate_win_percentages.append(season._home_and_away_win_percentage)
                if len(season._finals_matches) > 0:
                    finals_qualifiers_per_year[years.index(year)] += 1
                    finalists_ladder_positions[years.index(year)].append(season._home_and_away_ladder_position)
                    if i == Geelong:
                        just_victorian_finals.append((season._n_total_wins - season.n_home_and_away_wins) / len(season._finals_matches))
                    else:
                        just_interstate_finals.append((season._n_total_wins - season.n_home_and_away_wins) / len(season._finals_matches))
                else:
                    non_finalists_ladder_positions[years.index(year)].append(season._home_and_away_ladder_position)
                if i != Geelong:
                    just_interstate.append(season._home_and_away_win_percentage)
                else:
                    just_victorian.append(season._home_and_away_win_percentage)
            else:
                melboune_win_percentages.append(season._home_and_away_win_percentage)
                just_victorian.append(season._home_and_away_win_percentage)
                if len(season._finals_matches) > 0:
                    just_victorian_finals.append((season._n_total_wins - season.n_home_and_away_wins) / len(season._finals_matches))
    ignore_extra_team = 0
    #if year > 1986:
    #ignore_extra_team = 1
    #if year != 1992 and year != 1994 and year != 2006 and year != 2018:
    number_of_interstate_sides_per_year.append(100 * (number_of_interstate_sides) / (total_sides - ignore_extra_team))
    n_i_s_p_y.append(number_of_interstate_sides)
    expected_finals_qualifiers_per_year.append((number_of_interstate_sides_per_year[-1] / 100) * finals_cutoff[-1])
    melbournian_averages.append(100 * statistics.mean(melboune_win_percentages))
    interstate_and_geelong_averages.append(100 * statistics.mean(interstate_win_percentages))
    victorian.append(100 * statistics.mean(just_victorian))
    interstate.append(100 * statistics.mean(just_interstate))
    if len(just_interstate_finals) > 0:
        interstate_finals.append(100 * statistics.mean(just_interstate_finals))
    else:
        interstate_finals.append(None)
    #victorian_finals.append(100 * statistics.mean(just_victorian_finals))
    total_standard_games += inter_standard_games
    total_finals += inter_finals_games
    all_inter_finals_wins += inter_inter_finals_wins
    all_inter_haa_wins += inter_inter_standard_wins
    all_inter_win_percentage_over_time.append(100 * (all_inter_haa_wins) / (total_standard_games))#all_inter_finals_wins, total_finals
    haagames_per_year.append(inter_standard_games)
    all_inter_home_games.append(inter_standard_home_games)
    finals_per_year.append(inter_finals_games)
    if total_finals > 0: finals_inter_win_percentage_over_time.append(100 * (all_inter_finals_wins) / (total_finals))
    print(year)
#"""
#print("hga test :", haa_home_side_advantage / haa_n_all_games)
"""
for club in current_clubs:
    for year in club._seasons:
        wins = 0
        for match_n, match in enumerate(club._seasons[year]._home_and_away_matches):
            if match._winner == club._name:
                wins += 1
            if match_n == 12:
                if wins == 12:
                    print(year, club._name)
                break
"""
"""
jackyboy = {
    1: {0:0, 1:0, 2:0}, 
    2: {0:0, 1:0, 2:0},
    3: {0:0, 1:0, 2:0},
    4: {0:0, 1:0, 2:0}
}
jackyboy1 = 0
jackyboy2 = 0
for club in current_clubs:
    for year in club._seasons:
        if year < 1980 or len(club._seasons[year]._home_and_away_matches) < 1 or club._seasons[year]._home_and_away_ladder_position > 4:
            continue
        for club2 in current_clubs:
            if club == club2 or len(club2._seasons[year]._home_and_away_matches) < 1 or club2._seasons[year]._home_and_away_ladder_position > 5:
                continue
            if club._seasons[year]._home_and_away_ladder_position < 3:
                if club2._seasons[year]._home_and_away_ladder_position == 3:
                    diff = club._seasons[year].n_home_and_away_wins - club2._seasons[year].n_home_and_away_wins
            elif club2._seasons[year]._home_and_away_ladder_position == 5:
                diff = club._seasons[year].n_home_and_away_wins - club2._seasons[year].n_home_and_away_wins
        print(club._name, year)
        # for match in club._seasons[year]._home_and_away_matches:
        #     print(match._winner)
        #print(club._seasons[year]._home_and_away_matches[-1]._winner, club._seasons[year]._home_and_away_matches[-2]._winner)
        losses = 0
        if club._seasons[year]._home_and_away_matches[-1]._winner != club._name:
            losses += 1
        if club._seasons[year]._home_and_away_matches[-2]._winner != club._name:
            losses += 1
        print(year, club._name, "had", losses, "/ 2 losses leading into finals and finished", club._seasons[year]._final_ladder_position)
quit()
""""""            
"""
"""
game_12_indicators = []
for year in years:
    if year < 2000 or year == 2020:
        continue
    for club in current_clubs:
        if year < club._year_entered_comp:
            continue
        name = club._name
        season = club._seasons[year]
        wins = 0
        for match_n, match in enumerate(season._home_and_away_matches):
            if name != match._home_team and name != match._away_team:
                continue
            if match._winner == name:
                wins += 1
            elif match._winner == DRAW:
                wins += 0.5
            if match_n == 11:
                game_12_indicators.append((wins, season._home_and_away_ladder_position, season.n_home_and_away_wins, (name, year)))
                if season._home_and_away_ladder_position < 5:
                    print(year, name, "End Year:", season.n_home_and_away_wins, ". Just Over Halfwayish In:", wins)
                    if wins == 13:
                        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!CHinpoku", year, name)
                elif wins > 6 and season._home_and_away_ladder_position > 4:
                    print("//////////////////// ", year, name, "started:", wins, "wins, ended up:", str(season._home_and_away_ladder_position) + "th,", season.n_home_and_away_wins, "wins")
                break
missers = [i[0] for i in game_12_indicators if i[0] > 6 and i[1] > 4]
print(len(missers))
collections3 = collections.Counter(missers)
print("12 games results bearing on missing top 4 finish:", collections3)
missers2 = [i[2] for i in game_12_indicators if i[1] > 4 and i[2] > 10]
print(len(missers2))
collections4 = collections.Counter(missers2)
print("22 games results bearing on missing top 4 finish:", collections4)
top4 = [i[2] for i in game_12_indicators if i[1] < 5]
collections2 = collections.Counter(top4)
print(len(top4))
#print(collections2.get())
print("22 games results bearing on top 4 finish:", collections2)
collections1 = collections.Counter([i[0] for i in game_12_indicators if i[1] < 5])
print("12 games results bearing on top 4 finish:", collections1)
print("Richmond 12 games in: 7 wins")
quit()
"""

x = years
y = melbournian_averages
y2 = interstate_and_geelong_averages
y3 = victorian
y4 = interstate
y5 = victorian_finals
y6 = interstate_finals
y7 = just_inter_games_vic_home
y8 = just_inter_games_inter_home
y9 = just_inter_games_vic_finals
y10 = just_inter_games_inter_finals
y_10_2 = [round(y10[i], 4) if y10[i] != None else 0.0 for i in range(len(y10)) if i + year_started in interstate_premierships]
y_10_3 = [round(y10[i], 4) for i in range(len(y10)) if i + year_started in interstate_v_vic_grand_finals]
y_11 = [100 * finals_qualifiers_per_year[i] / finals_cutoff[i] for i in range(len(x))]
y_12 = [(just_inter_games_inter_finals[i] / 100) * finals_per_year[i] if just_inter_games_inter_finals[i] != None else None for i in range(len(x))]

y_12_2 = [round(y_12[i], 4) if y_12[i] != None else 0.0 for i in range(len(y_12)) if i + year_started in interstate_premierships]
y_12_3 = [round(y_12[i], 4) for i in range(len(y_12)) if i + year_started in interstate_v_vic_grand_finals]
y_13 = [i / 2 for i in haagames_per_year]
y_14 = [(y8[i] / 100) * haagames_per_year[i] for i in range(len(x))]
y_15 = [] #Being used
x2 = [] #Being used

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xticks(range(1980, math.ceil(last_season / 5) * 5 + 1, 5))
ax.set_yticks(range(0, 111, 5))
ax.minorticks_on()
ax.grid(which='minor')
ax.grid(which='major', color="black")

#ax.plot(x, [50 for i in range(len(x))], 'k--')
'''ax.plot(x, y3, 'r', label="Victorian. Total avg: " + str(round(statistics.mean(victorian), 4)))
ax.plot(x, y4, 'b', label="Interstate. Total avg: " + str(round(statistics.mean(interstate), 4)))
ax.plot(x, y5, 'g', label="Victorian finals. Total avg: " + str(round(statistics.mean(victorian_finals), 4)))
ax.plot(x, y6, 'y', label="Interstate finals. Total avg: " + str(round(statistics.mean(interstate_finals), 4)))#'''
#ax.plot(x, y7, 'c', label="Victorian2. Total avg: " + str(round(statistics.mean(just_inter_games_vic_home), 4)))

ax.plot(x, haagames_per_year, color='k', label="Number of interstate v vic games during home and away season. Total games: " + str(total_standard_games))
ax.plot(x, y_14, color='lime', label="Number of interstate wins in such games. Total: " + str(all_inter_haa_wins) + " (" + str(round(100 * all_inter_haa_wins / total_standard_games, 4)) + '%, ' + str(total_standard_games / 2 - all_inter_haa_wins) + ' win(s) off 50%)')
#ax.plot(x, all_inter_home_games, color='saddlebrown', label="Number of home games. Total: " + str(sum(all_inter_home_games)) + " ( " + str(round( 100 * sum(all_inter_home_games) / total_standard_games, 4)) + "%)")

game_diff = [y_14[i] - y_13[i] for i in range(len(x))]
avg_game_diff = round(statistics.mean(game_diff), 3)
"""
diff_50 = [round(i, 2) for i in np.diff(np.array(game_diff)).tolist()]
avg = 3
moving_average = [round(i, 2) for i in pd.DataFrame(y_14).rolling(avg).mean()[0].tolist()[avg - 1:]]
start = math.floor((avg - 1) / 2)
stop = len(x) - start
ax.plot(x[start:stop], moving_average, color='brown', label="Rolling " + str(avg) + " year win avg")#
ax.plot(x, all_inter_win_percentage_over_time, 'crimson', label="Cumulative home and away win % 1982-> the point you're looking at.")
moving_average_diff = [round(i, 2) for i in np.diff(np.array(moving_average)).tolist()]
print(moving_average)
print(moving_average_diff)
print(statistics.mean(diff_50), diff_50)#year to year change in difference between wins and 50%, plus the avg of that
#ax.plot(x, list(map(abs, game_diff)), 'brown', label="Difference")
"""
k = 1
while abs(k * avg_game_diff) < n_i_s_p_y[-1]:
    k += 1
result_type = "loss(es)" if avg_game_diff < 0 else "win(s)"
ax.plot(x, y_13, color='orange', label="50%. Avg game diff to wins: " + str(avg_game_diff) + "/year. ~" + str(round(abs(k * avg_game_diff) / n_i_s_p_y[-1], 2)) + " extra h&a " + result_type + " / interstate club every " + str(k) + " year(s).")
#KEEP BELOW !                !                          !                                !                        !
print(y8)
"""
ax.plot(x, y8, 'm', label="Interstate v Vic during home and away season. Total games: " + str(total_standard_games) + ". Total wins: " +  str(all_inter_haa_wins) + ". Win %: " + str(round(100 * all_inter_haa_wins / total_standard_games, 4)))
#ax.plot(x, y9, 'darkorange', label="Victorian finals2. Total avg: " + str(round(statistics.mean(just_inter_games_vic_finals), 4)))
#ax.plot(x, all_inter_win_percentage_over_time, 'orange', label="Cumulative home and away win % 1982-> the point you're looking at.")
ax.plot(x[7:], y10[7:], 'lime', label="Interstate v Vic during finals. Total games: " + str(total_finals) + ". Total wins: " + str(all_inter_finals_wins) + ". Win %: " + str(round(100 * all_inter_finals_wins / total_finals, 4)))
#ax.plot(x[4:], finals_inter_win_percentage_over_time, 'forestgreen', label="Cumulative finals win % 1982-> the point you're looking at.")
ax.plot(x, y_11, color='orange', label="Percentage of finals participants that were interstate. Avg: " + str(round(statistics.mean(y_11), 4)))
ax.plot(x, number_of_interstate_sides_per_year, color='fuchsia', label="Percentage of finals participants expected to be interstate. Avg: " + str(round(statistics.mean(number_of_interstate_sides_per_year), 4)))#step..., where="post"..., linestyle='dashed'...grey...Percentage of league that's interstate. Also
ax.plot(x[4:7], y10[4:7], 'lime')
"""
#Below is a comparison of home ground win % in h&a games between three teams not selected at random
'''
y_11 = [100 * i[0] / i[1] for i in r_hg_record_haa]
y_12 = [100 * i[0] / i[1] for i in wc_hg_record_haa]
y_13 = [100 * i[0] / i[1] for i in g_hg_record_haa]
ax.plot(x[5:], y_11, 'yellow', label="Richmond")
print(wc_hg_record_haa)
ax.plot(x[5:], y_12, 'blue', label="WC")
ax.plot(x, y_13, 'red', label="Geelong")
print(statistics.mean(y_11), statistics.mean(y_12), statistics.mean(y_13))
print(statistics.mean([i[0] for i in r_hg_record_haa]), statistics.mean([i[0] for i in wc_hg_record_haa]))
'''

"""
h&a win record wc at the g 1986-2016: 42.555.
Richmond's record: 46.989, ~ 4 and 1/2 percent better.
Wc v Richmond at the g 1986-2016: 8-7 in WC favour. Current record 9-7 in Richmond's favour.
Wc record at subiaco 14-3 in their favour. At perth stadium (optus) 1-0 in their favour.
Total record (all venues) 26-19 in WC favour.
"""

"""
Richmond same year h&a losses v finals opponents 2017-2020
2017: Geelong by 14, GWS by 3, Adelaide by 76
2018: n/a.
Richmond beat Hawthorn by 13, Collingwood by 43 & 28. WC beat us by 47 points. Collingwood had 1 win v finalists pre finals.
2019: Geelong by 67 points, GWS by 49 points.
2020: SK by 26, PA by 21. 
Richmond beat Lions by 41.

Collingwood had 7 straight M.C.G. games in 2010 heading into finals.
Soz 4 all this, so much hate out their I need stats to remind me Richmond r halfway to decent.
"""

#Uncomment below to see WC specifically
'''ax.plot(x[5:], wc_home_and_away, 'aqua', label="WC H&A v victorians. Total games: " + str(all_wc_haa) + ". Total wins: " + str(all_wc_haa_wins) + ". Win %: " + str(round(100 * all_wc_haa_wins / all_wc_haa, 4)))
west_coast_finals_years_v_vic = [] 
#post 2020: 492 h&a games, 284.5 wins, 57.82%. 43 finals, 21.5 wins, 50%.
for i in x[5:]:
    if len(clubs["West Coast"]._seasons[i]._finals_matches) > 0:
        for j in clubs["West Coast"]._seasons[i]._finals_matches:
            if j._inter_match:
                west_coast_finals_years_v_vic.append(i)
                break
ax.plot(west_coast_finals_years_v_vic, west_coast_finals_wins_per_year, 'g', label="WC finals v victorians. Total games: " + str(all_west_coast_finals_v_vic) + "Total wins: " + str(WC_inter_finals_wins) + ". Win %: " + str(round(100 * WC_inter_finals_wins / all_west_coast_finals_v_vic, 2)))#'''

plt.legend()
plt.xlabel('Years')
#plt.ylabel('Percentage')

"""
ax2 = ax.twiny()
ax2.set_xlim(ax.get_xlim())
ax2.set_xticks(x)
ax2.set_xticklabels(haagames_per_year)

ax3 = ax.twiny()
ax3.set_xlim(ax.get_xlim())
ax3.set_xticks(x)
ax3.tick_params(pad=14.0)
ax3.set_xticklabels(finals_per_year)
"""

'''
ax4 = ax.twiny()
ax4.set_xlim(ax.get_xlim())
ax4.set_xticks(x)
ax4.tick_params(pad=24.0)
ax4.set_xticklabels(finals_qualifiers_per_year)
'''

plt.title('Interstate v vic in home and away games ' + str(year_started) + "-" + str(last_season))

# for i in current_clubs:
#     if i._name == "Fitzroy":
#         continue
#     club_haa_inter_games = []
#     club_haa_inter_wins = []
#     for season in i._seasons:
#         number_of_inter_games = 0
#         number_of_inter_wins = 0
#         for match in i._seasons[season]._home_and_away_matches:
#             if match._inter_match:
#                 number_of_inter_games += 1
#                 if match._winner == DRAW:
#                     number_of_inter_wins += 0.5
#                 elif clubs[match._winner] == i:
#                     number_of_inter_wins += 1
#         club_haa_inter_games.append(number_of_inter_games)
#         club_haa_inter_wins.append(number_of_inter_wins)
#     half = [n_games / 2 for n_games in club_haa_inter_games]
#     total_games = sum(club_haa_inter_games)
#     total_wins = sum(club_haa_inter_wins)
#     figE = plt.figure()
#     axE = figE.add_subplot(111)
#     axE.set_xticks(range(1980, math.ceil(last_season / 5) * 5 + 1, 5))
#     axE.set_yticks(range(0, 25, 5))
#     axE.minorticks_on()
#     axE.grid(which='minor')
#     axE.grid(which='major', color="black")
#     axE.plot(x, club_haa_inter_games, color='k', label="Number of interstate v vic games during home and away season. Total games: " + str(total_games))
#     wind_diff = total_games / 2 - total_wins
#     result_type = "loss(es)" if wind_diff < 0 else "win(s)"
#     axE.plot(x, club_haa_inter_wins, color='lime', label="Wins. Total: "+ str(total_wins) + " (" + str(round(100 * total_wins / total_games, 4)) + '%, ' + str(abs(wind_diff)) + ' ' + result_type + ' off 50%)')
#     axE.plot(x, half, color='orange', label="50%. Avg game diff to wins: ")# + str(avg_game_diff) + "/year. ~" + str(round(abs(k * avg_game_diff) / n_i_s_p_y[-1], 2)) + " extra h&a " + result_type + " / interstate club every " + str(k) + " year(s).")
#     plt.legend()#[x.index(i._year_entered_comp) if i._year_entered_comp >= year_started else 0:]
#     plt.xlabel('Years')
#     plt.title(i._name)
# plt.show()
# quit()

fig3 = plt.figure()
az = fig3.add_subplot(111)
az.set_xticks(range(1980, math.ceil(last_season / 5) * 5 + 1, 5))
az.set_yticks(range(11))
az.minorticks_on()
az.grid(which='minor')
az.grid(which='major', color="black")
az.plot(x, finals_per_year, color='k', label="Number of Interstate v Vic finals. Total games: " + str(total_finals))
az.plot(x[7:], y_12[7:], 'lime', label="Wins. Total: " + str(all_inter_finals_wins) + " (" + str(round(100 * all_inter_finals_wins / total_finals, 4)) + "%, " + str(total_finals / 2 - all_inter_finals_wins) + " win(s) off 50%)")
az.plot(x, [i / 2 for i in finals_per_year], color='orange', label="50%")
az.plot(x[4:7], y_12[4:7], 'lime')
interstate_vic_gf_wins = len(list(set(interstate_v_vic_grand_finals) & set(interstate_premierships)))
az.scatter(interstate_v_vic_grand_finals, y_12_3, c='r', s=110.0, label="Interstate v Vic grand finals. Total: " + str(len(y_10_3)) + ". Wins: " + str(interstate_vic_gf_wins) + " (" + str(round(100 * len(list(set(interstate_v_vic_grand_finals) & set(interstate_premierships))) / len(y_10_3), 4)) + "%, " + str(len(y_10_3) / 2 - interstate_vic_gf_wins) + " win(s) off 50%)")
az.scatter(interstate_premierships, y_12_2, c='blue', label="Interstate premierships.")

plt.legend()
plt.xlabel('Years')
#plt.ylabel('Games')
plt.title('Interstate v vic in finals games ' + str(year_started) + "-" + str(last_season))
number_of_interstate_sides

fig4 = plt.figure()
aa = fig4.add_subplot(111)
aa.set_xticks(range(1980, math.ceil(last_season / 5) * 5 + 1, 5))
aa.minorticks_on()
aa.grid(which='minor')
aa.grid(which='major', color="black")

aa.plot(x, finals_cutoff, color='k', label="Number of sides allowed to play finals.")
aa.plot(x, n_i_s_p_y, color='dimgrey', label="Number of interstate sides.")
aa.plot(x, expected_finals_qualifiers_per_year, color='fuchsia', label="Number of interstate sides expected to be playing finals. Total expected qualifications: " + str(round(sum(expected_finals_qualifiers_per_year), 3)))#brown
aa.plot(x, finals_qualifiers_per_year, color='purple', label="Number of interstate sides that played finals. Total qualifications: " + str(sum(finals_qualifiers_per_year)))

#aa.plot(x, [statistics.mean(i) if len(i) > 0 else 0 for i in finalists_ladder_positions], color='deepskyblue', label="Mean ladder position. Mean: " + str(round(statistics.mean([statistics.mean(i) if len(i) > 0 else 0 for i in finalists_ladder_positions]), 3)))#[9 - j for j in i]
#aa.plot(x, [statistics.median([9 - j for j in i]) if len(i) > 0 else 0 for i in finalists_ladder_positions], color='cyan', label="Median ladder position. Median: " + str(round(statistics.median([statistics.median([9 - j for j in i]) if len(i) > 0 else 0 for i in finalists_ladder_positions]), 3)))

plt.legend()
plt.xlabel('Years')
"""
aa2 = aa.twinx()
aa2.set_ylim(aa.get_ylim())
#aa2.set_yticks(y)
aa2.set_yticklabels(range(9, 0, -1))
"""
#plt.ylabel('Games')
plt.title('Quantity of interstate finals series qualifications ' + str(year_started) + "-" + str(last_season))




fig5 = plt.figure()
ab = fig5.add_subplot(111)
ab.set_xticks(range(1980, math.ceil(last_season / 5) * 5 + 1, 5))
ab.minorticks_on()
ab.grid(which='minor')
ab.grid(which='major', color="black")

actual_positions_progression = {1: [0], 2: [0], 3: [0], 4: [0], 5: [0], 6: [0], 7: [0], 8: [0], 9:[0], 10:[0], 11:[0], 12:[0], 13:[0], 14:[0], 15:[0], 16:[0], 17:[0], 18:[0]}

for i in range(len(x)):
    if len(finalists_ladder_positions[i]) > 0 and finalists_ladder_positions[i][0] != -1:
        x2 += [x[i] for j in range(len(finalists_ladder_positions[i]))]
        y_15 += finalists_ladder_positions[i]
    for j in range(1, 9):
        to_add = 1 if j in finalists_ladder_positions[i] else 0
        actual_positions_progression[j].append(actual_positions_progression[j][-1] + to_add)
    
#aa.scatter(x2, y_15, c='deepskyblue', label="Ladder positions in year. Avg/year: " + str(round(statistics.mean([statistics.mean(i) for i in finalists_ladder_positions if len(i) > 0]), 3)))

total_positions = dict(collections.Counter(y_15))
total_expected_positions = {1: [0], 2: [0], 3: [0], 4: [0], 5: [0], 6: [0], 7: [0], 8: [0], 9:[0], 10:[0], 11:[0], 12:[0], 13:[0], 14:[0], 15:[0], 16:[0], 17:[0], 18:[0]}
#total_expected_positions_per_year = [[] for i in range(8)] [[[]#for j in range(finals_cutoff[i])] for i in range(len(x))]

non_finalists_positions = {}
adding_it_all_up = []
for i in non_finalists_ladder_positions:
    adding_it_all_up += i 
total_non_finalists_positions = dict(collections.Counter(adding_it_all_up))
print(non_finalists_ladder_positions)
"""
for i in range(len(x)):
    for i in interstate_clubs:
        for j in range(9, 1 + round(1 / (number_of_interstate_sides_per_year[i] / 100 / n_i_s_p_y[i])))
            to_add = 1 if j in finalists_ladder_positions[i] else 0
            non_finalists_positions[j].append(non_finalists_positions[-1] + non_finalists_ladder_positions[i])
"""
#"""UNCOMMENT THIS ONE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
for i in range(len(x)):
    #print(Sydney._seasons[x[i]]._teams_in_season)
    for j in range(1, Sydney._seasons[x[i]]._teams_in_season + 1):
        if j == 19:
            print(19)
            continue
        #if j > finals_cutoff[i]:
        if j <= finals_cutoff[i]:
            total_expected_positions[j].append(total_expected_positions[j][-1] + number_of_interstate_sides_per_year[i] / 100)
        else:
            total_expected_positions[j].append(total_expected_positions[j][-1])
        #total_expected_positions_per_year[]
for i in range(1, 9):#19
    total_expected_positions[i] = total_expected_positions[i][1:]
    if i <= 8:
        actual_positions_progression[i] = actual_positions_progression[i][1:]

for i in total_non_finalists_positions.keys():
    actual_positions_progression[i][-1] += total_non_finalists_positions[i]

#differences_per_position = [actual_positions_progression[i][-1] - total_expected_positions[i][-1] for i in range(1, 9)]
#actual_positions_2 = [round(total_expected_positions[i][-1], 3) for i in range(1, 19)]
total_non_finalists_positions[6] = 0
#differences_2 = [(i, round(actual_positions_progression[i][-1] - total_expected_positions[i][-1], 3)) for i in range(1, 19)]
print(total_non_finalists_positions)
printable_total_expected_positions = [round(total_expected_positions[i][-1], 3) for i in range(6, 19)]
print(printable_total_expected_positions)
differences_3 = [(i, round(total_non_finalists_positions[i] - total_expected_positions[i][-1], 3)) for i in range(6, 19)]
print(differences_3, sum([i[1] for i in differences_3]), sum([i[1] for i in differences_3][:4]))
#print(actual_positions_2)
#print(differences_2, sum([i[1] for i in differences_2][:]))

'''
print(total_expected_positions)
print(total_positions)
print(actual_positions_progression)
print(differences_per_position)
print(sum(differences_per_position))
'''

ab.set_yticks(range(max([math.ceil(i[-1]) for i in total_expected_positions.values()]) + 1))
colours = {5:"yellow", 3:"royalblue", 2:"red", 7:"navy", 1:"black", 4:"lime", "Hawthorn":"brown", "Fitzroy":"grey", "St Kilda":"crimson", "Western Bulldogs":"green", 6:"purple", 8:"orange", "Brisbane Lions": "orangered", -1:"cyan", -2:"darkgoldenrod", -3:"deeppink", "Adelaide":"royalblue"} #ugh takes so long to write out
#ab.plot(x, finals_cutoff, color='k', label="Number of sides allowed to play finals.")
ab.set_prop_cycle(color=colours[-1])
ab.plot(x, total_expected_positions[5], label="Number of times expected to place in ladder positions 1-5. Total: " + str(round(total_expected_positions[5][-1], 3)) + "ea")
ab.set_prop_cycle(color=colours[-2])
ab.plot(x, total_expected_positions[6], label="Number of times expected to place in ladder position 6. Total: " + str(round(total_expected_positions[6][-1], 3)))
ab.set_prop_cycle(color=colours[-3])
ab.plot(x, total_expected_positions[7], label="Number of times expected to place in ladder positions 7 & 8. Total: " + str(round(total_expected_positions[7][-1], 3)) + "ea")

for i in range(8, 0, -1):
    ab.set_prop_cycle(color=colours[i])
    ab.plot(x, actual_positions_progression[i], label="Progression of times placed in ladder position " + str(i) + ". Total: " + str(actual_positions_progression[i][-1]))#, where='post'

plt.legend()
plt.xlabel('Years')
plt.title('Quality of interstate finals series qualifications ' + str(year_started) + "-" + str(last_season))
#"""


"""
Conclusions from this first graph is:
I write this precedeeing the 2021 season. So as of now, interstate sides have
1. Appeared in 21/31 grand finals.
1.1. Not sure how many they should have appeared in and won, as that must be a funciton of
    percentage of how many interstate teams were in the comp at every stage
2. Won 12/21 of those appearances, for 12/31 premierships. This is despite the
    fact that they represent just under half of all sides (8/18) since 2012, growing
    sporadically from the 3/14 sides that were present in 1990.
3. 18/21 grand finals have been against vic sides.
4. Have won 9/18 of those grand finals. 
5. Interestingly, won 7/9 (includes brisbane 3-peat) from first half of those grand finals and 
    lost 7/9 (includes hawks 3-peat) of grand finals since.
6. They win 1.6% less of their games against the vics during the home and away season. 
7. THey win 0.65% less of their games against the vics during the finals series.
7.1. They are 74-1-76 in finals v vics! How is that not even?
8. Unfortunately, even though there is 30 years being considered, the trends of who is
    better seem to be too long to make any guesses as to how long an 'ascendancy' will last.
    One could hypothesise that the extent of an ascendancy will be matched at its conclusion, as
    happenned when the 2002-2007 interstate ascendancy was followed by the 2008-2013 vic ascendancy.
    I think in light of the closeness of the numbers we can safely say that these were just extended
    streaks of flipping heads though.
8.1. The significance of history depends on where you're standing in it. If I'd done this just after
    2006, I would have seen the same home and away and finals win percentages, but 10 premierships to
    an expected 6.72!, interstaters went 10/12 gfs!!!!!!!! We'd all be here trying to figure out what
    it was about grand final day that made interstate sides so much more likely to win it than
    victorians. If I'd analysed starting in "the AFl era (1990)", win percentage home and away would be
    about the same, win percentage in finals would be up 2%, expected premierships down 1 (and gfs 2).
    As it is, interstaters need 1 more to square up the ledger. The worst the interstaters have been in
    premierships v expected premierships was 0:1.54 in '91. I conclude this shows that interstate sides
    have been consistently winning exactly as many premierships as they would be expected to win,
    regardless of whether they're an interstate side or not. 
    But we could just as easily launch from here into an extended period of interstate or victorian
    dominance. I'll just have to keep faith that it'll all be squared up in the end.
9. Interstate sides do lose more finals and home and away games then they are expected to though.
    1.6% more h&a games. That's 1.6% * 8 * 22 * (% of 22 games played against vics, changes every year)
    more losses / season for interstate teams.

    151 vic v interstate finals. 1 (3? 5?) draw and 74 interstate wins, == 1 loss caused by an interstate
    side so far. That's congruent with what you'd expect if there was 0 difference in finals between
    interstate and vic teams.
    
    There's a lot less data on the finals than the home and away games of course, so it's more
    malleable to change. But seeing as how it was 45-50 % in all the above years
    I checked (I think) except for '91 (17.5%! We'd all be sitting here trying to figure out what it
    was about finals that made interstate sides so much more likely to lose them), I'd think it's
    fairly strong/correct/reasonable.
10. 1990 && not first year 49.37, 50.1 (51?). 1990 && not first 3 years
11. Three times # "home" games were uneven: 1997 +1 interstate, 2020 +"4" interstate and for what I can
    only believe was an easter egg reason by the scheduler put there for nerds like me who bothered to
    check, 2015 when for the first and so far only ever time in 40 years of scheduling interstate v vic
    games, the AFL decided to schedule an odd number of games, and rounded the resulting .5 remainder
    down in favour of the vics.
    edit: turns out it was rescheduling cos of the then Adelaide coach Phil Walsh's untimely and
    unfortunate passing, may he rest in peace.
"""


k = len(number_of_interstate_sides_per_year)
expected_premierships_per_year = [1 / 12] * k
z = 0
premierships_per_year = []
for i in x:
    if z < len(interstate_premierships) and i == interstate_premierships[z]:
        z += 1
    premierships_per_year.append(z)
    #if z == len(interstate_premierships):
    #    continue
for i in range(0, k):#1 instead of 0??
    expected_premierships_per_year[i] = expected_premierships_per_year[i - 1] + number_of_interstate_sides_per_year[i] / 100
premierships_compared_to_progression = [100 * premierships_per_year[i] / expected_premierships_per_year[i] for i in range(k)]
premierships_compared_to_rounded_progression = [100 * premierships_per_year[i] / round(expected_premierships_per_year[i]) if round(expected_premierships_per_year[i]) != 0 else 1 for i in range(k)]
'''diff = [(expected_premierships_per_year[i] - premierships_per_year[i]) ** 2 for i in range(k)]
r_squared = 0'''
#ax.step(x, premierships_compared_to_progression, color="blue", linestyle="dashed", label="Yearly Progression of Premierships / Expected Premierships")
fig2 = plt.figure()
ay = fig2.add_subplot(111)
ay.set_xticks(range(1980, math.ceil(last_season / 5) * 5 + 1, 5))
ay.minorticks_on()
ay.grid(which='minor')
ay.grid(which='major', color="black")
#ay.step(x, premierships_compared_to_rounded_progression, color="blue", linestyle="dashed", label="Yearly Progression of Premierships / Rounded Expected Premierships")
#ay.plot(x, expected_finals_qualifiers_per_year, color='brown', label="Number of interstate sides expected to be playing finals.")
#ay.plot(x, finals_qualifiers_per_year, color='c', label="Number of interstate sides that played finals.", where='post')

expected_interstate_premierships = sum(number_of_interstate_sides_per_year) / 100
whichevers_higher = math.ceil(expected_interstate_premierships) if math.ceil(expected_interstate_premierships) > len(interstate_premierships) else len(interstate_premierships)
ay.set_yticks(range((whichevers_higher + 1) * 2))
#print(expected_interstate_premierships)
print(premierships_per_year, interstate_premierships, expected_premierships_per_year)
#crimson
z = 0
interstate_grand_finals = list(set(interstate_v_vic_grand_finals) | set(interstate_premierships))
interstate_v_interstate_grand_finals = list((set(interstate_v_vic_grand_finals) & set(interstate_premierships)) ^ set(interstate_premierships))
grand_finals_per_year = []
for i in x:
    if i in interstate_grand_finals:
        z += 1
        if i in interstate_v_interstate_grand_finals:
            z += 1
    grand_finals_per_year.append(z)
ay.plot(x, [2 * i for i in expected_premierships_per_year], color='r', label="Expected / and actual _| grand final appearances for all together / (Expected: " + str(round(2 * expected_interstate_premierships, 2)) + ", Actual: " + str((len(list((set(interstate_v_vic_grand_finals) & set(interstate_premierships)) ^ set(interstate_premierships))) + len(list(set(interstate_v_vic_grand_finals) | set(interstate_premierships))))) + ')')#, where='post'
ay.step(x, grand_finals_per_year, color='r', where='post')
ay.plot(x, expected_premierships_per_year, color='b', label="Expected / and actual _| premierships for all together (Expected: " + str(round(expected_interstate_premierships, 2)) + ", Actual: " + str(len(y_10_2)) + ')')#, where='post'
ay.step(x, premierships_per_year, color='b', where='post')
colours = {"Gold Coast":"yellow", "Richmond":"yellow", "Geelong":"royalblue", "North Melbourne":"royalblue", "Essendon":"red", "Carlton":"navy", "Collingwood":"black", "Melbourne":"lime", "Hawthorn":"brown", "Fitzroy":"grey", "St Kilda":"crimson", "Western Bulldogs":"green", "Fremantle":"purple", "Greater Western Sydney":"orange", "Brisbane Lions": "orangered", "Port Adelaide":"cyan", "West Coast":"goldenrod", "Sydney":"deeppink", "Adelaide":"royalblue"} #ugh takes so long to write out
#ab.plot(x, finals_cutoff, color='k', label="Number of sides allowed to play finals.")
for i in current_clubs:
    if i._interstate:
        ay.set_prop_cycle(color=colours[i._name])
        if i._name == "Fitzroy":
            ay.plot(x[x.index(i._year_entered_comp) if i._year_entered_comp >= year_started else 0:15], i._expected_premierships[:15], label="Expected / and actual _| premierships for " + i._name + " (Expected: " + str(round(i._expected_premierships[-1], 2)) + ", Actual: " + str(i._premierships[-1]) + ')')#, where='post'
            ay.step(x[x.index(i._year_entered_comp) if i._year_entered_comp >= year_started else 0:15], i._premierships[:15], where='post')
            continue
        ay.plot(x[x.index(i._year_entered_comp) if i._year_entered_comp >= year_started else 0:], i._expected_premierships, label="Expected / and actual _| premierships for " + i._name + " (Expected: " + str(round(i._expected_premierships[-1], 2)) + ", Actual: " + str(i._premierships[-1]) + ')')#, where='post'
        ay.step(x[x.index(i._year_entered_comp) if i._year_entered_comp >= year_started else 0:], i._premierships, where='post')


plt.legend()
plt.xlabel('Years')
plt.ylabel('Premierships')
plt.title('Progression of Interstate Premierships ' + str(year_started) + "-" + str(last_season))

#quit()
plt.show()