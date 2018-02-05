####HTML SETLIST SCRAPER########
#BY: Brent Vaalburg#
#Version 0.1#
from pymongo import MongoClient
from bs4 import BeautifulSoup
import os


##SET LIST DATA SOURCE PATH##

data_dir = 'HTML/'

#####CONNECT TO SETLISTS COLLECTION ON sts9_db###

sts9 = MongoClient('10.0.0.16', 27017).sts9_db.setlists

#################################################

##HTML SCRAPE FUNCTON##

def scrape_setlist(html):

    ###Date Venue################

    # search input html for show date and venue store as string

    date_venue = str(html.find('div',{'class':'release_attr_title'}).string)


    #unformatted string is split
    date_venue_split = date_venue.split(":: ")

    #splits are stored to separate vars

    yyyy_mm_dd = date_venue_split[0].split(".")
    venue = date_venue_split[1]
    city_state = date_venue_split[2].split(", ")

    city = city_state[0]
    state = city_state[1]

    yyyy = yyyy_mm_dd[0]
    mm = yyyy_mm_dd[1]
    dd = yyyy_mm_dd[2]

    #search input html for setlist data

    setlist = str()

    ##create show document for submission to mongo sts9 db

    show = {"year": str.rstrip(yyyy),
            "month": str.rstrip(mm),
            "day": str.rstrip(dd),
            "venue": str.rstrip(venue),
            "city": str.rstrip(city),
            "state": str.rstrip(state)}

    #insert show document to sts9_db, setlists collection

    sts9.insert_one(show)


#main loop for cycling through multiple html files



##############MAIN LOOP##################################
for file in os.listdir(data_dir):
    if file.endswith('.html'):
        fname = os.path.join(data_dir,file)
        with open(fname) as f:
            soup = BeautifulSoup(f.read(),'html.parser')
            scrape_setlist(soup)
##########################################################