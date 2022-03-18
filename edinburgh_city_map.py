import pandas as pd
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
st.write(df)

charge = df['Charge'].drop_duplicates()
charge_choice = st.sidebar.selectbox('Select if there is a cost:', charge)
facilities = df["Facilities"]
facilities_choice = st.sidebar.selectbox('Select by available facilities:', facilities)
hours = df["Opening times"]
hours_choice = st.sidebar.selectbox('Select by opening times:', hours)






st.map(df)