import pandas as pd
import streamlit as st
import pydeck as pdk
from PIL import Image


st.title("Where to Go When You've 'Got to Go' in the City of Edinburgh")

# using columns to work on the placement of the image in the centre of the page
col1, col2, col3 = st.columns(3)
with col1:
    st.write(' ')

with col2:
    image = Image.open('scottish_washroom_sign.png')
    st.image(image, width=400)

with col3:
    st.write('')

# use st.write() to easily enter text and hyperlinks
st.write("Use this app to identify the nearest washroom. Keep in mind, however, this data was last updated in 2015...so you may be out of luck!")
st.write("This demo is meant to show how easy it is to develop an interactive geospatial web application with only a few lines of code. Explore the code base to find out how.")

# Commented lines of code will not be read or visible
# data source: https://github.com/edinburghcouncil/datasets/blob/master/Public%20toilets.csv
# data source last updated in 2015

# Reading in the dataset and some pre-processing to drop unused columns
df = pd.read_csv("edinburgh_public_toilets.csv")
# splitting location into lat, long
data = df['Location'].str.strip('()').str.split(',').str[:2]
# adding geometry
geom = pd.DataFrame(data.tolist(), columns=['lat', 'lon'], index=df.index) \
         .apply(pd.to_numeric, errors='coerce')
df = df.join(geom)
# if data entry is empty (NA), replace with 'No additional services'
df.fillna('No additional services', inplace=True)
# drop all unnessary other columns
df.drop(["Refurbished in 2013", "Refurbishment status", "Email", "Telephone", "Location"], axis=1, inplace=True)

# table with the full dataset
st.write("Scroll through the table below for the full list and use the filters on the left-hand panel to filter based on your needs.")
st.write(df)

# use Streamlit's side bar options to allow for filtering of dataset by pulldown options
st.sidebar.markdown('### Data Filters')
charge = list(df['Charge'].drop_duplicates())
# multiselect allows you to select more than one filter option at a time
charge_choice = st.sidebar.multiselect('Select if there is a cost:', charge)
facilities = list(df["Facilities"].drop_duplicates())
facilities_choice = st.sidebar.multiselect('Select by available facilities:', facilities)

df = df[df['Charge'].isin(charge_choice)]
df = df[df['Facilities'].isin(facilities_choice)]

# create spacing in the layout
st.write('')
# adding more descriptive text
st.write("After filtering, find your results below. Use the interactive map below to zoom in further and hover over the point(s) on the map to find out more information.")
st.write('')
# produce a table of the filtered dataframe 
st.table(df) 

# defining tool tips to allow for pop up labels on map 
# these labels are linked to columns in the original dataframe
tooltip={
    'html': 'Charge: {Charge}</br> Facilities: {Facilities} </br> Opening hours: {Opening_times}</br> Name: {Toilet}',
    "style": {
        "backgroundColor": "steelblue",
        "color": "white"
   }
}

# Use Streamlit's pydeck_chart to define the layers shown in the map (see docs: https://docs.streamlit.io/library/api-reference/charts/st.pydeck_chart)
r =   st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        tooltip = tooltip,
        initial_view_state=pdk.ViewState(
            latitude=55.950558,
            longitude=-3.185556,
            zoom=10,
            pitch=25
        ),
        layers=[
            pdk.Layer(
                'ColumnLayer',
                data=df,
                get_position='[lon, lat]',
                auto_highlight=True,
                pickable=True,
                opacity=0.4,
                stroked=True,
                filled=True,
                radius=200,
                elevation_scale=0,
                elevation_range=[0, 10],
                extruded=True,
            )
        ]
    ))

