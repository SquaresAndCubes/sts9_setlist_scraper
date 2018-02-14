####HTML SETLIST SCRAPER########
# BY: Brent Vaalburg#
# Version 0.1#
from pymongo import MongoClient
from bs4 import BeautifulSoup
import urllib.request

#####CONNECT TO SETLISTS COLLECTION ON sts9_db###

mongo_client = MongoClient('labops-bldr-lnx', 27017)

sts9db = mongo_client.sts9_db.setlists

#################################################

##HTML SCRAPE FUNCTON##

def scrape_setlist(html):
    ###Date Venue################

    # search input html for show date and venue store as string

    date_venue_city_state = html.find('h2', {'itemprop': 'name'}).string.strip()

    # parse date venue city and state from scraped string

    date_venue_city = date_venue_city_state[:-2].replace(',', '')

    date_venue_city_ps = date_venue_city.split('::')

    date = date_venue_city_ps[0].strip()

    venue = date_venue_city_ps[1].strip()

    city = date_venue_city_ps[2].strip()

    date_ps = date.split('.')

    yyyy = date_ps[0]

    mm = date_ps[1]

    dd = date_ps[2]

    state = date_venue_city_state[-2:]

    print(date_venue_city_state+'\n')

    print(yyyy+'\n'+mm+'\n'+dd+'\n'+venue+'\n'+city+'\n'+state+'\n')

    #END Venue and Date Parsing###################################################

    ##Begin Parsing Setlist Data####

    pre_songs = []

    pre_setlist = []

    for td in html.find_all('td', {'class': 'play'}):
        pre_songs.append(td.next_sibling.next_sibling.text.replace('(1)','').replace('(2)','').strip())

    for song in pre_songs:
        pre_setlist.extend([x.strip() for x in song.split('>')])


    setlist = list(dict.fromkeys(pre_setlist))

    print(pre_songs)

    print(setlist)

    print('\n')

    print('--------------------------------------------------')



    show = {'year': yyyy,
            'month': mm,
            'day': dd,
            'venue': venue,
            'city': city,
            'state': state,
            'setlist': setlist}

    sts9db.insert_one(show)



# main loop for cycling through multiple html files
##SET LIST URL##

in_url = open('urls2.txt')

for line in in_url:

    req = urllib.request.Request(str(line))

    try:
        resp = urllib.request.urlopen(req)

    except urllib.request.HTTPError as e:
        if e.code == 404:
            print('*******************\n*********404*******\n*******************\n' + line)
            print('\n')

    else:

        body = resp.read()
        soup = BeautifulSoup(body, 'html.parser')
        scrape_setlist(soup)

in_url.close()
mongo_client.close()
