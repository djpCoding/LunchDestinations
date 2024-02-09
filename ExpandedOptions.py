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
from geopy.geocoders import Nominatim
 



with st.sidebar:
    add_radio = st.selectbox("Options",
                         ("Search for a bumpin' spot", "Submit a new restaraunt option!")
                         )
    if add_radio == "Search for a bumpin' spot": 
        add_radio2 = st.selectbox("Downtown, North loop, or Both", 
                                ("Downtown","North loop","Both")
                                )

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


def geo_location(loc):
    #making an instance of Nominatim class
    geolocator = Nominatim(user_agent="my_request")
    
    #applying geocode method to get the location
    location = geolocator.geocode(loc)
    
    #printing address and coordinates
    return location.latitude, location.longitude

def write_to_rest(df):
    csv_filename = "Restaurants.csv"

    name = df["Restaurant"].tolist()
    name = name[0]
    df.to_csv(csv_filename, mode="a", index= False, header=False)
    st.success("Form Submitted Successfully for  %s" % name)



def form_material():
    with st.form("New Restaurant Submission Form", border = True, clear_on_submit=True):
        st.write("New Restaraunt Submission Form")
        new_rest_name = st.text_input("Name of the Restaraunt")
        c1, c2 = st.columns(2)
        with c1:
            new_rest_cat = st.selectbox("Category", ["","Coffee", "Fast-casual","Dine-in","Drinks"])
        with c2:
            new_rest_cuis = st.text_input("What is the restaraunts cuisine type?")
        co1, co2, co3 = st.columns(3)
        with co1:
            new_rest_build = st.text_input("What building is the restaraunts in?")
        with co2:
            new_rest_level = st.text_input("What floor is the restaraunt on?")
        with co3:
            new_rest_area = st.selectbox("Restaraunt Neighborhood", ["","Downtown","North loop"])
        new_rest_address = st.text_input("What is the restraunt's address?")
        col1, col2 = st.columns(2)
        with col1:
            new_rest_open = st.text_input("What time does the restaraunt open? (am/pm format)","8:00am")
        with col2:
            new_rest_close = st.text_input("What time does the restaraunt close? (am/pm format)","8:00pm")
        new_rest_link = st.text_input("What's the link to the restaraunt's website?")
        submitted = st.form_submit_button("Submit")
        if submitted:
            found = rest[rest["Restaurant"].str.contains(new_rest_name)]
            found = found["Restaurant"].count()
            if found > 0:
                st.write("It looks like this restaraunt has already been added. If this isn't true, please add additional description to the name.")
            else:
                new_rest_coords = geo_location(new_rest_address)
                new_rest_coords = ', '.join(map(str, new_rest_coords))
                new_rest_df = [{"Restaurant": new_rest_name,"Category": new_rest_cat,"Cuisine": new_rest_cuis, 
                               "Building": new_rest_build, "Level": new_rest_level,"Address": new_rest_address, 
                               "Open": new_rest_open,"Close": new_rest_close, "Bfast": "User submission - not configued","Lunch": "User submission - not configued",
                               "Dinner": "User submission - not configued", "Cost": "User submission - not configued","Rating": "User submission - not configued",
                               "Link": new_rest_link,"Area": new_rest_area,
                               "Coordinates": new_rest_coords}]
                new_rest_df = pd.DataFrame(new_rest_df)
                write_to_rest(new_rest_df)
    with open("Restaurants.csv") as file: 
        btn = st.download_button('Download the CSV of Restaraunts', data=file, file_name="restarauntscatalog.csv", mime='text/csv')


if __name__ == "__main__":
    if "submitted" not in st.session_state:
        st.session_state.submitted = False

def transform_upload():
    "text"



# Load up the map for later use
# Coordinates for downtown Minneapolis
minneapolis_coords = pd.DataFrame({"lat": [44.979087279569036],"lon": [-93.2717422460245]})
inspire11_cords = pd.DataFrame({"lat": [44.979087279569036], "lon": [-93.2717422460245]})

def random_coffee():
    filtered_coffee = rest[(current_time > rest['OpenDT']) & (current_time < rest['CloseDT'])]
    filtered_coffee = filtered_coffee.loc[filtered_coffee["Category"]=="Coffee"]
    if add_radio2 is not "Both":
        filtered_coffee = filtered_coffee.loc[filtered_coffee["Area"]==add_radio2]
    if len(filtered_coffee.index) > 0:
        random_coffee_row = filtered_coffee.sample(n=1, replace=False)  
    else: 
        st.write("It looks like there are no open coffee shops right now. Sorry!")
        random_coffee_row = []
    return random_coffee_row

def random_lunch():
    filtered_lunch = rest
    filtered_lunch = filtered_lunch.loc[filtered_lunch["Category"]=="Fast casual"]
    if add_radio2 is not "Both":
        filtered_lunch = filtered_lunch.loc[filtered_lunch["Area"]==add_radio2]
    if len(filtered_lunch) > 0:
        random_lunch_row = filtered_lunch.sample(n=1, replace=False) 
    else:
        st.write("Looks like we don't have any lunch options right now.")
        random_lunch_row = []                 
    return random_lunch_row

