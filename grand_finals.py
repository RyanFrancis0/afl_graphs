import urllib.request
from bs4 import BeautifulSoup
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
ax.set_prop_cycle(color=['red', 'navy', 'black', 'lime', 'royalblue', 'grey', 'deeppink', 'crimson','yellow', 'brown', 'blue', 'green', 'gold', 'royalblue', 'purple','orangered', 'cyan', 'orange', 'darkgoldenrod', 'red', 'orange']) #cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)]
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
    ax.step(x, y, where='post', label=club)
    rtyughk = [seasons[total.index(i)] for i in premierships]
    ax.scatter(premierships, rtyughk)

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
