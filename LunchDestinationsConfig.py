import streamlit as st
from datetime import datetime
import os
import pandas as pd
import numpy as np
import pydeck as pdk
#import folium
from datetime import datetime
import pytz
#from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go

# st.image('https://raw.githubusercontent.com/djpCoding/LunchDestinations/main/Inspire11.png')
st.title("Minneapolis Restaurant Roulette")
st.markdown("Unsure of where to eat lunch or grab a quick snack? Use this restaurant roulette to find a new (or not so new) location for an option close to the office!")



# Define the current central US time for comaprison on luck params 
def currenttimestamp():
    date_format = '%Y-%m-%d %H:%M:%S'
    now = datetime.now(pytz.timezone('US/Central'))
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    current_time = datetime.strptime(current_time, date_format)
    return current_time
current_time = currenttimestamp()

# Load the data that was stored in the file and cache it. Only needed to load up once. 
#@st.cache_data()
def load_info():
    rest = pd.read_csv("Restaurants.csv")
    rest['OpenDT'] = pd.to_datetime(rest['Open'])
    rest['CloseDT'] = pd.to_datetime(rest['Close'])
    rest[["lat","lon"]] = rest["Coordinates"].str.split(", ", expand = True)
    return rest
rest = load_info()   

# Load up the map for later use
# Coordinates for downtown Minneapolis
minneapolis_coords = pd.DataFrame({"lat": [44.979087279569036],"lon": [-93.2717422460245]})
inspire11_cords = pd.DataFrame({"lat": [44.979087279569036], "lon": [-93.2717422460245]})


def random_coffee():
    filtered_coffee = rest[(current_time > rest['OpenDT']) & (current_time < rest['CloseDT'])]
    filtered_coffee = filtered_coffee.loc[filtered_coffee["Categtory"]=="Coffee"]
    if len(filtered_coffee.index) > 0:
        random_coffee_row = filtered_coffee.sample(n=1, replace=False)  
    else: 
        st.write("It looks like there are no open coffee shops right now. Sorry!")
        random_coffee_row = []
    return random_coffee_row


def random_lunch():
    filtered_lunch = rest
    filtered_lunch = filtered_lunch.loc[filtered_lunch["Categtory"]=="Fast casual"]
    if len(filtered_lunch) > 0:
        random_lunch_row = filtered_lunch.sample(n=1, replace=False) 
    else:
        st.write("Looks like we don't have any lunch options right now.")
        random_lunch_row = [] 
    return random_lunch_row

def map_render(lat, lon, name):
        data = {'lat': lat, 'lon': lon, 'size': 500, "label": name}
        df = pd.DataFrame(data)
        df.loc[len(df.index)] = [44.979087279569036, -93.2717422460245, 500, "Inspire11"]
        fig = px.scatter_mapbox(
            df,
            lat='lat',
            lon='lon',
            zoom=15,
            height=600,
        )
        fig.update_layout(mapbox_style="carto-positron")
        fig.update_traces(marker=dict(size=15))
        fig.add_trace(go.Scattermapbox(mode='markers+text',
            lat=df['lat'],
            lon=df['lon'],
            text=df['label'],
            textfont=dict(size=12,color='green'),
            textposition='bottom center',
            showlegend=False
            )
        )
        fig.update_layout(hovermode=False)
        return fig



def get_coffee():
    coffee = random_coffee()
    if len(coffee) > 0: 
        #    st.table(coffee[["Restaurant","Cuisine", "Building", "Level"]])
        st.markdown(coffee[["Restaurant","Cuisine", "Building", "Level","Open","Close"]].style.hide(axis="index").to_html(), unsafe_allow_html=True)
        coffee_choice = coffee["Restaurant"].tolist()
        address_coffee = coffee["Address"].tolist()
        coffee_rest_link = coffee["Link"].tolist()
        url = coffee_rest_link[0]
        st.write("Check out the menu for %s" % coffee_choice[0], "here: %s" % url)
        st.write("Here's the address if you need it: %s" % address_coffee[0] )
        st.markdown("***HAVE A GOOD COFFEE THERE PARTNER!!*** :sunglasses:")
        buttons = st.columns(3)
        with buttons[1]:
            st.button("Try Again")
        lat = pd.to_numeric(coffee['lat'], errors='coerce')
        lon = pd.to_numeric(coffee['lon'], errors='coerce')
        name = coffee["Restaurant"]
        coffee_map = map_render(lat, lon, name)
        st.write(coffee_map)
        st.write("Sorry, looks like there are no open coffee shops in the area right now")
    else:
        st.write("Please try again later")


def get_lunch():
    lunch = random_lunch()
#    if len(lunch)
    if len(lunch) > 0: 
        st.markdown(lunch[["Restaurant","Cuisine", "Building", "Level","Open","Close"]].style.hide(axis="index").to_html(), unsafe_allow_html=True)
        lunch_choice = lunch["Restaurant"].tolist()
        address_lunch = lunch["Address"].tolist()
        lunch_rest_link = lunch["Link"].tolist()
        url = lunch_rest_link[0]
        st.write("Check out the menu for %s" % lunch_choice[0], "here: %s" % url)
        st.write("Here's the address if you need it: %s" % address_lunch[0] )
        st.markdown("***HAVE A GOOD LUNCH THERE PARTNER!!*** :sunglasses:")
        buttons = st.columns(3)
        with buttons[1]:
            st.button("Try Again")
        lat = pd.to_numeric(lunch['lat'], errors='coerce')
        lon = pd.to_numeric(lunch['lon'], errors='coerce')
        name = lunch["Restaurant"]
        lunch_map = map_render(lat, lon, name)
        lunch_map
    else: 
        st.write("Please try again later")






def main3():
#    st.title("Streamlit Button Example")

    # Initialize session state
    if 'button_clicked' not in st.session_state:
        st.session_state.button_clicked = False

    # Create a button
    things = st.columns(3)
    with things[1]:
        button_clicked = st.button("Click me!")

    # Check if the button was clicked
    if button_clicked:
        if not st.session_state.button_clicked:
            st.session_state.button_clicked = True
        else:
            st.session_state.button_clicked = False

    # Display the result of the button click
    if st.session_state.button_clicked:
        st.write("You clicked the button! Nice! But wrong button!!")


def main_mvp():
    selection = st.selectbox("Select an Option", ["Options","I need Coffee... bad", "Lunch Please!"])
    if selection == "I need Coffee... bad":
        get_coffee()
    elif selection == "Lunch Please!":
        get_lunch()
    else:
        st.write("You'll need to make a selection to get this thing going")
        main3()

if __name__ == "__main__":
    main_mvp()










