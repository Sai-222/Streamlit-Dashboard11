from email.policy import default
from enum import unique
from operator import le
from turtle import fillcolor
import matplotlib
from matplotlib import colors
from requests import options
import streamlit as st
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import matplotlib.pyplot as pltst
from matplotlib.pyplot import close, pie, axis, show
import plotly.express as px
import hydralit_components as hc
from streamlit_option_menu import option_menu
import requests
import seaborn as sns
import os
from matplotlib.backends.backend_agg import RendererAgg
import plotly.graph_objects as go
from datetime import datetime

#Import CSV Files---------------------------------------------------------------------

dataset_path = "/Users/woxacorp./Desktop/workspace/dashboard/app/performance_top_trader.csv"
dataset_path = "/Users/woxacorp./Desktop/workspace/dashboard/app/Simple_History.csv"

def load_performance_data(nrows):
    data = pd.read_csv('performance_top_trader.csv', nrows=nrows, skip_blank_lines=True).dropna()
    return data

def load_Simple_data(nrows):
    data = pd.read_csv('Simple_History.csv', nrows=nrows, skip_blank_lines=True).dropna()
    return data    


# Nav-Bar----------------------------------------------------------------------------

menu_data = [
    {'icon': "far fa-chart-bar", 'label':"chart"},
]

over_theme = {'txc_inactive':'white','menu_background':'blue','txc_active':'black','option_active':'white'}
menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    home_name='Home',
    login_name='Logout',
    hide_streamlit_markers=False,
    sticky_nav=True,
    sticky_mode='pinned'
)

st.info(f"{menu_id}")    

#Title of the Page--------------------------------------------------------------------

Page_Title = st.title('Trader Statistics')  

Performance_history = load_performance_data(200)
Simple_Data = load_Simple_data(500)

#Side Bar------------------------------------------------------------------------------
#1-------------------------------------------------
st.sidebar.header("Click here to Filter :")
Months = Simple_Data['Month'].unique()
Month_Selected = st.sidebar.multiselect('Month',Months)
#2---------------------------------------------------
Trades = Simple_Data['categories'].unique()
Trade_Category = st.sidebar.multiselect('Trading Categories', Trades)
#Slider-----------------------------------------------------
Profit_Loss = Simple_Data['P/L'].value_counts()
Profit_Category = st.sidebar.slider('Profit Loss', int(Profit_Loss.min()), int(Profit_Loss.max()),
(int(Profit_Loss.min()), int(Profit_Loss.max())), 1)

#Create Mask for the side bar --------------------------------------------------------------
#mask_Month = Simple_Data['Month'].isin(Month_Selected)
#mask_Category = Simple_Data['categories'].isin(Trade_Category)
#mask_PL = Simple_Data['P/L'].isin(Profit_Category)
#Apply the Mask-------------------------------------------------------------------------------

#Masked_Stuff = Simple_Data[mask_Month & mask_Category]
#st.write(Masked_Stuff)

#Testing stuff Matplotlib------------------------------------------------------------------------

#matplotlib.use("agg")
#_lock = RendererAgg.lock

#Month_Profit = Masked_Stuff['Month'].value_counts()
#df = pd.merge(pd.DataFrame(Month_Profit),Simple_Data,left_index=True, right_on='P/L')

#row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns((0.2, 1, .2, 1, .2))

#with row0_1, _lock:
    #st.header("Profit-Loss per Month")
    #fig, ax = pltst.subplots(figsize=(5,5))
    #ax.pie(Month_Profit, labels=(Month_Profit.index ))

    #p = pltst.gcf()
    #st.pyplot(fig)

#with row0_2:
 #   df = df.reset_index(drop=True)
  #  t = ''
   # for i in range(len(df)):
    #    t=t+df.loc[i,'abreviated_name']+': '+df.loc[i,'name']+'   \n'
     #   for i in range(5):
      #      st.write("")
       #     st.write(t) 


#Trader Performance------------------------------------------------------------------------

st.subheader('Trader Information')
if st.checkbox('Click for Traders History Stats'):
    st.subheader('Trader Performance')
    st.write(Simple_Data)


#Bar Chart Representing the P/L vs. Dates------------------------------------------------------

st.subheader('Trader Performance History')
fig_1 = px.timeline(Simple_Data, x_start='open_time', x_end= 'clsoe_time', y='P/L',
labels={'P/L': 'P/L of Trader per day'}
)

st.plotly_chart(fig_1)

fig = px.violin(Simple_Data, x='P/L', y='Month',
labels={'P/L': 'P/L of Trader per month', 'open_time': 'Dates'}, orientation= 'h',
)
st.plotly_chart(fig)

st.subheader('Profit/Loss when compared to the amount of Leverage taken')
chart_data = pd.DataFrame(Simple_Data[:500], columns=['amount', 'P/L', 'leverage'])
st.bar_chart(chart_data)

#Candle stick chart displaying P/L-------------------------------------------------------------------


