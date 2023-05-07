# Importing the required modules
import os
import sys
import pandas as pd
from bs4 import BeautifulSoup
  
path = 'html.html'
  
# empty list
data = []
  
# for getting the header from
# the HTML file
list_header = []
soup = BeautifulSoup(open("/workspaces/EnergyPrograms/data.html"),'html.parser')
header = soup.find_all("table")[0].find("tr")
 
for items in header:
    try:
        list_header.append(items.get_text())
    except:
        continue
 
# for getting the data
HTML_data = soup.find_all("table")[0].find_all("tr")[1:]

for element in HTML_data:
    sub_data = []
    url = None

    for sub_element in element:
        try:
            sub_data.append(sub_element.get_text())
            url = sub_element.findChild("a")['href']
        except:
            continue
    print(url)
    data.append(sub_data)
 
# Storing the data into Pandas
# DataFrame
dataFrame = pd.DataFrame(data = data, columns = list_header)
  
# Converting Pandas DataFrame
# into CSV file
dataFrame.to_csv('out2.csv')