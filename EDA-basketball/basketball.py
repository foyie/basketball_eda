import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

#putting title in st
st.title('NBA player stats')

#for writing texts 
st.markdown(""" 
            We are doing webscraping
            * **Libraries:** streamlit,pandas,numpy etc
            * **Data scource:** [NBA reference site](https://www.basketball-reference.com/) 
            """) 

st.sidebar.header('User input features')
selecter_year=st.sidebar.selectbox('Year?',list(reversed(range(1950,2020))))

#webscraping 

@st.cache #saves the data after loading one time 

def load_data(year):
    
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html" #??
    html=pd.read_html(url,header=0)
    df=html[0]
    raw=df.drop(df[df.Age=='Age'].index)
    raw=df.fillna(0)
    playerstats=raw.drop(['Rk'],axis=1)
    return playerstats  #shows the unmodded data
playerstats=load_data(selecter_year)

# Sidebar - Team selection
sorted_unique_team = sorted(playerstats.Tm.unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team) 
#first value=name,second=options to chose from,third=default view

# Sidebar - Position selection
unique_pos = ['C','PF','SF','PG','SG']
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

df_selected_team=playerstats[(playerstats.Tm.isin(selected_team))&(playerstats.Pos.isin(selected_pos))]

st.header('Player stats for selected team')
st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
st.dataframe(df_selected_team)

#heatmap 

if st.button('Heatmap'):
    st.header('Intercorrelation Matrix Heatmap')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    df_selected_team.to_csv('output.csv',index=False)
    df = pd.read_csv('output.csv')
    
    corr=df.corr()
    mask=np.zeros_like(corr)
    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
    st.pyplot()
    