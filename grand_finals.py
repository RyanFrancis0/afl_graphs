import urllib.request
from bs4 import BeautifulSoup
from operator import itemgetter
import matplotlib.pyplot as plt

#constants
universalURL = 'https://en.wikipedia.org/wiki/List_of_VFL/AFL_premiers'
last_season = 2019 #auto updated, dont need to edit. only thing u need to edit on this page is colour order, and also if gc get a gf or new club after this year

def getURL(url):
    stream = urllib.request.urlopen(url)
    text = stream.read().decode('utf-8')
    stream.close()
    return text
    
#MAIN:           
text = getURL(universalURL)
soup = BeautifulSoup(text, 'html.parser')
rows = soup.find('table', attrs={'style':'text-align:center;'}).findAll('tr')


##NUM_COLORS = 20

#plt.subplot(10, 2, 1)
fig = plt.figure()
ax = fig.add_subplot(111)
#cm = plt.get_cmap('tab20')
prop_cycle = ['red', 'navy', 'black', 'lime', 'royalblue', 'grey', 'deeppink', 'crimson','yellow', 'brown', 'blue', 'green', 'gold', 'royalblue', 'purple','orangered', 'cyan', 'orange', 'darkgoldenrod', 'red', 'orange']
ax.set_prop_cycle(color=prop_cycle) #cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)]
colours = {"geelong":"royalblue", "essendon":"red", "carlton":"navy"} #ugh takes so long to write out

rows = sorted(rows[2:20], key = lambda row: int(row.find('td').text[:4]))

#
for row in rows:
    club = row.find('th').text.strip()
    gfs = row.findAll('td')
    year_started = int(gfs[0].text[:4])
    premierships = [int(i.text) for i in gfs[2].findAll('a')]
    runner_ups = [int(i.text) for i in gfs[4].findAll('a')]
    total = premierships + runner_ups
    if max(total) > last_season:
        last_season = max(total)

def countlist(random_list):
    retlist = []
    # Avoid IndexError for  random_list[i+1]
    count = 1
    for i in range(len(random_list) - 1):
        # Check if the next number is consecutive
        if random_list[i] + 1 == random_list[i+1]:
            count += 1
        else:
            # If it is not append the count and restart counting
            retlist.append(count)
            count = 1
    # Since we stopped the loop one early append the last count
    retlist.append(count)
    return retlist

dynasties = []
for row in rows:
    club = row.find('th').text.strip()
    gfs = row.findAll('td')
    year_started = int(gfs[0].text[:4])
    premierships = [int(i.text) for i in gfs[2].findAll('a')]
    runner_ups = [int(i.text) for i in gfs[4].findAll('a')]
    total = premierships + runner_ups
    total.sort()
    if len(total) > 0:
        years_b4_gf = (total[0] - year_started) * [0]
        year_finished = total[len(total) - 1]
        years_since_gf = (last_season + 1 - year_finished) * [len(total)]
    else:
        years_b4_gf = (last_season - year_started) * [0]
        years_since_gf = []
        year_finished = last_season
    x = (len(years_b4_gf) * [year_started]) + total + list(range(year_finished, last_season + 1))
    seasons = list(range(1, len(total) + 1)) #couldsnt think of better name
    y = years_b4_gf + seasons + years_since_gf
    ax.set_prop_cycle(color=prop_cycle[rows.index(row):])
    ax.step(x, y, where='post', label=club)
    rtyughk = [seasons[total.index(i)] for i in premierships]
    #I'm strictly defining a dynasty as a stretch of >= 3 grand finals and >= 1 premierships with < 2 years between any of the grand finals in question
    dynasty = []
    for i in range(len(total)):
        if club == "Adelaide":
            print(dynasty)
        if i != len(total) - 1 and total[i] + 2 >= total[i + 1]:
            dynasty.append(total[i])
        else:
            #if the next grand final is greater that two years from this grand final
            if len(dynasty) >= 1 or (i == len(total) - 1 and len(dynasty) >= 1):
                dynasty.append(total[i])
                #If 3+ premierships or 4+ grand finals
                ps = [j for j in dynasty if j in premierships]
                n_p = len(ps)
                n_g = len(dynasty)
                if n_p >= 2:
                    #len_p = -1 * (dynasty[-1] - dynasty[0] + 1) #HUGE apologies for this complete hack
                    #if n_p > 1: 
                    len_p = ps[-1] - ps[0] + 1
                    consec_g = max(countlist(dynasty))
                    len_g = dynasty[-1] - dynasty[0] + 1
                    dynasties.append((club, dynasty, ps, n_p, len_p, n_g, consec_g, len_g))
                    ax.set_prop_cycle(color=prop_cycle[rows.index(row):])
                    ax.plot([dynasty[0], dynasty[-1]], [seasons[total.index(dynasty[0])], seasons[total.index(dynasty[-1])]], ':')
            dynasty = []
    ax.set_prop_cycle(color=prop_cycle[rows.index(row):])
    ax.scatter(premierships, rtyughk)

#print(dynasties)
my_rankings = sorted(dynasties, key = itemgetter(7), reverse = True)
my_rankings = sorted(my_rankings, key = itemgetter(6), reverse = True)
my_rankings = sorted(my_rankings, key = itemgetter(5), reverse = True)
my_rankings = sorted(my_rankings, key = itemgetter(4))
my_rankings = sorted(my_rankings, key = itemgetter(3), reverse = True)
#print("")
#print(my_rankings)

rankings = [(i[3], i[4], i[5], i[6], i[7]) for i in my_rankings]
current_ranking = 1
print("Ranking dynasities by my metrics")
for i in my_rankings:
    #print(i)
    position = my_rankings.index(i)
    final_position = str(current_ranking)
    if (i != my_rankings[0] and rankings[position - 1] == rankings[position]) or (i != my_rankings[-1] and rankings[position + 1] == rankings[position]):
        final_position = '=' + final_position
        if (i != my_rankings[-1] and rankings[position + 1] != rankings[position]):
            current_ranking += 1
    else:
        current_ranking += 1
    print("{}. {} {} - {} won {} premierships in {} years from {} grand finals (including {} consecutive) over {} years".format(final_position, i[0], i[1][0], i[1][-1], i[3], i[4], i[5], i[6], i[7]))

#print(plt.get_data_interval())
ax.set_xticks([i for i in range(1890, (last_season + (last_season % 10) + 10), 10)])
plt.ylabel('Grand Finals w/ premierships')    
plt.xlabel('Years')
plt.title('Grand finals by club')
plt.legend()
plt.minorticks_on()
plt.grid(which='minor')
plt.grid(which='major', color="black")
#plt.legend(loc='upper left', ncol=1, mode="expand")


#test
seasonsURL = 'https://afltables.com/afl/seas/ladders/laddersyby.html'
text = getURL(seasonsURL)
soup = BeautifulSoup(text, 'html.parser')
tables = soup.findAll('table')
for i in range(5):
    rows = tables[i].find('tbody').findAll('tr')
    
#plt.subplot(10, 2, 2)



plt.show()
