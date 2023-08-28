# import selenium library for web scrapping
# Data Scrapping
import selenium
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
s=Service('C:\Program Files (x86)/chromedriver.exe')
d= webdriver.Chrome(service=s)
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import re 
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common import exceptions
import pandas as pd

Articles=[]

for i in range(1,221): #Loop through each of the webpage
    webpage='https://www.airlinequality.com/airline-reviews/qatar-airways/page/' + str(i) + '/' 
    d.get(webpage)
    WebDriverWait(d, 5)
    try:
        #For each web page extract all the articles present(i.e individual reviews on the page)
        bodies=d.find_elements(By.XPATH, "*//article[@itemprop='review']")
        #loop through the individual review
        for body in bodies:
            Article=[]
            header=body.find_element(By.XPATH, ".//h2[@class='text_header']").text  #extract review title
            Article.append(header)
            date_published= body.find_element(By.XPATH, ".//time[@itemprop='datePublished']").text #extract review date
            Article.append(date_published)
            country= body.find_element(By.XPATH, ".//h3[@class='text_sub_header userStatusWrapper']").text #extract country of reviewer
            country = re.findall(r'\(.*?\)', country)[0]
            Article.append(country)
            name= body.find_element(By.XPATH, ".//span[@itemprop='author']").text # extract name of reviewer
            Article.append(name)
            overall_rating=body.find_element(By.XPATH, ".//div[@itemprop='reviewRating']").text  #extract overall rating from reviewer
            Article.append(overall_rating)
            text= body.find_element(By.XPATH, ".//div[@class='text_content ']").get_attribute('textContent') #extract review text
            Article.append(text)
            #extracting individual review stars
            reviews=body.find_elements(By.XPATH, ".//td[@class='review-value ']")
            stars=body.find_elements(By.XPATH, ".//td[@class='review-rating-stars stars']")
            rheaders= body.find_elements(By.XPATH, ".//td[contains(@class, 'review-rating-header')]")
            rec=body.find_element(By.XPATH, ".//td[contains(@class, 'review-value rating')]")
            rates=[]
            headers=[]
            header_lists=['Type Of Traveller', 'Seat Type', 'Route', 'Date Flown', 'Seat Comfort', 'Cabin Staff Service', 'Food & Beverages',
            'Inflight Entertainment', 'Ground Service', 'Wifi & Connectivity', 'Value For Money', 'Recommended']
            for review in reviews:
                rates.append(review.text)
            for star in stars:
                total_star=star.find_elements(By.XPATH, ".//span[@class='star fill']")
                total_star=len(total_star)
                rates.append(total_star)
                
            for header in rheaders:
                headers.append(header.text)
            rates.append(rec.text)
            dico={}
            for a, b in zip(rates, headers):
                dico[b]=a
            # for i in header_lists:
            #     if i not in dico:
            #         dico[i]='Nan'
            # rec=dico['Recommended']
            # del dico['Recommended']
            # dico['Recommended']=rec
            # for value in dico.values():
            Article.append(dico)
            Articles.append(Article)
    except:
        pass
#saving extracted reviews to a dataframe and download
df1=pd.DataFrame(Articles)
df1.to_csv('air.csv', sep = ',', index = False)



# Data Cleaning
import ast
lsst=[]
df=pd.read_csv('air.csv')
for row in df['6'].values:
  test=ast.literal_eval(row)
  lsst.append(test)

df1= df.iloc[:, 0:6]
df1.columns= ['Title', 'Date_Published', 'Country', 'Name', 'Overall_rating', 'Review Text']
df2=pd.DataFrame.from_records(lsst)
df=pd.concat([df1, df2], axis=1)
df.to_csv('airquality.csv', sep=',', index=False)



# #renaming the columns
# import pandas as pd
# df=pd.read_csv('air.csv')
# df.columns=['Title', 'Date_Published', 'Country', 'Name', 'Overall_rating', 'Review Text','Type Of Traveller', 'Seat Type', 'Route', 'Date Flown', 'Seat Comfort', 'Cabin Staff Service',\
#             'Food & Beverages', 'Inflight Entertainment', 'Ground Service', 'Wifi & Connectivity', 'Value For Money', 'Recommended', 'Recommended_' ]
# df.to_csv('airlinequalityreviews.csv', sep = ',', index = False)
        

    
    
        
        
    
    
    
    
    

