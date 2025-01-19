import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
import time

# Function to get followers count for a Spotify user
def get_followers_count(spotify, user_id):
    """Fetch the followers count of a Spotify user."""
    try:
        user_profile = spotify.user(user_id)
        return user_profile.get('followers', {}).get('total', 0)
    except Exception as e:
        st.error(f"Error fetching followers: {e}")
        return None

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
    token_info = spotify_auth.get_cached_token()

    if not token_info:
        auth_url = spotify_auth.get_authorize_url()
        st.write("[Click here to authenticate with Spotify]({auth_url})")
        st.stop()

    spotify = spotipy.Spotify(auth=token_info['access_token'])

    # Get current user's profile
    user = spotify.current_user()
    if user:
        st.success(f"Connected as {user['display_name']}")
        user_id = user['id']

        # Initialize session state for followers
        if "followers_count" not in st.session_state:
            st.session_state["followers_count"] = get_followers_count(spotify, user_id)

        # Display current followers count
        current_followers_count = st.session_state["followers_count"]
        st.write(f"Current Followers: {current_followers_count}")

        # Polling for new followers
        st.write("Listening for follower count updates...")

        # Check for updates periodically
        new_followers_count = get_followers_count(spotify, user_id)

        if new_followers_count is not None and new_followers_count > current_followers_count:
            st.write(f":tada: Your followers increased! New Total: {new_followers_count}")
            st.session_state["followers_count"] = new_followers_count

        # Refresh the app after a short delay
        time.sleep(3)
        st.experimental_rerun()

except Exception as e:
    st.error(f"Error connecting to Spotify API: {e}")
