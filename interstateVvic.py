#help("modules") #
import urllib.request
import matplotlib.pyplot as plt
import statistics
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup


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
universalURL = 'https://afltables.com/afl/seas/{}.html' 
year_started = 1982#1990 #1897
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
        """Returns w/l record of 5 rounds immediately before selected one"""
        if round < 5:
            return [0, 0, 0, 0, 0]
        return []
    def do_calcs(self):
        return

class Club(object):
    def __init__(self, name, home_grounds, interstate):
        """Club(str, str)"""
        self._name = name
        self._colour = colours[name]
        self._home_grounds = home_grounds
        self._interstate = interstate
        self._seasons = {}
    #def get_season(self, year):
    #    return self._seasons[year - 2000]

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

class Match(object):
    def __init__(self, home_team, away_team, home_team_score, away_team_score, venue):
        self._home_team = home_team
        self._away_team = away_team
        self._home_team_score = home_team_score
        self._away_team_score = away_team_score
        self._margin = home_team_score - away_team_score
        self._winner = "draw"
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

for year in range(year_started, this_season + 1):
    print(year)
    text = getURL(universalURL.format(year))
    soup = BeautifulSoup(text, 'html.parser')
    tables = soup.findAll('table')
    last_season = this_season# int(tables[0].find('tr').find('a').text) - 1
    tables.reverse()
    current_clubs = set(clubs.values())
    #create seasons for every club
    for i in current_clubs:
        i._seasons[year] = Season(year)
    x = 0
    #do finals first
    inter_inter_finals_wins = 0
    inter_finals_games = 0
    inter_inter_standard_wins = 0
    inter_standard_games = 0
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
        #If this is the gf and its not a draw and at least one of the teams is interstate
        if team1_score != team2_score and (clubs[team1]._seasons[year]._final_ladder_position == 1 or clubs[team2]._seasons[year]._final_ladder_position == 1) and (clubs[team1]._interstate or clubs[team2]._interstate):
            if (clubs[team1]._interstate and not clubs[team2]._interstate) or (clubs[team2]._interstate and not clubs[team1]._interstate):
                interstate_v_vic_grand_finals.append(year)
            if clubs[match._winner]._interstate:
                interstate_premierships.append(year)
        if tables[x + 2].text == "Finals":
            break
        x += 2
        continue
        finals_lookout = True
        rows = i.findAll('tr')
        year = int(rows[0].find('a').text)
        nTeams = len(rows) - 2
        teams_in_comp.append(nTeams)
        for k in range(2, nTeams + 2):
            club = rows[k].find('a').text
            if club == "Kangaroos":
                club = "North Melbourne"
            elif club == "Brisbane Bears":
                club = "Brisbane Lions"
            elif club == "Footscray":
                club = "Western Bulldogs"
            elif club == "South Melbourne":
                club = "Sydney"
            position = k - 1
            teams.setdefault(club, [[], []])[0].append(year)
            teams[club][1].append(position)
            if finals_lookout and k > 2 and not(rows[k].findAll('td')[-1] in rows[k].findAll('td', {"bgcolor":"#ffccff"})):
                finals_lookout = False
                finals_cutoff.append(position - 1)
            #should i record premiership or last place?
    rows = BeautifulSoup(getURL(universalURL.format(year)), features="lxml").findChildren('table')[-x - 4].findChildren('tr')[2:-1]
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
        if match._inter_match:
            inter_standard_games += 1
            if team1_score != team2_score and clubs[match._winner]._interstate:
                inter_inter_standard_wins += 1
        clubs[team1]._seasons[year]._total_matches.append(match)
        clubs[team1]._seasons[year]._home_and_away_matches.append(match)
        clubs[team2]._seasons[year]._total_matches.append(match)
        clubs[team2]._seasons[year]._home_and_away_matches.append(match)
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
            if i._interstate:
                number_of_interstate_sides += 1
                interstate_win_percentages.append(season._home_and_away_win_percentage)
                if len(season._finals_matches) > 0:
                    if i == Geelong:
                        just_victorian_finals.append((season._n_total_wins - season.n_home_and_away_wins) / len(season._finals_matches))
                    else:
                        just_interstate_finals.append((season._n_total_wins - season.n_home_and_away_wins) / len(season._finals_matches))
                if i != Geelong:
                    just_interstate.append(season._home_and_away_win_percentage)
                else:
                    just_victorian.append(season._home_and_away_win_percentage)
            else:
                melboune_win_percentages.append(season._home_and_away_win_percentage)
                just_victorian.append(season._home_and_away_win_percentage)
                if len(season._finals_matches) > 0:
                    just_victorian_finals.append((season._n_total_wins - season.n_home_and_away_wins) / len(season._finals_matches))
    number_of_interstate_sides_per_year.append(100 * number_of_interstate_sides / total_sides)
    melbournian_averages.append(100 * statistics.mean(melboune_win_percentages))
    interstate_and_geelong_averages.append(100 * statistics.mean(interstate_win_percentages))
    victorian.append(100 * statistics.mean(just_victorian))
    interstate.append(100 * statistics.mean(just_interstate))
    if len(just_interstate_finals) > 0:
        interstate_finals.append(100 * statistics.mean(just_interstate_finals))
    else:
        interstate_finals.append(None)
    victorian_finals.append(100 * statistics.mean(just_victorian_finals))