def random_drinks():
    filtered_drinks = rest[current_time > rest['OpenDT']]
    filtered_drinks = filtered_drinks.loc[filtered_drinks["Category"]=="Drinks"]
    if add_radio2 is not "Both":
        filtered_drinks = filtered_drinks.loc[filtered_drinks["Area"]==add_radio2]
    if len(filtered_drinks) > 0:
        random_drink_row = filtered_drinks.sample(n=1, replace=False) 
    else:
        st.write("Looks like we don't have any drink options right now.")
        random_drink_row = []                 
    return random_drink_row    

def random_dinner():
    filtered_dinner = rest.loc[rest["Category"]=="Dine-in"]
    filtered_dinner = filtered_dinner[current_time < rest['CloseDT']]
    if add_radio2 is not "Both":
        filtered_dinner = filtered_dinner.loc[filtered_dinner["Area"]==add_radio2]
    if len(filtered_dinner) > 0:
        random_dinner_row = filtered_dinner.sample(n=1, replace=False) 
    else:
        st.write("Looks like we don't have any dinner options right now.")
        random_dinner_row = []                 
    return random_dinner_row   

def map_render(lat, lon, name, area):
        data = {'lat': lat, 'lon': lon, 'size': 500, "label": name}
        df = pd.DataFrame(data)
        df.loc[len(df.index)] = [44.979087279569036, -93.2717422460245, 500, "Inspire11"]
        if area == "North loop":
            zoom_level = 13.75
        elif area == "Downtown":
            zoom_level = 15
        else:
            zoom_level = 15
        fig = px.scatter_mapbox(
            df,
            lat='lat',
            lon='lon',
            zoom=zoom_level,
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
        area = coffee["Area"].tolist()
        area = area[0]
        coffee_map = map_render(lat, lon, name, area)
        st.write(coffee_map)
        st.write(area)
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
        area = lunch["Area"].tolist()
        area = area[0]
        lunch_map = map_render(lat, lon, name, area)
        lunch_map
    else: 
        st.write("Please try again later")

def get_drinks():
    drinks = random_drinks()
    if len(drinks) > 0: 
        st.markdown(drinks[["Restaurant","Cuisine", "Building", "Level","Open","Close"]].style.hide(axis="index").to_html(), unsafe_allow_html=True)
        drinks_choice = drinks["Restaurant"].tolist()
        address_drinks = drinks["Address"].tolist()
        drinks_rest_link = drinks["Link"].tolist()
        url = drinks_rest_link[0]
        st.write("Check out the menu for %s" % drinks_choice[0], "here: %s" % url)
        st.write("Here's the address if you need it: %s" % address_drinks[0] )
        st.markdown("***HAVE A GOOD LIBATION OR TWO THERE PARTNER!!*** :sunglasses:")
        buttons = st.columns(3)
        with buttons[1]:
            st.button("Try Again")
        lat = pd.to_numeric(drinks['lat'], errors='coerce')
        lon = pd.to_numeric(drinks['lon'], errors='coerce')
        name = drinks["Restaurant"]
        area = drinks["Area"].tolist()
        area = area[0]
        drinks_map = map_render(lat, lon, name, area)
        drinks_map
    else: 
        st.write("Please try again later. Looks like there's no open watering hole yet.")

def get_dinner():
    dinner = random_dinner()
    if len(dinner) > 0: 
        st.markdown(dinner[["Restaurant","Cuisine", "Building", "Level","Open","Close"]].style.hide(axis="index").to_html(), unsafe_allow_html=True)
        dinner_choice = dinner["Restaurant"].tolist()
        address_dinner = dinner["Address"].tolist()
        dinner_rest_link = dinner["Link"].tolist()
        url = dinner_rest_link[0]
        st.write("Check out the menu for %s" % dinner_choice[0], "here: %s" % url)
        st.write("Here's the address if you need it: %s" % address_dinner[0] )
        st.markdown("***HAVE A GOOD FANCY FEAST THERE PARTNER!!*** :sunglasses:")
        buttons = st.columns(3)
        with buttons[1]:
            st.button("Try Again")
        lat = pd.to_numeric(dinner['lat'], errors='coerce')
        lon = pd.to_numeric(dinner['lon'], errors='coerce')
        name = dinner["Restaurant"]
        area = dinner["Area"].tolist()
        area = area[0]
        dinner_map = map_render(lat, lon, name, area)
        dinner_map
    else: 
        st.write("OH NO. Not another COVID. We couldn't find anything with your search.")    

if add_radio == "Search for a bumpin' spot":
    # st.image('https://raw.githubusercontent.com/djpCoding/LunchDestinations/main/Inspire11.png')
    st.title("Minneapolis Restaurant Roulette")
    st.markdown("Unsure of where to eat lunch or grab a quick snack? Use this restaurant roulette to find a new (or not so new) location for an option close to the office!")
    

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
        selection = st.selectbox("Select an Option", ["Options","I need Coffee... bad", "Lunch Please!","What a day, it's time for drinks", "I'd like dinner now"])
        if selection == "I need Coffee... bad":
            get_coffee()
        elif selection == "Lunch Please!":
#            meal = st.selectbox("Select which meal you are looking for", ["Lunch","Breakfast","Dinner"])
            get_lunch()
        elif selection == "What a day, it's time for drinks":
            get_drinks()
        elif selection == "I'd like dinner now":
            get_dinner()
        else:
            st.write("You'll need to make a selection to get this thing going")
            main3()

    if __name__ == "__main__":
        main_mvp()

elif add_radio == "Submit a new restaraunt option!":
    st.header("New Restaraunt Submission")
    st.write("Fill out the form or upload new options below to add restaraunt options to the site.")
    form_material()






