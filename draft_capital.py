
import statistics
import ast
import os
import matplotlib.pyplot as plt
import numpy as np
import urllib.request
from bs4 import BeautifulSoup

script_directory = str(os.path.dirname(os.path.realpath(__file__)))
file_name = "draftscapitalsavefile.txt"
path_to_file = script_directory + '\\' + file_name
"""
README:

"""


#Constants
this_season = 2020 #? update manuslly
universalURL = 'https://www.draftguru.com.au/clubs/{}'
year_started = 1981#1897#<- interesting #1990
colours = {"GoldCoast":"yellow", "Geelong":"royalblue", "Essendon":"red", "Carlton":"navy", "Collingwood":"black", "Melbourne":"lime", "Hawthorn":"brown", "Fitzroy":"grey", "St Kilda":"crimson", "Richmond":"yellow", "North Melbourne":"blue", "Western Bulldogs":"green", "Fremantle":"purple","Greater Western Sydney":"orange", "Brisbane Lions": "orangered", "Port Adelaide":"cyan", "West Coast":"darkgoldenrod", "Sydney":"deeppink", "Adelaide":"royalblue"} #ugh takes so long to write out

pick2points = {
    1:3000,
    2:2517,
    3:2234,
    4:2034,
    5:1878,
    6:1751,
    7:1644,
    8:1551,
    9:1469,
    10:1395,
    11:1329,
    12:1268,
    13:1212,
    14:1161,
    15:1112,
    16:1067,
    17:1025,
    18:985,
    19:948,
    20:912,
    21:878,
    22:845,
    23:815,
    24:785,
    25:756,
    26:729,
    27:703,
    28:677,
    29:653,
    30:629,
    31:606,
    32:584,
    33:563,
    34:542,
    35:522,
    36:502,
    37:483,
    38:465,
    39:446,
    40:429,
    41:412,
    42:395,
    43:378,
    44:362,
    45:347,
    46:331,
    47:316,
    48:302,
    49:287,
    50:273,
    51:259,
    52:246,
    53:233,
    54:220,
    55:207,
    56:194,
    57:182,
    58:170,
    59:158,
    60:146,
    61:135,
    62:123,
    63:112,
    64:101,
    65:90,
    66:80,
    67:69,
    68:59,
    69:49,
    70:39,
    71:29,
    72:19,
    73:9,
}

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

"""
with open(path_to_file, "r") as f:
    clubs = ast.literal_eval(f.read())
"""

years = list(range(year_started, this_season)) # n

#MAIN:
RETRIEVE_DATA = True
if RETRIEVE_DATA:
    clubs = [
        ["adelaide", [0 for i in years], [0 for i in years]],
        ["brisbane", [0 for i in years], [0 for i in years]],
        ["carlton", [0 for i in years], [0 for i in years]],
        ["collingwood", [0 for i in years], [0 for i in years]],
        ["essendon", [0 for i in years], [0 for i in years]],
        ["fremantle", [0 for i in years], [0 for i in years]],
        ["geelong", [0 for i in years], [0 for i in years]],
        ["gold-coast", [0 for i in years], [0 for i in years]],
        ["greater-western-sydney", [0 for i in years], [0 for i in years]],
        ["hawthorn", [0 for i in years], [0 for i in years]],
        ["melbourne", [0 for i in years], [0 for i in years]],
        ["north-melbourne", [0 for i in years], [0 for i in years]],
        ["port-adelaide", [0 for i in years], [0 for i in years]],
        ["richmond", [0 for i in years], [0 for i in years]],
        ["st-kilda", [0 for i in years], [0 for i in years]],
        ["sydney", [0 for i in years], [0 for i in years]],
        ["west-coast", [0 for i in years], [0 for i in years]],
        ["western-bulldogs", [0 for i in years], [0 for i in years]],
    ]
    for club in clubs:
        try:
            rows = BeautifulSoup(getURL(universalURL.format(club[0])), 'html.parser').find('table').findAll('tr')
        except:
            print(club[0], "Not Found!")
            continue
        print(club)
        current_idx = int(str(rows[0].text).strip()) - year_started
        print(current_idx)
        for row in rows[3:]:
            if row.has_attr("class") and row["class"][0] == "year-header":# and row.text.strip():
                current_idx += 1
                print(club[1])
                print(current_idx)
                print(club[1][current_idx])
                print(club[1][current_idx - 1])
                print(club[2][current_idx])
                club[1][current_idx] = club[1][current_idx - 1] - club[2][current_idx]
            columns = row.findAll('td')
            if len(columns) < 8:
                continue
            pick_text = str(columns[3].text)
            player = str(columns[3]["href"].text).strip() if columns[3].has_attr("href") else "nup"
            print(1, pick_text, player)
            pick = 0
            if pick_text[:20] == "National Draft pick ":
                club[1][current_idx] += pick2points.get(int(pick_text[20:].strip()), 0)
                club[2][this_season - current_idx ]
                rows2 = BeautifulSoup(getURL(player), 'html.parser').find('table').findAll('tr')
                print("yoyo")
            else:
                print('\'' + pick_text[:20] + '\'')
            # if start:
            #     current_idx = 
            # this_is_year_row = False
            # try:
            #     this_is_year_row =  in years
            # except:
            #     continue
            # if this_is_year_row:
            columns = row.findAll('td')

quit()
"""
    for k in range(year_started, this_season):
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
                    clubs[team1] = [[k], [0 for i in years]]
                if team2 in clubs:
                    clubs[team2][0].append(k)
                else:
                    clubs[team2] = [[k], [0 for i in years]]
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
    with open(path_to_file, "w") as f:
        f.write(str(clubs))
    #"""

all_clubs_windows = 0
all_club_window_lengths = [0 for i in years]
all_clubs_prelim_distances = [0 for i in years]
all_clubs_years_twixt_clusters = [0 for i in years]
all_clubs_years_twixt_clusters_1990 = [0 for i in years]
prelims_1990 = 0
club_windows_1990 = 0
club_window_lengths_1990 = [0 for i in years]
club_prelim_distances_1990 = [0 for i in years]
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
    window_lengths = [0 for i in years]
    years_between_prelims = np.diff(np.array(clubs[i][0])).tolist()
    years_between_prelims.append(last_season + 1 - clubs[i][0][-1])
    all_clubs_prelim_distances += years_between_prelims
    years_between_clusters = [0 for i in years]
    years_between_clusters_1990 = [0 for i in years]
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
        len(clubs[i][0]),
        p(len(clubs[i][1])/len(clubs[i][0])),
        total_windows,
        round(statistics.mean(window_lengths), 2),
        round(statistics.mean(years_between_prelims), 2),
        round(statistics.mean(years_between_clusters), 2),
        ' ' #round(statistics.mean(years_between_clusters_1990), 2)
    )))

ax.set_xticks([i for i in range(year_started - int(str(year_started)[-1]), (last_season + (last_season % 10) + 10), 10)])
plt.ylabel('Prelim Finals w/ wins as dots ') 
'''+ 
    p(club_windows_1990/prelims_1990) + 
    " " + 
    str(round(statistics.mean(club_window_lengths_1990), 2)) + 
    " " + 
    str(round(statistics.mean(club_prelim_distances_1990), 2)) + 
    " " + 
    str(round(statistics.mean(all_clubs_years_twixt_clusters_1990), 2))
)'''
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