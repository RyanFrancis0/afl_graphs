#help("modules") #
import math
import statistics
import collections
import urllib.request
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup


SHOW_GRAPHS = False

"""
Note to me: the ladder change year by year doesn't make any sense. You naturally believe that all things being
equal, a team's ladder position must in general follow a sine curve and with 100 points of data on half these
teams you'd think you could see that. And while you can trace up and downy stuff, the time periods are wayyyyy
shorter than a sine curve. Teams seem to typically change a lot of places on the ladder year to year. If you
do explore this further, graph the typical magnitude of change in ladder position for all clubs (must it be 0
if it applie to all clubs?), then maybe look at graphing the ladder round by round, that would provide a lot
more data points and team form might fluctuate in a year. Maybe if you finish top of the ladder one year you
slowly fall down it the next. That doesn't sound like what happens.
"""



#constants
universalURL = 'https://afltables.com/afl/seas/ladders/laddersyby.html' 
year_started = 1897
this_season = 2020 #<-this is a manually used value, see last_season below which is autoupdated
teams_in_comp = []
finals_cutoff = []
teams = {}

def getURL(url):
    stream = urllib.request.urlopen(url)
    text = stream.read().decode('utf-8')
    stream.close()
    return text

#MAIN:
text = getURL(universalURL)
soup = BeautifulSoup(text, 'html.parser')
tables = soup.findAll('table')
last_season = this_season# int(tables[0].find('tr').find('a').text) - 1
tables.reverse()

for i in tables[1:]:
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
del teams["University"] #<- remove this?

colours = {"Fitzroy":"Grey", "Gold Coast":"orangered", "Geelong":"royalblue", "Essendon":"red", "Carlton":"navy", "Collingwood":"black", "Melbourne":"lime", "Hawthorn":"brown", "Fitzroy":"grey", "St Kilda":"crimson", "Richmond":"yellow", "North Melbourne":"blue", "Western Bulldogs":"green", "Fremantle":"purple","Greater Western Sydney":"orange", "Brisbane Lions": "orangered", "Port Adelaide":"cyan", "West Coast":"darkgoldenrod", "Sydney":"deeppink", "Adelaide":"royalblue"} #ugh takes so long to write out
running_colours = []
for i in teams:
    running_colours.append(colours[i])

means = []
modes = []
medians = []
expected_premierships = []

count = 1
for i in teams:
    year_began = teams[i][0][0]
    start_diff = year_began - year_started
    x = teams[i][0]
    y = teams[i][1]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_prop_cycle(color=running_colours)
    ax.step([i for i in range(year_began, year_began + len(teams_in_comp[start_diff:]))], teams_in_comp[start_diff:], 'k--', label="Teams In Comp", where="post")
    ax.plot(x, y, label="Position")#, where='mid'
    y3 = [sum([1 / j for j in teams_in_comp[start_diff:start_diff + i]]) for i in range(len(x))]
    expected_premierships.append((y3[-1], i))
    print("Expected Premierships", y3, y3[-1], [teams_in_comp[start_diff:i] for i in range(len(x))])
    ax.plot(x, y3, label="Expected Premierships")
    years_in_top_4_since_1995 = []
    streak = []
    streaks = []
    year_grah = 1995 if x[0] <= 1995 else x[0]
    print(i)
    #print(year_grah, range(x.index(year_grah), x.index(year_grah) + last_season + 1 - year_grah))

    ax.scatter(x, y)
    ax.invert_yaxis()
    if i == "Fitzroy":
       continue
    for k in range(x.index(year_grah), x.index(year_grah) + last_season + 1 - year_grah):
        if y[k] < 5:
            print("in top 4", x[k], y[k])
            years_in_top_4_since_1995.append((x[k], y[k]))
            streak.append(y[k])
        elif len(streak) > 0:
            print("aw dropped it", x[k])
            x2 = range(x[k] - len(streak), x[k])
            ax.plot(x2, streak, ':')
            streaks.append(x2)
            streak = []


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
    n_club_streaks = len(streaks)
    print(n_club_streaks)
    if n_club_streaks > 0:
        avg_len_club_streaks = statistics.mean([len(i) for i in streaks])
        print(avg_len_club_streaks)
        if n_club_streaks > 1:
            if streaks[0][0] != year_grah:
                streaks = [[year_grah]] + streaks
            if streaks[-1][-1] != last_season:
                streaks.append([last_season])
            print(streaks)
            len_years_tween_streaks = statistics.mean([streaks[i + 1][0] - streaks[i][-1] for i in range(len(streaks) - 1)])
            print(len_years_tween_streaks)
    
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
    avg = 3#4
    moving_average = [round(i, 2) for i in pd.DataFrame(y).rolling(avg).mean()[0].tolist()[avg - 1:]]
    #print(moving_average)
    moving_average_diff = np.diff(np.array(moving_average)).tolist()
    start = math.floor((avg - 1) / 2)
    stop = len(x) - start
    reduced = x[start:stop]
    ax.plot(reduced[:stop - (len(reduced) - len(moving_average)) - 1], moving_average, color='brown', label="Rolling " + str(avg) + " year ladder position avg")#
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

