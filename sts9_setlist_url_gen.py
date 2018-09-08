from bs4 import BeautifulSoup
import re

in_html = ['HTML/URL/Music _ STS9 _ Live _ By Year _ 2017.html',]

txt_file = open('urls.txt', 'a')

for file in in_html:
    with open(file) as f:
        soup = BeautifulSoup(f.read().decode('utf8'), 'lxml')
        for show in soup.find_all('a', attrs={'class':'product-item__link'}):
            show_string = show.get('href').encode('utf-8')
            #show_string2 = show.text

            txt_file.write(show_string+'\n')
            #txt_file.write(show_string2.encode('utf-8'))

txt_file.close()




