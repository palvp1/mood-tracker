
import streamlit as st
import pandas as pd
import datetime
import os

# ======================== #
#        CONSTANTS         #
# ======================== #

FILE_PATH = "mood_journal.xlsx"
COLUMNS = ["Date", "Mood", "Journal"]
MOODS = {
    "😊 Happy": "Happy",
    "😐 Neutral": "Neutral",
    "😔 Sad": "Sad",
    "😤 Stressed": "Stressed",
    "😴 Tired": "Tired",
    "😄 Excited": "Excited",
}

# ======================== #
#      DATA FUNCTIONS      #
# ======================== #

def load_data():
    if os.path.exists(FILE_PATH):
        try:
            df = pd.read_excel(FILE_PATH)
            df["Date"] = pd.to_datetime(df["Date"]).dt.date  # Ensure Date is clean
            return df
        except Exception as e:
            st.error(f"Error reading Excel file: {e}")
            return pd.DataFrame(columns=COLUMNS)
    else:
        return pd.DataFrame(columns=COLUMNS)

def save_data(df):
    try:
        df.to_excel(FILE_PATH, index=False)
    except Exception as e:
        st.error(f"Failed to save data: {e}")

def already_logged_today(df):
    today = datetime.date.today()
    return today in df["Date"].values

def add_new_entry(df, mood, journal):
    new_entry = {
        "Date": datetime.date.today(),
        "Mood": mood,
        "Journal": journal.strip()
    }
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    return df

# ======================== #
#     UI + MAIN LOGIC      #
# ======================== #

def show_statistics(df):
    st.markdown("### 📊 Mood Summary")
    if df.empty:
        st.info("No data available to show statistics.")
        return

    mood_counts = df["Mood"].value_counts()
    most_common = mood_counts.idxmax()
    st.write("**Most frequent mood:**", most_common)
    st.bar_chart(mood_counts)

def main():
    st.set_page_config(page_title="Mood Tracker", layout="centered")
    st.title("🌞 Daily Mood Tracker with Emoji & Journal")

    df = load_data()

    # Mood Picker
    mood_choice = st.radio("How are you feeling today?", list(MOODS.keys()))
    selected_mood = MOODS[mood_choice]

    # Journal Entry
    journal_text = st.text_area("Write about your day (optional):")

    # Entry Handling
    if already_logged_today(df):
        st.warning("You've already submitted your mood today.")
    elif st.button("Save Today’s Entry"):
        df = add_new_entry(df, selected_mood, journal_text)
        save_data(df)
        st.success("Your entry has been saved!")

    # Show Mood History
    st.markdown("### 📅 Your Mood Journal")
    if not df.empty:
        st.dataframe(df.sort_values("Date", ascending=False))
    else:
        st.info("No entries found yet.")

    # Show Stats
    show_statistics(df)

if __name__ == "__main__":
    main()
