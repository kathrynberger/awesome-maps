import pandas as pd
import pydeck as pdk
import numpy as np
import streamlit as st

st.title("Where to Go When You've Got to Go in the City of Edinburgh")

st.write("Use this app to identify the nearest washroom. Keep in mind, however, this data was last updated in 2015...so you may be out of luck!")
st.write("Data source: https://github.com/edinburghcouncil/datasets/blob/master/Public%20toilets.csv")

# data source: https://github.com/edinburghcouncil/datasets/blob/master/Public%20toilets.csv
# last updated in 2015

df = pd.read_csv("edinburgh_public_toilets.csv")
data = df['Location'].str.strip('()').str.split(',').str[:2]
geom = pd.DataFrame(data.tolist(), columns=['lat', 'lon'], index=df.index) \
         .apply(pd.to_numeric, errors='coerce')
df = df.join(geom)
df.fillna('', inplace=True)
df.drop(["Refurbished in 2013", "Refurbishment status", "Email", "Telephone", "Location"], axis=1, inplace=True)

# table with the full dataset
st.write("Scroll through the full table below")
st.write(df)

# allowing for filtering of dataset by pulldown options
st.sidebar.markdown('### Data Filters')
charge = list(df['Charge'].drop_duplicates())
charge_choice = st.sidebar.multiselect('Select if there is a cost:', charge)
facilities = list(df["Facilities"].drop_duplicates())
facilities_choice = st.sidebar.multiselect('Select by available facilities:', facilities)
# hours = list(df["Opening times"].drop_duplicates())
# hours_choice = st.sidebar.multiselect('Select by opening times:', hours)

df = df[df['Charge'].isin(charge_choice)]
df = df[df['Facilities'].isin(facilities_choice)]
# df = df[df['Opening times'].isin(hours_choice)]
st.write("Use the filtering options on the panel to the left and find the results below")
st.write(df)
st.map(df)