'''
#MAIN:
means = []
modes = []
medians = []
count = 1
for i in teams:
    if i == "Fitzroy":
        continue
    year_began = teams[i][0][0]
    start_diff = year_began - year_started
    x = teams[i][0]
    y = teams[i][1]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_prop_cycle(color=running_colours)
    ax.step([i for i in range(year_began, year_began + len(teams_in_comp[start_diff:]))], teams_in_comp[start_diff:], 'k--', label="Teams In Comp", where="post")
    ax.plot(x, y, label="Position")#, where='mid'
    ax.scatter(x, y)
    ax.invert_yaxis()
    avg_in_comp = []
    team_stats = []
    start_place = start_diff
    skipped = 0
    index = start_diff - 1
    yindex = 0
    for k in teams_in_comp[start_diff:]:
        index += 1
        skipped += 1
        if x[yindex] == year_began + index - start_diff:
            team_stats.append(y[yindex])
            yindex += 1
        else:
            team_stats.append(y[yindex - 1])
        if k == teams_in_comp[start_place] and index != len(teams_in_comp) - 1:
            continue
        avg_in_comp += skipped * [statistics.mean(team_stats)]
        team_stats = []
        start_place = index
        skipped = 0
    ax.step([i for i in range(year_began, year_began + len(teams_in_comp[start_diff:]))], avg_in_comp, 'g--', label="Average Ladder Position In Era", where="pre")
    ax.step(x, [statistics.mean(y)] * len(x), 'y--', label="Average Ladder Position All Time")# don't have?
    ax.step([i for i in range(year_began, year_began + len(finals_cutoff[start_diff:]))], finals_cutoff[start_diff:], 'r--', label="Finals Cutoff", where="post")
    index = 0
    addon = 0
    years_played_finals = [year_began]
    for k in range(start_diff, len(finals_cutoff)):
        if year_started + k != teams[i][0][index]:
            continue
        if finals_cutoff[k] >= teams[i][1][index]:
            years_played_finals.append(teams[i][0][index])
        index += 1
    if years_played_finals[-1] != last_season and len(years_played_finals) > 1:
        years_played_finals.append(last_season)
        addon += 1
    if years_played_finals[0] == year_began:
        years_played_finals.remove(year_began)
    frock = np.diff(np.array(years_played_finals)).tolist()
    years_between_finals = [i for i in frock if i > 1]
    
    finals_lengths = []
    length = 1
    for k in range(len(frock)):
        if frock[k] == 1:
            length += 1
            if k == len(frock) - 1:
                finals_lengths.append(length)
        elif length != 0:
            finals_lengths.append(length)
            length = 1
    if len(years_played_finals) == 0:
        years_between_finals = [last_season - year_began]
        finals_lengths = [-1]
    if len(years_between_finals) == 0:
        years_between_finals = [years_played_finals[0] - year_began]
    
    print(i) 
    
    print(frock)
    print(years_played_finals)
    print(years_between_finals)
    print(finals_lengths)
    ladder_moves = np.diff(np.array(y)).tolist()#map takes a function nad applies it to every item in a list
    abs_ladder_moves = list(map(abs, ladder_moves))
    print(sorted(abs_ladder_moves))
    avg_ladder_move = statistics.mean(abs_ladder_moves)
    means.append(avg_ladder_move)
    modes.append(statistics.mode([round(k) for k in abs_ladder_moves]))
    medians.append(statistics.median(abs_ladder_moves))
    print(avg_ladder_move)
    averages = []
    for k in range(1, len(y)):
        averages.append(round(statistics.mean(y[:k]), 2))
    
    """ 
    maybe if avg of next 3 data points greater than everage of last 3 by certain amount then break
    cos adhusting avg and the val abs(val must be > isnt working)
    """
    avg = 4
    moving_average = [round(i, 2) for i in pd.DataFrame(y).rolling(avg).mean()[0].tolist()[avg - 1:]]
    #print(moving_average)
    moving_average_diff = np.diff(np.array(moving_average)).tolist()
    print(moving_average_diff)
    size = len(moving_average_diff)
    idx_list = [idx + 1 for idx, val in
            enumerate(moving_average_diff) if abs(val) > 2.5]  
    res = []
    if len(idx_list) != 0:
        res = [moving_average_diff[i: j] for i, j in
            zip([0] + idx_list, idx_list + 
            ([size] if idx_list[-1] != size else []))]
        total_before = avg - 1
        for k in res:
            x2 = [x[total_before], x[total_before + len(k)]]
            y2 = [statistics.mean(y[total_before:total_before + len(k)]), statistics.mean(y[total_before:total_before + len(k)])]#[y[total_before], y[total_before + len(k)]]
            ax.plot(x2, y2, 'm--')
            total_before += len(k)
        print(x[total_before])
    
    print(statistics.mean(moving_average))
    #ax.plot(x[avg - 1:], moving_average)
    #ax.scatter(x[avg - 1:], moving_average)
    print(res)
    """
    for k in res:
        ax.plot([j for j in range(x, len(k))])
    """
    """ ugh finals clusters is so much work
    finals_clusters = []
    last = years_played_finals[0]
    record = [last]
    for k in years_played_finals[1:]:
        if k - last < 3:
            record.append(k)
            last = k
            if k != 
    """
    ax.set_xticks([i for i in range(year_began - year_began % 10, (last_season + (last_season % 10) + 10), 10)])
    ax.set_yticks([i for i in range(19)])
    plt.ylabel('Ladder Position')    
    plt.xlabel('Years')
    plt.legend()
    plt.title(
        i +
        ", times played finals: " + 
        str(len(years_played_finals) - addon) + 
        ", average sretch of finals droughts: " + 
        str(round(statistics.mean(years_between_finals), 2)) + 
        ", average stretch of successive finals: " + 
        str(round(statistics.mean(finals_lengths), 2))
     )
    ax.minorticks_on()
    ax.grid(which='minor')
    ax.grid(which='major', color="black")
    count += 1
    #break
print(means)
print(modes)
print(medians)
print(statistics.mean(means))
print(statistics.mean(modes))
print(statistics.mean(medians))
'''

