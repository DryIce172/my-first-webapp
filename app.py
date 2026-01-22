import streamlit as st
from streamlit_js_eval import streamlit_js_eval
import datetime
import requests
import pytz  # New library for timezone handling

# --- SETTINGS ---
NEWS_API_KEY = st.secrets["news_key"]

# 1. Get the USER'S browser timezone via JavaScript
# This runs in the visitor's browser, not on the server!
user_tz_name = streamlit_js_eval(js_expressions="Intl.DateTimeFormat().resolvedOptions().timeZone", key="tz")

# 2. Use that Timezone to find the City (Fallback to UTC if not loaded yet)
if user_tz_name:
    # Example: 'Asia/Kolkata' -> we want just 'Kolkata' for the weather
    detected_city = user_tz_name.split('/')[-1].replace('_', ' ')
    tz_string = user_tz_name
else:
    detected_city = "Bengaluru" # Default fallback
    tz_string = "UTC"

# 3. Correct Time Logic
utc_now = datetime.datetime.now(datetime.timezone.utc)
user_tz = pytz.timezone(tz_string)
local_now = utc_now.astimezone(user_tz)

# 4. Display the dynamic header
st.title(f"Hello from {detected_city}!")
st.write(f"Your local time is: **{local_now.strftime('%I:%M %p')}**")
st.caption(f"Detected Browser Timezone: {tz_string}")






st.set_page_config(page_title="My First Python Web App", page_icon="🌤️")

# 1. Automatic Location Detection
try:
    loc_res = requests.get('http://ip-api.com/json/').json()
#    city = loc_res.get('city', 'New York')
    country = loc_res.get('country', 'USA')
    country_code = loc_res.get('countryCode', 'us').lower()
    tz_string = loc_res.get('timezone', 'UTC') # e.g., 'Asia/Kolkata'
except:
    , country, country_code = "New York", "USA", "us"

# 2. Fix the Time Logic
# Get the current time in UTC, then convert it to the user's timezone
utc_now = datetime.datetime.now(datetime.timezone.utc)
user_tz = pytz.timezone(tz_string)
# local_now = utc_now.astimezone(user_tz)

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

# 4. Display in Streamlit
st.title(f"{greeting}, {detected_city}!")
st.subheader(f"📅 {local_now.strftime('%A, %B %d, %Y | %I:%M %p')}")
st.caption(f"Timezone detected as: {tz_string}")

col1, col2 = st.columns(2)

with col1:
    st.info(f"📍 **Location:** {detected_city}, {country}")
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



