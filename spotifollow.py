import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
from datetime import datetime

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
        st.write(f"[Click here to authenticate with Spotify]({auth_url})")
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
        if "follower_increase_count" not in st.session_state:
            st.session_state["follower_increase_count"] = 0

        # Display current followers count dynamically
        followers_display = st.empty()
        increase_display = st.empty()
        current_followers_count = st.session_state["followers_count"]

        # Fetch new followers count
        new_followers_count = get_followers_count(spotify, user_id)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if new_followers_count is not None:
            if new_followers_count != current_followers_count:
                st.session_state["followers_count"] = new_followers_count
                st.session_state["follower_increase_count"] += new_followers_count - current_followers_count
                current_followers_count = new_followers_count
                followers_display.write(
                    f":tada: Followers count updated! New Total: {new_followers_count} \n\nLast Updated: {current_time}"
                )
                increase_display.write(
                    f"Follower Increases Detected: {st.session_state['follower_increase_count']}"
                )
            else:
                followers_display.write(
                    f"No change in followers. Current Total: {current_followers_count} \n\nLast Checked: {current_time}"
                )
                increase_display.write(
                    f"Follower Increases Detected: {st.session_state['follower_increase_count']}"
                )

        # Refresh the app every 3 seconds
        st.experimental_rerun()

except Exception as e:
    st.error(f"Error connecting to Spotify API: {e}")
