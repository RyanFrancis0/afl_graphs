import urllib.request
import matplotlib.pyplot as plt
import numpy as np
import statistics
import ast
from bs4 import BeautifulSoup

"""
README:
If last_season (see constants below) isn't the last season in the AFL in which prelims were played OR you haven't
    run this file on this computer before (Because of the 120+ webpages that need to be accessed, the amount of
    processing that needs to be done on that accessed data and the fact that 99.99% of the times you run this file
    the data doesn't need updating I save the data to a txt file in the folder this program is in rather than
    gather it anew):
1. change it to the correct season 
2. uncomment the RETRIEVE DATA section below
3. run the program
4. close the graph that opens up
5. recomment that section
6. save this file

I could've made that above process automatic but couldn't be bothered/didn't want to bother afltables.com every time
    someone runs this
"""


#Constants
last_season = 2019
universalURL = 'https://afltables.com/afl/seas/{}.html'
year_started = 1897
colours = {"GoldCoast":"yellow", "Geelong":"royalblue", "Essendon":"red", "Carlton":"navy", "Collingwood":"black", "Melbourne":"lime", "Hawthorn":"brown", "Fitzroy":"grey", "St Kilda":"crimson", "Richmond":"yellow", "North Melbourne":"blue", "Western Bulldogs":"green", "Fremantle":"purple","Greater Western Sydney":"orange", "Brisbane Lions": "orangered", "Port Adelaide":"cyan", "West Coast":"darkgoldenrod", "Sydney":"deeppink", "Adelaide":"royalblue"} #ugh takes so long to write out

def getURL(url):
    stream = urllib.request.urlopen(url)
    text = stream.read().decode('utf-8')
    stream.close()
    return text

"""
Convert float to 2 decimal place percentage string with percent sign on the end

Input (float): f
returns (str): f * 100, rouded to 2 decimal, with percent symbol on end
"""
def p(f):
    return str(round(100 * f, 2)) + '%'

with open("prelimsavefile.txt", "r") as f:
    clubs = ast.literal_eval(f.read())

#MAIN:
""" RETRIEVE DATA
clubs = {} # {"club":[[years total], [years won]]}
for k in range(year_started, last_season + 1):
    text = getURL(universalURL.format(k))
    soup = BeautifulSoup(text, 'html.parser')
    tables = soup.findAll('table')
    if tables[-2].text != "Grand Final":
        #1987 & 1924
        continue
    flag = False
    for i in tables:
        if flag == True:
            flag = False
            data = i.findAll('tr')
            team1 = data[0].find('a').text
            team2 = data[1].find('a').text
            if team1 == "Kangaroos":
                team1 = "North Melbourne"
            elif team1 == "Brisbane Bears":
                team1 = "Brisbane Lions"
            elif team1 == "Footscray":
                team1 = "Western Bulldogs"
            elif team1 == "South Melbourne":
                team1 = "Sydney"
            if team2 == "Kangaroos":
                team2 = "North Melbourne"
            elif team2 == "Brisbane Bears":
                team2 = "Brisbane Lions"
            elif team2 == "Footscray":
                team2 = "Western Bulldogs"
            elif team2 == "South Melbourne":
                team2 = "Sydney"
            if team1 in clubs:
                clubs[team1][0].append(k)
            else:
                clubs[team1] = [[k], []]
            if team2 in clubs:
                clubs[team2][0].append(k)
            else:
                clubs[team2] = [[k], []]
        if i.text == "Preliminary Final":
            flag = True
    gfdata = tables[len(tables) - 1].findAll('tr')
    team1 = gfdata[0].find('a').text
    team2 = gfdata[1].find('a').text
    if team1 == "Kangaroos":
        team1 = "North Melbourne"
    elif team1 == "Brisbane Bears":
        team1 = "Brisbane Lions"
    elif team1 == "Footscray":
        team1 = "Western Bulldogs"
    elif team1 == "South Melbourne":
        team1 = "Sydney"
    if team2 == "Kangaroos":
        team2 = "North Melbourne"
    elif team2 == "Brisbane Bears":
        team2 = "Brisbane Lions"
    elif team2 == "Footscray":
        team2 = "Western Bulldogs"
    elif team2 == "South Melbourne":
        team2 = "Sydney"
    if team1 in clubs:
        clubs[team1][1].append(k)
        if k not in clubs[team1][0]:
            clubs[team1][0].append(k)
    else:
        clubs[team1] = [[k], [k]]
    if team2 in clubs:
        clubs[team2][1].append(k)
        if k not in clubs[team2][0]:
            clubs[team2][0].append(k)
    else:
        clubs[team2] = [[k], [k]]
with open("prelimsavefile.txt", "w") as f:
    f.write(str(clubs))
"""

