import requests
from dotenv import load_dotenv
import os
import streamlit as st

# Load environment variables from .env file
load_dotenv()

# Access environment variables
CLIENT_ID = os.getenv("Client_ID")
CLIENT_SECRET = os.getenv("Client_Secret")

# Obtain access token
def get_access_token():
    url = "https://api.prokerala.com/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    response = requests.post(url, headers=headers, data=data)
    access_token = response.json().get("access_token")
    return access_token

# Fetch coordinates from city name using geocoding
def get_coordinates(city):
    url = f"https://geocode.xyz/{city}?json=1"
    response = requests.get(url)
    data = response.json()
    latitude = data.get("latt")
    longitude = data.get("longt")
    return f"{latitude},{longitude}"

# Perform Kundli matching
def perform_kundli_matching(girl_dob):
    access_token = get_access_token()
    # girl_coordinates = get_coordinates(girl_city)
    url = "https://api.prokerala.com/v2/astrology/kundli-matching"
    headers = {"Authorization": f"Bearer {access_token}"}
    girl_dob_iso = girl_dob.strftime("%Y-%m-%dT%H:%M:%S%z")
    print(girl_dob_iso)
    # print(girl_coordinates)
    data = {
        "ayanamsa": 1,
        "girl_coordinates":  "19.9975,73.7898",
        "girl_dob": girl_dob_iso,
        "boy_coordinates" : "19.9975,73.7898",
        "boy_dob" : "1995-02-07T01:47:00+05:30",
        "la": "en"
    }
    response = requests.post(url, headers=headers, json=data)
    return response

# Streamlit UI
st.title("Kundli Matching Application")
# girl_city = st.text_input("Enter Girl's City")
girl_dob = st.date_input("Enter Girl's Birthdate")

if st.button("Match Kundlis"):
    if girl_dob:
        matching_result = perform_kundli_matching(girl_dob)
        st.text(matching_result)
    else:
        st.warning("Please enter the required information.")
