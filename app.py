import streamlit as st
import datetime
import requests

# --- SETTINGS ---
NEWS_API_KEY = "YOUR_API_KEY_HERE"

st.set_page_config(page_title="My First Python Web App", page_icon="🌤️")

# 1. Automatic Location Detection
try:
    loc = requests.get('http://ip-api.com/json/').json()
    city = loc.get('city', 'New York')
    country = loc.get('country', 'USA')
    country_code = loc.get('countryCode', 'us').lower()
except:
    city, country, country_code = "New York", "USA", "us"

# 2. UI Layout
st.title(f"👋 Welcome to {city}!")
st.subheader(f"{datetime.datetime.now().strftime('%A, %B %d')}")

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