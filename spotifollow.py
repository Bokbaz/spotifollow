import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
from time import sleep
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PIL import Image

# Function to send an email notification
def send_email_notification(new_followers, new_follower_names):
    sender_email = "your_email@example.com"
    sender_password = "your_email_password"
    recipient_email = "jan.sarbaz@yahoo.com"

    subject = "New Spotify Followers Notification"
    body = f"You have new followers!\n\nTotal Followers: {new_followers}\n\nNew Followers:\n" + "\n".join(new_follower_names)

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the SMTP server and send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        print("Email notification sent!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Function to get followers details for a Spotify artist/user
def get_followers_details(spotify, user_id):
    """Fetch the followers' details of a Spotify user/artist."""
    try:
        followers = spotify.user_followers(user_id)  # Assuming a valid method exists
        return [follower['display_name'] for follower in followers['items']]
    except Exception as e:
        st.error(f"Error fetching followers: {e}")
        return []

# Streamlit App Setup
st.title("Spotify Follower Notifier")

# Using Streamlit secrets to get Spotify API credentials
client_id = st.secrets["spotify_client_id"]
client_secret = st.secrets["spotify_client_secret"]
redirect_uri = "https://spotifollowbok.streamlit.app/"  # Fixed redirect URI