#Markdown Menu----------------------------------------------------------------------------

st.subheader('Copied Traders')
st.caption('The trade made by copying traders in terms of Profit/Loss is shown in the following charts')

Copier_List = Simple_Data['parent_username'].unique()
Copiers = st.selectbox('List of copiers', Copier_List, 0)
fig_4 = px.pie(Simple_Data, names='parent_username', values='P/L',
title='Profit - Loss stats acquired from the Copied Traders'
)
st.plotly_chart(fig_4)

#Buy/Sell Score---------------------------------------------------------------------------------
st.subheader('Buy/Sell Stochastics')


fig_3 = px.bar(Simple_Data, x= 'P/L', y= 'is_buy', orientation= 'h',
title= 'Buying and Selling information of the trader' 

)
st.caption('The Buying and Selling information of the Trader are shown below')
st.plotly_chart(fig_3)

with st.expander('More on Stochastics'):
    st.write('**Stochastics** : They are used to measure an issues opening and closing price and its price range over a pre-determined period of time. [Learn more about Stochastics](https://www.investopedia.com/articles/technical/073001.asp).')

#Trade Categories---------------------------------------------------------------------------------

st.subheader('Trader Interests')

st.caption('Investor interests in the trading categories is displayed here in the terms of profit and loss percentage, The pie plot demonstrates the percentage of investment put into certain investment categories.')

fig_2 = px.pie(Simple_Data, names='categories', values='amount',
title='Investor Interests'
)
st.plotly_chart(fig_2)


#Testing-------------------------------------------------------------------------------------------------
st.subheader('Just Testing')
st.caption('A basic Ternary Plot describes the  ratios of three variables in an equilateral Triangle, Since one variable is not independent of the other variable, they are summed to equal a constant and the the sum of the dependent variable define the location of the plot. [Learn more abou the Ternary Plot](https://en.wikipedia.org/wiki/Ternary_plot#:~:text=A%20ternary%20plot%2C%20ternary%20graph,positions%20in%20an%20equilateral%20triangle.).')
fig_5= px.line_ternary(Simple_Data, a='P/L', b='amount', c='leverage')
st.plotly_chart(fig_5)

#FeedBack Page----------------------------------------------------------------------------------------

option_data = [
    {'icon':"bi bi-hand-thumbs-up", 'label':"Agree"},
    {'icon': "fa fa-question-circle", 'label':"Partially Agree"},
    {'icon': "bi bi-hand-thumbs-down", 'label':"Disagree"},
]
over_theme = {'txc_inactive':'white','menu_background':'blue','txc_active':'black','option_active':'white'}
font_fmt = {'font-class':'h3','font-size':'150%'}

op = hc.option_bar(option_definition=option_data,title='Was this page helpful ?',key='PrimaryOption',override_theme=over_theme, font_styling=font_fmt,horizontal_orientation=True)

# More on Investment Categories----------------------------------------------------------------------------

with st.expander('More on Investment Listing'):
    st.write('Major types of Investment Includes [Stock Trading](https://www.investopedia.com/articles/basics/06/invest1000.asp) [Crypto Trading](https://www.investopedia.com/investing-in-cryptocurrency-5215269) [Commodity Trading](https://www.investopedia.com/terms/c/commodity-market.asp) [Currency Trading](https://www.investopedia.com/financial-edge/0412/the-basics-of-currency-trading.aspx#:~:text=All%20currency%20trading%20is%20done,the%20smallest%20increment%20of%20trade.).')



# Additonal Information---------------------------------------------------------------------------    

with st.expander('Click here for Additional Information'):
    st.write("This section is to provide a more personalised perspective of the Traders Information, This section consists of the Country of Origin of the Trader, The average holdong time of an Asset ")
    st.text("Country of Origin")
    st.text_area("Active Since")
    st.text_area("Please report a if there is a bug")    
    st.text_input("enter your mail id")
    st.text_input("Subscribe to our Newsletter")

   

# Disclaimer-----------------------------------------------------------------------------------------
with st.expander('Disclaimer'):
    st.warning('Trading Disclaimer')
    st.text("The content provided by Awonar Inc. does not include financial advice, guidance or recommendations to take, or not to take, any trades, investments or decisions in relation to any matter. \nThe content provided is impersonal and not adapted to any specific client, trader, or business. \nTherefore we recommend that you seek pre-requisite knowledge about investment before making any decisions. \nResults are not guaranteed and may vary from person to person. \nThere are inherent risks involved with trading, including the loss of your investment. \nPast performance in the market is not indicative of future results. \nAny investment is solely at your own risk, you assume full responsibility.")    


#Footer----------------------------------------------------------------------------------------------

footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: right;
}
</style>
<div class="footer">
<p>Developed by Awonar Inc. <a style='display: block; text-align: right;' href="https://staging.awonar.com/markets" target="_blank">Learn More on Awonar Academy</a></p>
</div>

"""
st.markdown(footer,unsafe_allow_html=True)