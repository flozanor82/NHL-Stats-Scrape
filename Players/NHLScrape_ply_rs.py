# Run the command as administrator - conda update ipython
# cd "D:\Box Sync\Python Learning\NHL Scrape"
# d:
import os
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from __future__ import division
import pandas as pd
import requests
import time
import re
import itertools as it
import csv
#####################################
sess = webdriver.Chrome()
sess.get('http://www.nhl.com/stats/player?reportType=season&seasonFrom=19171918&seasonTo=20172018&gameType=2&filter=gamesPlayed,gte,1&sort=points,goals,assists') #Regular Season
time.sleep(4)

items=sess.find_element_by_css_selector('span.-totalInfo')
item=items.text
item= item.replace(' records returned','')		#Total number of records in the search
print(item)

ac = ActionChains(sess)
ac.send_keys(Keys.PAGE_DOWN)
ac.send_keys(Keys.PAGE_DOWN)
ac.send_keys(Keys.PAGE_DOWN)
ac.send_keys(Keys.PAGE_DOWN)
ac.perform()

itera=sess.find_element_by_css_selector('span.-totalPages')
itr=itera.text
print(itr)



limit=pd.to_numeric(itr)
#limit=5
main_ls=[]
j=0
while(j<limit):
#while(j<itr):
	rows0=sess.find_elements_by_css_selector('div.rt-tr-group')
	rows_ls=[]
	for row in rows0:
		rows_ls.append(row.text)
	print(rows_ls)
 	#len(rows_ls)
 
	rows_ls = [w.replace('\n','||') for w in rows_ls]

	df = pd.DataFrame(rows_ls)
	df = pd.DataFrame([sub.split("||") for sub in rows_ls])
	#print(df.ix[0])

	if len(df.columns)==22:
		df[22]="--"
		df.columns=["N","Player","Season","Team","Pos","GP","G","A","P","M_L","PIM","P_GP","PPG","PPP","SHG","SHP","GWG","OTG","S","S_Shr","Shifts_GP","FOW_Shr","TOI_GP"]
		df=df[["N","Player","Season","Team","Pos","GP","G","A","P","M_L","PIM","P_GP","PPG","PPP","SHG","SHP","GWG","OTG","S","S_Shr","TOI_GP","Shifts_GP","FOW_Shr"]]
	else:
		df.columns=["N","Player","Season","Team","Pos","GP","G","A","P","M_L","PIM","P_GP","PPG","PPP","SHG","SHP","GWG","OTG","S","S_Shr","TOI_GP","Shifts_GP","FOW_Shr"]

	print(df)	
	main_ls.append(df)
	j=j+1
	
	element = WebDriverWait(sess,15).until(
		EC.element_to_be_clickable((By.CSS_SELECTOR,'div.-next'))
		)
	sess.find_element_by_css_selector('div.-next').click()

len(main_ls)
df2=main_ls[0]
for l in range(1,limit):
	df2=df2.append(main_ls[l])
	print(l)

print(df2)

df2.to_csv('players_regular.csv', index=False)
sess.close()



#//*[@id="stats-page-body"]/div[2]/div[1]/div[3]
#//*[@id="stats-page-body"]/div[2]/div[1]/div[3]/div[1]

# Start with BS to see if it is an easy scrape - this one isnt
#players_regul =requests.get('http://www.nhl.com/stats/player?reportType=season&seasonFrom=19171918&seasonTo=20172018&gameType=2&filter=gamesPlayed,gte,1&sort=points,goals,assists')
#players_regul.status_code #200 is success we got the html#
#soup = bs(players_regul.text, 'html.parser')
#print(soup.prettify()) #prints the html but nicely-parsed- with BS
#soup.find_all(class_="rt-tbody")
#soup.find_all(class_="rt-tr-group")
#stats-page-body > div.ReactTable.-striped.-highlight > div.rt-table > div.rt-tbody > div:nth-child(1) > div > div:nth-child(2)