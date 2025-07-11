
import streamlit as st
import pandas as pd
from datetime import date, datetime
import os

st.set_page_config(page_title="Daily Mood Tracker", layout="centered")

# Title
st.markdown("<h1 style='text-align: center; color: #43A047;'>🌈 Daily Mood Tracker with Emoji & Journal</h1>", unsafe_allow_html=True)

# Layout: Date and Mood Selection
col1, col2 = st.columns(2)

with col1:
    selected_date = st.date_input("📅 Select the Date", date.today())

with col2:
    mood = st.selectbox(
        "😊 How are you feeling?",
        ["😁 Very Happy", "🙂 Good", "😐 Okay", "😔 Sad", "😡 Angry"]
    )

# Mood rating slider with emoji
emoji_rating = st.slider("🔢 Rate Your Mood", 1, 5, 3)
emoji_display = ["😭", "😞", "😐", "😊", "🤩"][emoji_rating - 1]
st.markdown(f"### Your Mood Rating: {emoji_display}")

# Journal Entry
journal = st.text_area("📝 Write about your day...", height=150, placeholder="Today I felt...")

# Mood-based GIF
if "Very Happy" in mood:
    st.image("https://media.giphy.com/media/l0HlT5gLspHWhQWDu/giphy.gif", caption="Feeling Awesome!")
elif "Sad" in mood:
    st.image("https://media.giphy.com/media/l0MYRzcWPdGQKjJri/giphy.gif", caption="It's okay to feel sad 💙")
elif "Angry" in mood:
    st.image("https://media.giphy.com/media/QBDfR1EC88XfK/giphy.gif", caption="Deep breaths 😤")

# File path
FILE_PATH = "mood_log.xlsx"

# Save button
if st.button("💾 Save Entry"):
    new_data = {
        "Date": [selected_date],
        "Mood": [mood],
        "Mood Rating": [emoji_rating],
        "Journal": [journal],
        "Timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    }

    new_df = pd.DataFrame(new_data)

    if os.path.exists(FILE_PATH):
        existing_df = pd.read_excel(FILE_PATH)
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        updated_df = new_df

    updated_df.to_excel(FILE_PATH, index=False)
    st.success("✅ Mood entry saved successfully!")

# Mood Trend Chart
if os.path.exists(FILE_PATH):
    df = pd.read_excel(FILE_PATH)
    st.subheader("📈 Your Mood Over Time")
    st.line_chart(df["Mood Rating"])

# About section
st.markdown("---")
st.markdown("🔍 *This app helps track your daily emotions and journaling habits. Built with 💚 using Streamlit.*")