print("Premiership differentials: (where a club is relative to their normally distributed expected premiership schedule)")
URL = 'https://en.wikipedia.org/wiki/List_of_VFL/AFL_premiers'
text = getURL(URL)
soup = BeautifulSoup(text, 'html.parser')
rows = soup.find('table', attrs={'style':'text-align:center;'}).findAll('tr')
rows = sorted(rows[2:20], key = lambda row: int(row.find('td').text[:4]))
expected_premierships = sorted(expected_premierships)
differentials = []
for row in rows:
    club = row.find('th').text.strip()
    gfs = row.findAll('td')
    premierships = len([int(i.text) for i in gfs[2].findAll('a')])
    a = [i for i in expected_premierships if i[1] == club]
    if club == "South Melbourne/Sydney[c]":
        a = [i for i in expected_premierships if i[1] == "Sydney"]
    elif club == "North Melbourne/Kangaroos[d]":
        a = [i for i in expected_premierships if i[1] == "North Melbourne"]
    elif club == "Footscray/Western Bulldogs[e]":
        a = [i for i in expected_premierships if i[1] == "Western Bulldogs"]
    differentials.append((premierships - a[0][0], club))
a = [i for i in expected_premierships if i[1] == "Gold Coast"]
differentials.append((-1 * a[0][0], "Gold Coast"))
adder = 1
for j, i in enumerate(sorted(differentials)):
    addendum = ""
    if i[0] > 0 and i[1] != "Richmond":
        addendum = "== Will be okay with them winning another premiership in " + str(1 + math.ceil(18 * i[0])) + " seasons time."
    elif i[0] < 0:
        addendum = "== Would take " + str(1 - math.floor(-18 * i[0])) + " seasons to root against them again if Richmond ain't in it"
    rounded = round(i[0], 2)
    pre = ""
    if i[1] == "Fitzroy":
        adder -= 1
    else:
        pre = str(j + adder) + '.'
    print(pre, i[1] + ':', rounded if rounded < 0 else '+' + str(rounded), addendum)
print("2020: The fastest Saints could get into the green on expected premierships was if they 11-peated starting with 2021 flag. How many generations for them to catch the norm? My descendants (if I have any) will have long forgotten me.")


too_late = last_season + 1
change_in_ladder_positions = []
change_in_ladder_positions_diff = []
year_im_doing_this = 2000#9

