import streamlit as st
import pandas as pd
import re
import geocoder
import pycountry
from geopy.geocoders import Nominatim
import csv

def get_state_from_location(location):
    geolocator = Nominatim(user_agent="my-app")
    address = geolocator.reverse(location, exactly_one=True)
    if address is not None:
        return address.raw['address']['state']
    else:
        return None

def lookup_programs(state):
    # Load the energy programs CSV file into a Pandas DataFrame
    
    clean_state_abbr = re.sub(r'^US-', '', state)
    
    programs_df = pd.read_csv("datafinal.csv")

    # Filter the DataFrame to only include programs for the specified state
    state_programs = programs_df[programs_df["State"] == clean_state_abbr]

    return state_programs

def state_name_to_abbreviation(state_name):
    for state in pycountry.subdivisions:
        if state_name.lower() == state.name.lower():
            return state.code
    return None

def get_matching_programs(state):
    matching_programs = []
    with open('energy_programs.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['State'] == state:
                matching_programs.append(row)
    return matching_programs

def summarize_with_chatgpt(description):
    prompt = f"Please summarize the following program description:\n\n{description}\n\nSummary:"
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        n=1,
        stop=None,
        timeout=15,
    )
    summary = response.choices[0].text.strip()
    return summary

def summarize_button(row):
    # Add a button to the row that summarizes the program description
    if st.button('Summarize'):
        summary = summarize(row['Description'])
        st.write(summary)

def summarize(description):
    summary = "Dummy data"
    return summary

def summarize_button(row):
    # Add a button to the row that summarizes the program description
    if st.button('Summarize'):
        summary = summarize(row['Description'])
        st.write(summary)

def main():
    st.title("Location to State")

    # Get the user's location from their IP address
    location = geocoder.ip('me').latlng

    # Get the US state from the location
    if location is not None:
        state = get_state_from_location(location)
        if state is not None:
            st.write("State:", state)
            st.write("Abbreviation: ", state_name_to_abbreviation(state))
            matching_programs = lookup_programs(state_name_to_abbreviation(state))
            df = pd.DataFrame(matching_programs)
            st.write(df)
        else:
            st.write("Could not find state from location")
    else:
        st.write("Could not retrieve location")

if __name__ == "__main__":
    main()