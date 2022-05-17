import pandas as pd
import streamlit as st
import pydeck as pdk

st.title("Where to Go When You've 'Got to Go' in the City of Edinburgh")

st.write("Use this app to identify the nearest washroom. Keep in mind, however, this data was last updated in 2015...so you may be out of luck!")
st.write("[Data source](https://github.com/edinburghcouncil/datasets/blob/master/Public%20toilets.csv)")

# data source: https://github.com/edinburghcouncil/datasets/blob/master/Public%20toilets.csv
# last updated in 2015

df = pd.read_csv("edinburgh_public_toilets.csv")
data = df['Location'].str.strip('()').str.split(',').str[:2]
geom = pd.DataFrame(data.tolist(), columns=['lat', 'lon'], index=df.index) \
         .apply(pd.to_numeric, errors='coerce')
df = df.join(geom)
df.fillna('No additional services', inplace=True)
df.drop(["Refurbished in 2013", "Refurbishment status", "Email", "Telephone", "Location"], axis=1, inplace=True)

# table with the full dataset
st.write("Scroll through the full table below for the full list and use the filters on the left-hand panel to filter based on your needs")
st.write(df)

# allowing for filtering of dataset by pulldown options
st.sidebar.markdown('### Data Filters')
charge = list(df['Charge'].drop_duplicates())
charge_choice = st.sidebar.multiselect('Select if there is a cost:', charge)
facilities = list(df["Facilities"].drop_duplicates())
facilities_choice = st.sidebar.multiselect('Select by available facilities:', facilities)

df = df[df['Charge'].isin(charge_choice)]
df = df[df['Facilities'].isin(facilities_choice)]

st.write("After filtering, find your results below. Hover over the point on the map to find out more information.")
st.write(df)


tooltip={
    'html': 'Charge: {Charge}</br> Facilities: {Facilities} </br> Opening hours: {Opening_times}</br> Name: {Toilet}',
    "style": {
        "backgroundColor": "steelblue",
        "color": "white"
   }
}

r =   st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        tooltip = tooltip,
        initial_view_state=pdk.ViewState(
            latitude=55.950558,
            longitude=-3.185556,
            zoom=8,
            pitch=50
        ),
        layers=[
            pdk.Layer(
                'ColumnLayer',
                data=df,
                get_position='[lon, lat]',
                auto_highlight=True,
                pickable=True,
                opacity=0.6,
                stroked=True,
                filled=True,
                get_radius = 10,
                get_fill_color=[255, 140, 0]
            )
        ]
    ))

