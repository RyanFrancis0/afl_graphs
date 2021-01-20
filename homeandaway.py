#help("modules") #
import urllib.request
import matplotlib.pyplot as plt
import statistics
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup




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
#quit()
plt.show()