print("Big rises and falls into and out of the top 4:")
for k in range(year_im_doing_this, too_late):
    #print(k)
    top8 = [0] * 8
    top8_diff = [0] * 8
    previous_year = k - 1
    for i in teams:
        #print(i, teams[i][0], teams[i][1])
        if teams[i][0][-1] <= previous_year or teams[i][0][0] > previous_year:
            #print(k, i)
            continue
        this_years_index = k - last_season
        # if len(teams[i][0]) != len(teams[i][1]):
        #     print("booyah biatch")
        this_years_position = teams[i][1][teams[i][0].index(k)]
        last_years_index = this_years_index - 1
        last_years_position = teams[i][1][teams[i][0].index(k - 1)]
        if this_years_position > 8:
            if last_years_position < 5:
                suffix = "th"
                if last_years_position == 1:
                    suffix = "st"
                elif last_years_position == 2:
                    suffix = "nd"
                elif last_years_position == 3:
                    suffix = "rd"
                print(teams[i][0][teams[i][0].index(k)], i + '.', "\x1B[3mFinished " + str(teams[i][1][teams[i][0].index(k)]) + "th" + "\x1B[23m.", "Fell", this_years_position - last_years_position, "ladder positions from", str(last_years_position) + suffix, "last year")
            continue
        top8[this_years_position - 1] = last_years_position
        top8_diff[this_years_position - 1] = -1 * (this_years_position - last_years_position)
        if this_years_position < 5 and last_years_position > 8:
            suffix = "th"
            if this_years_position == 1:
                suffix = "st"
            elif this_years_position == 2:
                suffix = "nd"
            elif this_years_position == 3:
                suffix = "rd"
            print(teams[i][0][teams[i][0].index(k - 1)], i + '.', "\x1B[3mFinished " + str(teams[i][1][teams[i][0].index(k - 1)]) + "th" + "\x1B[23m.", "Rose", top8_diff[this_years_position - 1], "ladder positions next year to", str(this_years_position) + suffix)
        #print(i, last_years_position, this_years_position, teams[i][1])
    change_in_ladder_positions.append(top8)
    change_in_ladder_positions_diff.append(top8_diff)
    #print(top8)

not_in_4 = []
not_in8 = []
people_from_outside_8 = []
total_top8_change = []
print("Ladder pos previous year")
for i in change_in_ladder_positions:
    n_not_in_4 = 0
    n_not_in_8 = 0
    total_changes_to_the_8 = 0
    for k in i[:4]:
        if k > 8:
            n_not_in_8 += 1
            total_changes_to_the_8 += 1
            people_from_outside_8.append(k)
        elif k > 4:
            n_not_in_4 += 1
    for k in i[4:]:
        if k > 8:
            total_changes_to_the_8 += 1
    not_in_4.append(n_not_in_4)
    not_in8.append(n_not_in_8)
    total_top8_change.append(total_changes_to_the_8)
    print(change_in_ladder_positions.index(i) + year_im_doing_this, i)
print(collections.Counter(sum(change_in_ladder_positions, [])))
print("Subsequent change in ladder pos")
for i in change_in_ladder_positions_diff:
    print(i)
print("Year_2_year_changes, top4, top8")
for i in range(len(not_in_4)):
    print(i + year_im_doing_this, "->", i + year_im_doing_this + 1, not_in_4[i], "team(s) from 5th-8th moved into top 4,", not_in8[i], "team(s) from outside the top 8 got into the top 4")
print("Average of last list")
print(statistics.mean(not_in_4), statistics.mean(not_in8))
print("Outside-8->in ladder pos mean, median, mode, max, min, shebang")
print(statistics.mean(people_from_outside_8), statistics.median(people_from_outside_8), statistics.mode(people_from_outside_8), min(people_from_outside_8), max(people_from_outside_8), people_from_outside_8, collections.Counter(people_from_outside_8))
print("Total changes to the 8")
print(statistics.mean(total_top8_change), total_top8_change, collections.Counter(total_top8_change))
print("1995-2020 there has NEVER been less than two changes to the top 8.")

if SHOW_GRAPHS:
    plt.show()