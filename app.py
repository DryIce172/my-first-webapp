import streamlit as st
import datetime
import requests
import pytz  # New library for timezone handling

# --- SETTINGS ---
NEWS_API_KEY = st.secrets["news_key"]

st.set_page_config(page_title="My First Python Web App", page_icon="🌤️")

# 1. Automatic Location Detection
try:
    loc_res = requests.get('http://ip-api.com/json/').json()
    city = loc_res.get('city', 'New York')
    country = loc_res.get('country', 'USA')
    country_code = loc_res.get('countryCode', 'us').lower()
    tz_string = loc_res.get('timezone', 'UTC') # e.g., 'Asia/Kolkata'
except:
    city, country, country_code = "New York", "USA", "us"

# 2. Fix the Time Logic
# Get the current time in UTC, then convert it to the user's timezone
utc_now = datetime.datetime.now(datetime.timezone.utc)
user_tz = pytz.timezone(tz_string)
local_now = utc_now.astimezone(user_tz)

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
st.title(f"{greeting}, {city}!")
st.subheader(f"📅 {local_now.strftime('%A, %B %d, %Y | %I:%M %p')}")
st.caption(f"Timezone detected as: {tz_string}")

col1, col2 = st.columns(2)

with col1:
    st.info(f"📍 **Location:** {city}, {country}")
    try:
        w_data = requests.get(f"https://wttr.in/{city}?format=%C+%t").text
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