x = range(year_started, last_season + 1)
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
y_10_2 = [round(y10[i], 4) for i in range(len(y10)) if i + year_started in interstate_premierships]
y_10_3 = [round(y10[i], 4) for i in range(len(y10)) if i + year_started in interstate_v_vic_grand_finals]
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xticks(range(year_started, last_season + 1), 5)
ax.set_yticks(range(0, 101, 5))
ax.minorticks_on()
ax.grid(which='minor')
ax.grid(which='major', color="black")
#ax.set_prop_cycle(color=running_colours)
#ax.step([i for i in range(year_began, year_began + len(teams_in_comp[start_diff:]))], teams_in_comp[start_diff:], 'k--', label="Teams In Comp", where="post")
ax.plot(x, [50 for i in range(len(x))], 'k--')
'''ax.plot(x, y3, 'r', label="Victorian. Total avg: " + str(round(statistics.mean(victorian), 4)))
ax.plot(x, y4, 'b', label="Interstate. Total avg: " + str(round(statistics.mean(interstate), 4)))
ax.plot(x, y5, 'g', label="Victorian finals. Total avg: " + str(round(statistics.mean(victorian_finals), 4)))
ax.plot(x, y6, 'y', label="Interstate finals. Total avg: " + str(round(statistics.mean(interstate_finals), 4)))#'''
#ax.plot(x, y7, 'c', label="Victorian2. Total avg: " + str(round(statistics.mean(just_inter_games_vic_home), 4)))
ax.step(range(year_started, last_season + 1), number_of_interstate_sides_per_year, color='grey', linestyle='dashed', label="Percentage of Comp that's interstate", where="post")
ax.plot(x, y8, 'm', label="Interstate v Vic during home and away season. " + str(len(x)) + " yr total avg: " + str(round(statistics.mean(just_inter_games_inter_home), 4)))
#ax.plot(x, y9, 'darkorange', label="Victorian finals2. Total avg: " + str(round(statistics.mean(just_inter_games_vic_finals), 4)))
ax.plot(x[4:7], y10[4:7], 'lime')
ax.plot(x[7:], y10[7:], 'lime', label="Interstate v Vic during finals. " + str(len(x)) + " yr total avg: " + str(round(statistics.mean([i for i in just_inter_games_inter_finals if i != None]), 4)))
#print(interstate_v_vic_grand_finals)
#print(y_8_2)
ax.scatter(interstate_v_vic_grand_finals, y_10_3, c='r', s=110.0, label="Interstate v vic gfs. Total: " + str(len(y_10_3)) + ". Total gf appearances (expected is twice below #): " + str(len(list(set(interstate_v_vic_grand_finals) | set(interstate_premierships))) + len(list(set(interstate_v_vic_grand_finals) & set(interstate_premierships)))))
ax.scatter(interstate_premierships, y_10_2, c='b', label="Interstate premierships. Total: " + str(len(y_10_2)) + ". Expected given # interstate teams in comp ea year: " + str(round(sum(number_of_interstate_sides_per_year) / 100, 2)))
#ax.plot(x, y, 'g', label="Melbourne " + str(round(statistics.mean(melbournian_averages), 4)))
#ax.plot(x, y2, 'y', label="Interstate and geelong " + str(round(statistics.mean(interstate_and_geelong_averages), 4)))
#ax.scatter(x, y)
#ax.scatter(x, y2)
#ax.scatter(x, y)
#ax.invert_yaxis()
plt.legend()
plt.xlabel('Years')
plt.ylabel('Percentage')#Win Percentage')    #Ladder Position
plt.title('Win percentage of interstate teams in interstate v vic games since ' + str(year_started))#Win percentage of vic & interstate sides of the last 30 years')


