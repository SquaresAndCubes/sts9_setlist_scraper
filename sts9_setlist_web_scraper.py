####HTML SETLIST SCRAPER########
# BY: Brent Vaalburg#
# Version 0.1#
from pymongo import MongoClient
from bs4 import BeautifulSoup
import re
import urllib.request
import os

#####CONNECT TO SETLISTS COLLECTION ON sts9_db###

#sts9 = MongoClient('10.0.0.16', 27017).sts9_db.setlists

#################################################

##HTML SCRAPE FUNCTON##

def scrape_setlist(html):
    ###Date Venue################

    # search input html for show date and venue store as string

    date_venue = html.find('h2', {'itemprop': 'name'}).string

    print(date_venue)

    # unformatted string is split
    date_venue_split = date_venue.split(" :: ")

    # splits are stored to separate vars

    yyyy_mm_dd = date_venue_split[0].split(".")
    venue = date_venue_split[1].strip()
    city_state = re.split(', | ', date_venue_split[2])

    city = city_state[0].strip()
    state = city_state[1].strip()

    yyyy = yyyy_mm_dd[0].strip()
    mm = yyyy_mm_dd[1].strip()
    dd = yyyy_mm_dd[2].strip()

    print(yyyy)
    print(mm)
    print(dd)
    print(venue)
    print(city)
    print(state)
    print('\n')

    # search input html for setlist data



    ##create show document for submission to mongo sts9 db

    # show = {"year": str.rstrip(yyyy),
    #         "month": str.rstrip(mm),
    #         "day": str.rstrip(dd),
    #         "venue": str.rstrip(venue),
    #         "city": str.rstrip(city),
    #         "state": str.rstrip(state)}
    #
    # # insert show document to sts9_db, setlists collection
    #
    # sts9.insert_one(show)


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
        scrape_setlist(soup)

in_url.close()