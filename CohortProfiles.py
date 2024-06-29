
import streamlit as st
from firebase_admin import firestore

# Function to initialize Firestore client if not initialized
def initialize_firestore():
    if 'db' not in st.session_state:
        st.session_state.db = firestore.client()
    return st.session_state.db

# Function to display campaign profile details
def display_campaign_profile(campaign_data):
    st.subheader(f"Campaign Profile: {campaign_data['profile_name']}")
    st.write(f"**Age:** {', '.join(campaign_data.get('age', []))}")
    st.write(f"**Gender:** {', '.join(campaign_data.get('gender', []))}")
    st.write(f"**Income Level:** {', '.join(campaign_data.get('income_level', []))}")
    st.write(f"**Region:** {', '.join(campaign_data.get('region', []))}")
    st.write(f"**Marital Status:** {', '.join(campaign_data.get('marital_status', []))}")
    st.write(f"**Online Presence:** {', '.join(campaign_data.get('online_presence', []))}")
    st.write(f"**Device Preference:** {', '.join(campaign_data.get('device_preference', []))}")
    st.write(f"**Internet Usage:** {', '.join(campaign_data.get('internet_usage', []))}")
    st.write(f"**Channel:** {', '.join(campaign_data.get('channel', []))}")

    # Button to select profile and redirect to campaign.py
    if st.button(f"Select {campaign_data['profile_name']}"):
        st.session_state.selected_campaign_profile = campaign_data
        st.experimental_rerun()

# Function to create a new campaign profile
def create_campaign_profile(db, username, profile_name, age, gender, income_level, region,
                            marital_status, online_presence, device_preference,
                            internet_usage, channel):
    # Mapping user-friendly channel names to backend-friendly ones
    channel_mapping = {
        "LinkedIn": "SM-LinkedIn",
        "Email": "DM-Email",
        "Google Ads": "Google_Ads",
        "Instagram": "Instagram",
        "Twitter": "Twitter"
    }
    mapped_channels = [channel_mapping[ch] for ch in channel]

    campaign_data = {
        "profile_name": profile_name,
        "age": age,
        "gender": gender,
        "income_level": income_level,
        "region": region,
        "marital_status": marital_status,
        "online_presence": online_presence,
        "device_preference": device_preference,
        "internet_usage": internet_usage,
        "channel": mapped_channels,
        "username": username
    }

    # Add the profile to Firestore
    db.collection('CampaignProfiles').document(profile_name).set(campaign_data)
    st.success(f"Campaign profile '{profile_name}' created successfully!")

    # Display the created profile details
    display_campaign_profile(campaign_data)

# Main Streamlit app function
def app():
    # Initialize Firestore client if not initialized
    db = initialize_firestore()

    st.header('Campaign Profiles')

    # Display existing campaign profiles of the current user
    current_username = st.session_state.get('username', None)
    if current_username:
        campaign_profiles_ref = db.collection('CampaignProfiles').where('username', '==', current_username).stream()
        for campaign_doc in campaign_profiles_ref:
            campaign_data = campaign_doc.to_dict()
            profile_name = campaign_data.get('profile_name')

            # Display profile details in an expander
            with st.expander(f"{profile_name}"):
                display_campaign_profile(campaign_data)

                # Delete button for each profile
                if st.button(f"Delete {profile_name}", key=f"delete_{profile_name}"):
                    db.collection('CampaignProfiles').document(profile_name).delete()
                    st.success(f"{profile_name} deleted successfully!")
                    st.experimental_rerun()  # Refresh the page to update the list

        # Create a new campaign profile section
        st.subheader('Create a New Campaign Profile')
        profile_name = st.text_input("Profile Name", max_chars=50)
        age = st.multiselect("Age", ["0-17", "18-24", "25-34", "35-54", "55+"])
        gender = st.multiselect("Gender", ["Male", "Female", "Others"])
        income_level = st.multiselect("Income Level", ["Low Income", "Middle Income", "High Income"])
        region = st.multiselect("Region", ["North-East", "West", "South", "Middle-West"])
        marital_status = st.multiselect("Marital Status", ["Single", "Married", "Divorced"])
        online_presence = st.multiselect("Online Presence", ["Regular", "Occasional", "Frequent"])
        device_preference = st.multiselect("Device Preference", ["Mobile", "Tablet", "Desktop"])
        internet_usage = st.multiselect("Internet Usage", ["Light", "Moderate", "Heavy"])
        channel_display = ["LinkedIn", "Email", "Google Ads", "Instagram", "Twitter"]
        channel = st.multiselect("Channel", channel_display)

        # Create campaign profile button
        if st.button("Create Campaign Profile"):
            if profile_name:
                create_campaign_profile(db, current_username, profile_name, age, gender, income_level, region,
                                        marital_status, online_presence, device_preference,
                                        internet_usage, channel)
            else:
                st.warning("Profile Name is required to create a campaign profile.")
    else:
        st.warning("Please log in to view and create campaign profiles.")

# Main function to run the Streamlit app
def main():
    app()

if __name__ == '__main__':
    main()