"""
Conclusions from this first graph is:
I write this precedeeing the 2021 season. So as of now, interstate sides have
1. Appeared in 21/31 grand finals.
1.1. Not sure how many they should have appeared in and won, as that must be a funciton of
    percentage of how many interstate teams were in the comp at every stage
2. Won 12/21 of those appearances, for 12/31 premierships. This is despite the
    fact that they represent just under half of all sides (8/18) since 2012, growing
    sporadically from the 3/14 sides that were present in 1990.
3. 18/21 grand finas have been against vic sides.
4. Have won 9/18 of those grand finals. 
5. Interestingly, won 7/9 (includes brisbane 3-peat) from first half of those grand finals and 
    2/9 (includes hawks 3-peat) of all grand finals since.
6. They win 2% less of their games against the vics during the home and away season. 
7. THey win 2% more of their games against the vics during the finals series.
8. Unfortunately, even though there is 30 years being considered, the trends of who is
    better seem to be too long to make any guesses as to how long an 'ascendancy' will last.
    One could hypothesise that the extent of an ascendancy will be matched at its conclusion, as
    happenned when the 2002-2007 interstate ascendancy was followed by the 2008-2013 vic ascendancy.
8.1. The significance of history depends on where you're standing in it. If I'd done this just after
    2006, I would have seen the same home and away and finals win percentages, but 10 premierships to
    an expected 6.72!, interstaters went 10/12 gfs!!!!!!!! We'd all be here trying to figure out what
    it was about grand final day that made interstate sides so much more likely to win it than
    victorians. If I'd analysed starting 1990, win percentage home and away would be about the
    same, win percentage in finals would be up 4% and expected grand finals would be down 1. As it is,
    interstaters need 1 more to square up the ledger. The worst the interstaters have been in
    premierships v expected premierships was 0:1.54 in 1991. In 1996 they were 2:2.97. In 2000 4:4.47.
    2011 10:8.63. 2017 11:11.29. I conclude this shows that interstate sides have been consistently
    winning exactly as many premierships as they would be expected to win, regardless of whether
    they're an interstate side or not. 

    But we could just as easily launch from here into an extended period of interstate or victorian
    dominance. I'll just have to keep faith that it'll all be squared up in the end.

9. Interstate sides do lose more finals and home and away games then they are expected to though.
    ~2.6% more games during the home and away and ~2.2% more games during finals. With the current
    8 interstate teams, playng 22 games each in a home and away season, that adds up to 0.57 a home
    and away game each team each year or 1 game every 2 years that they would lose to a vic side
    that they otherwise would have won if they weren't interstate. Finals is always weird, so I'll
    just leave it at an extra 2.6 losses every 100 vic v interstate finals. There's a lot less data
    on the finals than the home and away games of course, so it's more malleable to change in the
    next few years. But seeing as how it was 45-50 in all the above years I checked (I think) except
    for '91 (17.5%! We'd all be sitting here trying to figure out what it was about finals that made
    interstate sides so much more likely to lose them), I'd think it's fairly strong/correct/reasonable.
"""

'''ay = fig.add_subplot(111)
y5 = 
ay.plot(x, y5)'''

plt.show()