all_clubs_windows = 0
all_club_window_lengths = []
all_clubs_prelim_distances = []
all_clubs_years_twixt_clusters = []
all_clubs_years_twixt_clusters_1990 = []
prelims_1990 = 0
club_windows_1990 = 0
club_window_lengths_1990 = []
club_prelim_distances_1990 = []
fig = plt.figure()
ax = fig.add_subplot(111, alpha=0.7)

for i in clubs:
    ax.set_prop_cycle(color=colours[i])
    year_finished = clubs[i][0][-1]
    years_b4_pre = (clubs[i][0][0] - year_started) * [0]
    years_since_pre = (last_season + 1 - year_finished) * [len(clubs[i][0])]
    seasons = list(range(1, len(clubs[i][0]) + 1))
    x = (len(years_b4_pre) * [clubs[i][0][0]]) + clubs[i][0] + [last_season + 1]
    y = years_b4_pre + seasons + [len(clubs[i][0])]
    wins_y = [seasons[clubs[i][0].index(k)] for k in clubs[i][1]]
    ax.scatter(clubs[i][1], wins_y)
    last = clubs[i][0][0]
    record = [last]
    total_windows = 0
    window_lengths = []
    years_between_prelims = np.diff(np.array(clubs[i][0])).tolist()
    years_between_prelims.append(last_season + 1 - clubs[i][0][-1])
    all_clubs_prelim_distances += years_between_prelims
    years_between_clusters = []
    years_between_clusters_1990 = []
    flag = True
    for k in clubs[i][0][1:]:
        if k > 1990 and flag and clubs[i][0][0] < 1990:
            years_between_clusters_1990.append(k - 1990)
            flag = False
        if k >= 1990:
            prelims_1990 += 1
            if last >= 1990:
                club_prelim_distances_1990.append(k - last)
        if k - last < 3: # 
            record.append(k)  
            last = k
            if k != clubs[i][0][-1]:
                continue
        if k != record[-1]:
            years_between_clusters.append(k - record[-1])
            if record[-1] >= 1990:
                years_between_clusters_1990.append(k - record[-1])
        if len(record) > 1:
            total_windows += 1
            all_clubs_windows += len(record)
            if (record[0] >= 1990):
                club_windows_1990 += len(record)
                club_window_lengths_1990.append(record[-1] + 1 - record[0])
            window_lengths.append(record[-1] + 1 - record[0])
            x2 = [record[0], record[-1]]
            y2 = [y[x.index(record[0])], y[x.index(record[-1])]]
            ax.set_prop_cycle(color=colours[i])
            ax.plot(x2, y2, ':')
        record = [k]
        last = k
    all_club_window_lengths += window_lengths
    diff_last_Season_and_last_prelim = last_season + 1 - clubs[i][0][-1]
    years_between_clusters.append(diff_last_Season_and_last_prelim)
    years_between_clusters_1990.append(diff_last_Season_and_last_prelim)
    club_prelim_distances_1990.append(diff_last_Season_and_last_prelim)
    all_clubs_years_twixt_clusters += years_between_clusters
    all_clubs_years_twixt_clusters_1990 += years_between_clusters_1990
    ax.step(x, y, alpha=0.7, where='post', label=("{} {} {} {} {} {} {} {}".format(
        i,
        str(len(clubs[i][0])),
        p(len(clubs[i][1])/len(clubs[i][0])),
        total_windows,
        round(statistics.mean(window_lengths), 2),
        round(statistics.mean(years_between_prelims), 2),
        round(statistics.mean(years_between_clusters), 2),
        round(statistics.mean(years_between_clusters_1990), 2)
    )))

ax.set_xticks([i for i in range(1890, (last_season + (last_season % 10) + 10), 10)])
plt.ylabel('Prelim Finals w/ wins as dots ' + 
    p(club_windows_1990/prelims_1990) + 
    " " + 
    str(round(statistics.mean(club_window_lengths_1990), 2)) + 
    " " + 
    str(round(statistics.mean(club_prelim_distances_1990), 2)) + 
    " " + 
    str(round(statistics.mean(all_clubs_years_twixt_clusters_1990), 2))
)    
plt.xlabel('Years')
plt.title("Prelim finals by club " + 
    p(all_clubs_windows/sum(len(clubs[i][0]) for i in clubs)) + 
    " " + 
    str(round(statistics.mean(all_club_window_lengths), 2)) + 
    " " + 
    str(round(statistics.mean(all_clubs_prelim_distances), 2)) + 
    " " + 
    str(round(statistics.mean(all_clubs_years_twixt_clusters), 2))
)
plt.legend()
plt.minorticks_on()
plt.grid(which='minor')
plt.grid(which='major', color="black")

plt.show()