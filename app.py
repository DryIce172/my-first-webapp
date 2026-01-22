import streamlit as st
from streamlit_js_eval import get_geolocation
import requests
import datetime
import pytz

# --- 1. GET COORDINATES FROM BROWSER ---
# This line triggers the "Allow Location" popup in the user's browser
location = get_geolocation()

# --- 2. CONVERT COORDINATES TO CITY NAME ---
if location:
    lat = location['coords']['latitude']
    lon = location['coords']['longitude']
    
    try:
        # We use OpenStreetMap's free API to turn Lat/Lon into a City Name
        geo_url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
        # User-Agent is required by OpenStreetMap's policy
        headers = {'User-Agent': 'MyWeatherApp/1.0'}
        response = requests.get(geo_url, headers=headers).json()
        
        address = response.get('address', {})
        # Different areas use different keys (city, town, or suburb)
        city = address.get('city') or address.get('town') or address.get('suburb') or "Tokyo"
        country = address.get('country')
        country_code = address.get('country_code', 'in').lower()
        
    except Exception:
        city, country_code = "Bengaluru", "in"
else:
    # While waiting for user to click "Allow", or if they deny it
    st.info("Please allow location access to personalize your dashboard!")
    city, country_code = "Bengaluru", "in"

# --- 3. TIMEZONE & WEATHER LOGIC ---
# India uses one timezone ID ('Asia/Kolkata'), but we use our 'city' for the display
tz = pytz.timezone("Asia/Kolkata")
local_now = datetime.datetime.now(tz)

# Get weather based on the SPECIFIC city found via coordinates
weather_report = requests.get(f"https://wttr.in/{city}?format=%C+%t").text

# --- 4. THE UI ---
st.title(f"Welcome to {city}!")
st.metric("Local Time", local_now.strftime("%I:%M %p"))
st.info(f"📍 **Current Location:** {city}\n\n🌤️ **Weather:** {weather_report}")

# (Insert your News and Joke logic here using country_code and city)






#####################

NEWS_API_KEY = st.secrets["news_key"]

st.set_page_config(page_title="My First Python Web App", page_icon="🌤️")

# 3. Determine Greeting based on LOCAL hour
hour = local_now.hour
if 5 <= hour < 12:
    greeting = "Good morning"
elif 12 <= hour < 17:
    greeting = "Good afternoon"
elif 17 <= hour < 22:
    greeting = "Good evening"
else:
    greeting = "Gosh, it is late — hope you are doing fine"



col1, col2 = st.columns(2)

with col1:
    st.info(f"📍 **Location:** {city}, {country}")
    try:
        w_data = requests.get(f"https://wttr.in/{detected_city}?format=%C+%t").text
        st.metric("Weather", w_data)
    except:
        st.write("Weather unavailable")

with col2:
    try:
        j = requests.get("https://official-joke-api.appspot.com/random_joke").json()
        st.success(f"**Joke of the Day:**\n\n{j['setup']} — {j['punchline']}")
    except:
        st.write("No jokes today :(")

# 3. News Section
st.divider()
st.write("### 📰 Top News")
try:
    url = f"https://newsapi.org/v2/top-headlines?country={country_code}&apiKey={NEWS_API_KEY}"
    articles = requests.get(url).json().get('articles', [])[:3]
    for art in articles:
        st.write(f"**{art['title']}**")
        st.caption(f"Source: {art['source']['name']}")
except:
    st.write("Could not load news.")

# 4. The Cartoon
st.write("### 🐮 Motivational Cow")
st.code("""
      ^__^
      (oo)\_______
      (__)\       )\/\\
          ||----w |
          ||     ||

""", language=None)










