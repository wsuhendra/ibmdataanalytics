#Display the output
print("New Python File")

!pip install yfinance
!pip install bs4
!pip install nbformat

#importing libraries
import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)

#graphic function
def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
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
  
#Question 1: Use yfinance to Extract Stock Data
tesla=yf.Ticker('TSLA')
tesla_data=tesla.history(period='max')
tesla_data.reset_index(inplace=True)
tesla_data.head()

#Q2:Use Webscraping to Extract Tesla Revenue Data
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
html_data  = requests.get(url).text
#parsing
soup = BeautifulSoup(html_data, 'html.parser')
#dataframe
tesla_revenue = pd.DataFrame(columns=['Date', 'Revenue'])
for row in soup.find("tbody").find_all('tr'):
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text
    # appending
    tesla_revenue = pd.concat([tesla_revenue,pd.DataFrame({'Date':[date], 'Revenue':[revenue]})], ignore_index=True)

tesla_revenue['Revenue'] = tesla_revenue['Revenue'].str.replace('$',"")
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]
tesla_revenue.tail()

#Question 3: Use yfinance to Extract Stock Data
gme=yf.Ticker("GME")
gme_data=gme.history(period="max")
gme_data.reset_index(inplace=True)
gme_data.head()

#Q4:Use Webscraping to Extract Tesla Revenue Data
url_2 = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
html_data_2  = requests.get(url_2).text
#parsing
soup = BeautifulSoup(html_data_2, 'html.parser')
#dataframe
gme_revenue = pd.DataFrame(columns=["Date", "Revenue"])
for row in soup.find("tbody").find_all('tr'):
    col = row.find_all("td")
    year = col[0].text
    revenue = col[1].text
    # appending
    gme_revenue = pd.concat([gme_revenue,pd.DataFrame({"Date":[year], "Revenue":[revenue]})], ignore_index=True)
gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace('$',"")
gme_revenue.dropna(inplace=True)
gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]
gme_revenue.tail()

#Q5: Plot Tesla Stock Graph
make_graph(tesla_data,tesla_revenue,'Tesla')
