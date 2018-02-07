####HTML SETLIST SCRAPER########
# BY: Brent Vaalburg#
# Version 0.1#
from pymongo import MongoClient
from bs4 import BeautifulSoup
import re
import urllib.request
import os

#####CONNECT TO SETLISTS COLLECTION ON sts9_db###

sts9 = MongoClient('10.0.0.16', 27017).sts9_db.setlists

#################################################

##HTML SCRAPE FUNCTON##

def scrape_setlist(html):
    ###Date Venue################

    # search input html for show date and venue store as string

    date_venue_city_state = html.find('h2', {'itemprop': 'name'}).string.strip()

    #parse date venue city and state from scraped string

    date_venue_city = date_venue_city_state[:-2].replace(',','')

    date_venue_city_ps = date_venue_city.split('::')

    date = date_venue_city_ps[0].strip()

    venue = date_venue_city_ps[1].strip()

    city = date_venue_city_ps[2].strip()

    date_ps = date.split('.')

    yyyy = date_ps[0]

    mm = date_ps[1]

    dd = date_ps[2]

    state = date_venue_city_state[-2:]

    #print(date_venue_city_state)

    #print(yyyy+'\n'+mm+'\n'+dd+'\n'+venue+'\n'+city+'\n'+state+'\n')

    return yyyy, mm, dd, venue, city, state






    # search input html for setlist data



    ##create show document for submission to mongo sts9 db

def save_show(in_year, in_month, in_day, in_venue, in_city, in_state):

    show = {"year": str.rstrip(in_year),
            "month": str.rstrip(in_month),
            "day": str.rstrip(in_day),
            "venue": str.rstrip(in_venue),
            "city": str.rstrip(in_city),
            "state": str.rstrip(in_state)}

    # insert show document to sts9_db, setlists collection

    sts9.insert_one(show)


# main loop for cycling through multiple html files
##SET LIST URL##

in_url = open('urls.txt')

for line in in_url:

    req = urllib.request.Request(str(line))


    try:
        resp = urllib.request.urlopen(req)

    except urllib.request.HTTPError as e:
        if e.code == 404:
            print('*******************\n*********404*******\n*******************\n'+line)
            print('\n')

    else:

        body = resp.read()
        soup = BeautifulSoup(body, 'html.parser')

        save_show(scrape_setlist(soup))

in_url.close()
sts9.close()