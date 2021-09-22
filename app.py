#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Use Gravitational Quick Review from streamlit gallary


# In[ ]:


import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests, os
import io
from datetime import datetime
import matplotlib.dates as mdates


# In[ ]:


dicMonth = {1: 'January', 2: 'February', 3: 'March', 4: 'April',
           5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September',
           10: 'October', 11: 'November', 12: 'December'}
dicNumMonth = {v: k for k, v in dicMonth.items()}


# In[4]:


@st.cache
def quoteDaily(strTicker):
    apiKey = '5X7KUIKJE5AQZW2B'
#     strTicker = 'AAPL'
    path = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=' + strTicker + '&outputsize=full&apikey=' + apiKey + '&datatype=csv'
    try:
        r = requests.get(path)
        #
        dfTicker = pd.read_csv(io.StringIO(r.content.decode('utf-8')))
        dfTicker['timestamp'] = pd.to_datetime(dfTicker['timestamp'])
        dfTicker['year'] = pd.DatetimeIndex(dfTicker['timestamp']).year
        dfTicker['month'] = pd.DatetimeIndex(dfTicker['timestamp']).month
        #
    except:
        return pd.DataFrame()
    return dfTicker
#
@st.cache
def searchTicker(strTicker):
    apiKey = '5X7KUIKJE5AQZW2B'
#     strTicker = 'AAPL'
    path = 'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=' + strTicker + '&apikey=' + apiKey + '&datatype=csv'
    try:
        r = requests.get(path)
        #
        dfTicker = pd.read_csv(io.StringIO(r.content.decode('utf-8')))
#         dfTicker['timestamp'] = pd.to_datetime(dfTicker['timestamp'])
#         dfTicker['year'] = pd.DatetimeIndex(dfTicker['timestamp']).year
#         dfTicker['month'] = pd.DatetimeIndex(dfTicker['timestamp']).month
        #
    except:
        return pd.DataFrame()
    return dfTicker


# In[ ]:


# -- Set page config
apptitle = 'stock-streamlit-test'

st.set_page_config(page_title=apptitle, page_icon=":eyeglasses:")

# Title the app
st.title('Stocks View Test')

st.sidebar.markdown("## Select Ticker and Time")

strTickerPre = ''
strTicker = st.sidebar.text_input('Ticker/Name/Search')
strTicker = strTicker.lower()
if strTickerPre == '':
    dfTicker = pd.DataFrame()

if strTicker != strTickerPre:
    if len(strTicker) > 0:
        print('download from alpha vantage')
        dfTicker = quoteDaily(strTicker)
        print('done')
        if len(dfTicker) == 0:
            #Search info
            st.header('Search result for ' + strTicker)
            dfSearch = searchTicker(strTicker)
            st.dataframe(dfSearch)
#         print('no ticker')
    strTickerPre = strTicker
    

lstYear = []
if len(dfTicker) > 0:
    lstYear = dfTicker['year'].unique().tolist()
if len(lstYear) > 0:
    lstYearSelect = ['All'] + lstYear
else:
    lstYearSelect = lstYear
lstCheckYear = st.sidebar.multiselect('Select Year', lstYearSelect)

lstMonth = []
if len(dfTicker) > 0:
    lstMonth = sorted(dfTicker['month'].unique().tolist())
    lstMonth = [dicMonth[i] for i in lstMonth]
if len(lstMonth) > 0:
    lstMonthSelect = ['All'] + lstMonth
else:
    lstMonthSelect = lstMonth
lstCheckMonth = st.sidebar.multiselect('Select Month', lstMonthSelect)

if 'All' in lstCheckYear:
    lstCheckYear = lstYear
#     print(lstCheckYear)
if 'All' in lstCheckMonth:
    lstCheckMonth = lstMonth
#     print(lstCheckMonth)

if len(lstCheckMonth) > 0:
    lstCheckMonth = [dicNumMonth[i] for i in lstCheckMonth]

valZoom = st.sidebar.slider('Zoom', 1, 5)  # min, max, default

if (len(lstCheckYear) > 0) and len(lstCheckMonth) > 0:
    if len(dfTicker) > 0:
        dfPlot = dfTicker[(dfTicker['year'].isin(lstCheckYear)) & (dfTicker['month'].isin(lstCheckMonth))].copy()
        lenZoom = int((len(dfPlot)-1)/valZoom)
        if len(dfPlot) > 0:
            dfPlot['timestamp'] = pd.to_datetime(dfPlot['timestamp'])
            dfPlot = dfPlot.sort_values(by=['timestamp'])
            valView = st.sidebar.slider('View', min_value=1, max_value=len(dfPlot), step=lenZoom, value=1)
            st.header('Ticker: ' + strTicker.upper())
            plt.close()
            fig, ax = plt.subplots()
            ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
            ax.grid(True)
            if valView + lenZoom < len(dfPlot):
                endSlice = valView + lenZoom
            else:
                endSlice = len(dfPlot) - 1
                valView = endSlice - lenZoom
            if valView > 0:
                valView -= 1
            print('valView:', valView, 'endSlice:', endSlice, lenZoom)
            ax.set_ylabel('Close Price ($)')
            ax.set_xlabel('Date')
            ax.plot(dfPlot['timestamp'].iloc[valView:endSlice], dfPlot['close'].iloc[valView:endSlice])
            fig.autofmt_xdate()
            st.pyplot(fig)






