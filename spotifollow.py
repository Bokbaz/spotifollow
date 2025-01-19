import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
from time import sleep
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PIL import Image
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
import time
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

# Initialize Spotify OAuth
try:
    spotify_auth = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope="user-read-private"
    )
    token_info = spotify_auth.get_access_token(as_dict=False)
    spotify = spotipy.Spotify(auth=token_info)

    # Get current user's profile
    user = spotify.current_user()
    if user:
        st.success(f"Connected as {user['display_name']}")
        user_id = user['id']

        # Initialize session state for followers
        if "followers" not in st.session_state:
            st.session_state["followers"] = set(get_followers_details(spotify, user_id))

        # Display current followers
        current_followers = st.session_state["followers"]
        st.write(f"Current Followers: {len(current_followers)}")

        # Textbox to display new followers
        new_follower_box = st.empty()

        # Polling for new followers
        st.write("Listening for new followers...")

        # Check for updates periodically
        new_followers = set(get_followers_details(spotify, user_id))
        new_follower_names = new_followers - st.session_state["followers"]

        if new_follower_names:
            st.write(f":tada: You have new followers! Total Followers: {len(new_followers)}")
            send_email_notification(len(new_followers), list(new_follower_names))
            new_follower_box.text_area("New Followers:", "\n".join(new_follower_names), height=200)

        # Update session state
        st.session_state["followers"] = new_followers

        # Refresh the app after a short delay
        time.sleep(3)
        st.experimental_rerun()

except Exception as e:
    st.error(f"Error connecting to Spotify API: {e}")

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

# Initialize Spotify OAuth
try:
    spotify_auth = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope="user-read-private"
    )
    token_info = spotify_auth.get_access_token(as_dict=False)
    spotify = spotipy.Spotify(auth=token_info)

    # Get current user's profile
    user = spotify.current_user()
    if user:
        st.success(f"Connected as {user['display_name']}")
        user_id = user['id']

        # Display current followers
        current_followers = get_followers_details(spotify, user_id)
        if current_followers is not None:
            st.session_state["followers"] = set(current_followers)
            st.write(f"Current Followers: {len(current_followers)}")

        # Textbox to display new followers
        new_follower_box = st.empty()

        # Polling for new followers
        st.write("Listening for new followers...")

        while True:
            sleep(3)  # Check every 3 seconds
            new_followers = get_followers_details(spotify, user_id)

            if new_followers is not None:
                if "followers" in st.session_state:
                    new_follower_names = set(new_followers) - st.session_state["followers"]

                    if new_follower_names:
                        st.write(f":tada: You have new followers! Total Followers: {len(new_followers)}")
                        send_email_notification(len(new_followers), list(new_follower_names))
                        new_follower_box.text_area("New Followers:", "\n".join(new_follower_names), height=200)

                    # Update session state
                    st.session_state["followers"] = set(new_followers)
                else:
                    st.session_state["followers"] = set(new_followers)

except Exception as e:
    st.error(f"Error connecting to Spotify API: {e}")
