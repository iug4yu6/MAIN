import streamlit as st
from datetime import datetime
from supabase import create_client

# Supabase Setup
url = "https://rybiomxtctmhidbuslmn.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ5YmlvbXh0Y3RtaGlkYnVzbG1uIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDI4MzI4NTcsImV4cCI6MjA1ODQwODg1N30.UEPHZlnrl-mx51S6SM-ohxYR_9W8eICIoFegMj8KBRI"
supabase = create_client(url, key)

# Page Config
st.set_page_config(page_title="Restaurant Feedback", layout="centered", page_icon="🍲")
st.markdown("<h1 style='text-align:center;'>🍽️ Restaurant Feedback Form 🍽️</h1>", unsafe_allow_html=True)
st.markdown("---")

# Helper: Rating to Emoji
def get_emoji(rating):
    return ["😞 Very Bad", "😕 Bad", "😐 Okay", "🙂 Good", "😄 Excellent"][rating - 1]

# 👉 Name & Email Fields
name = st.text_input("Name", placeholder="Enter your name")
email = st.text_input("Email", placeholder="Enter your email")

st.markdown("---")

# 👉 Sliders for Ratings
col1, col2, col3 = st.columns(3)
with col1:
    food_rating = st.slider("Food 🍲", 1, 5, 3)
    st.markdown(f"<div style='text-align:center;font-size:22px'>{get_emoji(food_rating)}</div>", unsafe_allow_html=True)
with col2:
    service_rating = st.slider("Service 🧑‍🍳", 1, 5, 3)
    st.markdown(f"<div style='text-align:center;font-size:22px'>{get_emoji(service_rating)}</div>", unsafe_allow_html=True)
with col3:
    ambience_rating = st.slider("Ambience 🎶", 1, 5, 3)
    st.markdown(f"<div style='text-align:center;font-size:22px'>{get_emoji(ambience_rating)}</div>", unsafe_allow_html=True)

st.markdown("---")

# 👉 Best Things
best_things = st.multiselect("What did you like the most? 💖", [
    "Tasty Food", "Quick Service", "Friendly Staff", "Ambience", "Cleanliness"
])

# 👉 Extra Feedback
additional_feedback = st.text_area("Any suggestions or comments? ✍️", placeholder="So how was it ?")

# 👉 Submit Button
if st.button("✅ Submit Feedback"):
    if not name or not email:
        st.warning("Please fill in both name and email.")
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = {
            "timestamp": timestamp,
            "name": name,
            "email": email,
            "food_rating": food_rating,
            "service_rating": service_rating,
            "ambience_rating": ambience_rating,
            "best_things": ", ".join(best_things),
            "additional_feedback": additional_feedback
        }
        res = supabase.table("feedback").insert(data).execute()

        if res.data:
            st.balloons()
            st.success("Thank you for your valuable feedback! 🎉 make sure for checking your email to get coupon 💖")
        else:
            st.error("Something went wrong. Report Staff !")
