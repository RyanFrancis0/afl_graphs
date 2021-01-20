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
year_started = 2000 #1897
this_season = 2020 #<-this is a manually used value, see last_season below which is autoupdated
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

class Match(object):
    def __init__(self, home_team, away_team, home_team_score, away_team_score, venue):
        self._home_team = home_team
        self._away_team = away_team
        self._home_team_score = home_team_score
        self._away_team_score = away_team_score
        self._margin = home_team_score - away_team_score
        self._venue = venue

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
        self._win_percentage = 0.0
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
    "Hawthorn": Hawthorn,
    "Adelaide": Adelaide,
    "Port Adelaide": PA,
    "Sydney": Sydney,
    "Greater Western Sydney": GWS,
    "Western Bulldogs": WB,
    "Geelong": Geelong
    }

melbournian_averages = []
interstate_and_geelong_averages = []

for year in range(year_started, this_season):
    text = getURL(universalURL.format(year))
    soup = BeautifulSoup(text, 'html.parser')
    tables = soup.findAll('table')
    last_season = this_season# int(tables[0].find('tr').find('a').text) - 1
    tables.reverse()
    #create seasons for every club
    for i in clubs.keys():
        clubs[i]._seasons[year] = Season(year)
    x = 0
    #do finals first
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
    #a = 
    #print(a)
    rows = BeautifulSoup(getURL(universalURL.format(year))).findChildren('table')[-x - 4].findChildren('tr')[2:-2]
    for i in rows:
        collumns = i.findAll('td')
        club = collumns[1].text
        season = clubs[club]._seasons[year]
        season._games_in_season = int(collumns[2].text) + len(season._finals_matches)
        season._teams_in_season = len(rows)
        season.n_home_and_away_wins = int(collumns[3].text)
        season._n_total_wins = season.n_home_and_away_wins
        finals_wins = 0
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
        season._win_percentage = int(collumns[3].text) / int(collumns[5].text)
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
        clubs[team1]._seasons[year]._total_matches.append(match)
        clubs[team1]._seasons[year]._home_and_away_matches.append(match)
        clubs[team2]._seasons[year]._total_matches.append(match)
        clubs[team2]._seasons[year]._home_and_away_matches.append(match)
    for i in clubs.keys():
        clubs[i]._seasons[year]._total_matches.reverse()
        clubs[i]._seasons[year]._finals_matches.reverse()
        clubs[i]._seasons[year]._home_and_away_matches.reverse()
    melboune_win_percentages = []
    interstate_win_percentages = []
    for i in clubs.keys():
        season = clubs[i]._seasons[year]
        if len(season._total_matches) > 0:
            #print(str(year)# + " " + str(len(season._total_matches)))
            if clubs[i]._interstate:
                interstate_win_percentages.append(clubs[i]._seasons[year]._win_percentage)
            else:
                melboune_win_percentages.append(clubs[i]._seasons[year]._win_percentage)
    melbournian_averages.append(statistics.mean(melboune_win_percentages))
    interstate_and_geelong_averages.append(statistics.mean(interstate_win_percentages))
print(melbournian_averages)
print(interstate_and_geelong_averages)
print(statistics.mean(melbournian_averages))
print(statistics.mean(interstate_and_geelong_averages))
#del teams["University"] #<- remove this?

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

x = range(year_started, last_season + 1) #teams[i][0]
y = melbournian_averages #teams[i][1]
y2 = interstate_and_geelong_averages
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_prop_cycle(color=running_colours)
#ax.step([i for i in range(year_began, year_began + len(teams_in_comp[start_diff:]))], teams_in_comp[start_diff:], 'k--', label="Teams In Comp", where="post")
ax.plot(x, y, label="Position")#, where='mid'
ax.plot(x, y2, label="Position")#, where='mid'
#ax.scatter(x, y)
ax.invert_yaxis()
ax.set_xticks([i for i in range(year_began, (last_season + (last_season % 10)), 10)])# - year_began % 10
ax.set_yticks([i for i in range(0, 1, 0.1)])
plt.ylabel('Win Percentage, interstate avg = ' + str() + ' melbourn avg = ' + str())    #Ladder Position
plt.xlabel('Years')
plt.legend()
plt.title('')
ax.minorticks_on()
ax.grid(which='minor')
ax.grid(which='major', color="black")
#quit()
plt.show()