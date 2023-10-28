#!/usr/bin/env python
# coding: utf-8

# # yfinance shares data extraction

# In[29]:


#!pip install yfinance==0.2.4 --user
#!pip install pandas==1.3.3


# In[30]:


import yfinance as yf
import pandas as pd


# In[31]:


#creating an object apple with tinker function to access data through apple comapny's symbol AAPL
apple = yf.Ticker("AAPL")
#what is this link about?
get_ipython().system('wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/data/apple.json')


# In[34]:


#import json
#with open('apple.json') as json_file:
   # apple_info = json.load(json_file)
    # Print the type of data variable    
    #print("Type:", type(apple_info))
#apple_info


# In[35]:


apple_share_price_data = apple.history(period="max")
apple_share_price_data.reset_index(inplace=True)
apple_share_price_data.plot(x="Date", y="Open")


# In[36]:


apple.dividends.plot()


# In[ ]:





# # web scraping

# In[26]:


#!pip install pandas==1.3.3
#!pip install requests==2.26.0
#!mamba install bs4
#!mamba install html5lib
#!pip install lxml
#!pip install plotly==5.3.1
import requests
import pandas as pd
from bs4 import BeautifulSoup


# In[27]:


url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/netflix_data_webpage.html"


# In[28]:


data  = requests.get(url).text
print(data)
#we print data to understand the html data with tags,we are working on


# In[29]:



#we are creating a beautifulsoup object that keeps the data from the url above and we are parsing it with html5lib
soup = BeautifulSoup(data, 'html5lib')
#we are creating a datframe object(initially an empty pandas table) of name netflix_data
netflix_data = pd.DataFrame(columns=["Date", "Open", "High", "Low", "Close", "Volume"])


# In[30]:


# First we isolate the body of the table which contains all the information
# Then we loop through each row and find all the column values for each row
for row in soup.find("tbody").find_all('tr'):
    col = row.find_all("td")
    date = col[0].text
    Open = col[1].text
    high = col[2].text
    low = col[3].text
    close = col[4].text
    adj_close = col[5].text
    volume = col[6].text
    
    # Finally we append the data of each row to the table
    netflix_data = netflix_data.append({"Date":date, "Open":Open, "High":high, "Low":low, "Close":close, "Adj Close":adj_close, "Volume":volume}, ignore_index=True)    


# In[31]:


netflix_data.head()


# # multi web scraping

# In[111]:


#!pip install plotly


# In[112]:


import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# In[113]:


def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()


# In[114]:


import yfinance as yf
tesla= yf.Ticker("TSLA")
tesla_data=tesla.history(period="max")


# In[115]:


tesla_data.reset_index(inplace=True)
tesla_data.head()


# In[116]:


url="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
html_data=requests.get(url).text


# In[117]:


soup=BeautifulSoup(html_data,'html.parser')


# In[118]:


tables = soup.find_all('table')
for index,table in enumerate(tables):
    if ("Tesla Quarterly Revenue" in str(table)):
        table_index = index
Tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])
for row in tables[table_index].tbody.find_all("tr"):
    col = row.find_all("td")
    if (col != []):
        Date = col[0].text
        Revenue = col[1].text
        Tesla_revenue = Tesla_revenue.append({"Date":Date, "Revenue":Revenue}, ignore_index=True)


# In[119]:


Tesla_revenue["Revenue"] = str(Tesla_revenue['Revenue']).replace('$',"").replace(",","")


# In[120]:


Tesla_revenue.dropna(inplace=True)

Tesla_revenue = Tesla_revenue[Tesla_revenue['Revenue'] != ""]

Tesla_revenue.tail()


# In[121]:


gme= yf.Ticker("GME")
gme_data= gme.history(period="max")


# In[122]:


gme_data.reset_index(inplace=True)
gme_data.head()


# In[123]:


url="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
html_data=requests.get(url).text


# In[124]:


soup=BeautifulSoup(html_data,'html.parser')


# In[125]:


tables = soup.find_all('table')
for index,table in enumerate(tables):
    if ("GameStop Quarterly Revenue" in str(table)):
        table_index = index
gme_revenue = pd.DataFrame(columns=["Date", "Revenue"])
for row in tables[table_index].tbody.find_all("tr"):
    col = row.find_all("td")
    if (col != []):
        Date = col[0].text
        Revenue = col[1].text.replace("$", "").replace(",", "")
        gme_revenue = gme_revenue.append({"Date":Date, "Revenue":Revenue}, ignore_index=True)


# In[126]:


gme_revenue.tail()


# In[129]:


make_graph(gme_data, gme_revenue, 'GameStop')


# In[ ]:




