import streamlit as st
import requests
from firebase_admin import firestore

# Initialize Firestore client
if 'db' not in st.session_state:
    st.session_state.db = firestore.client()
db = st.session_state.db

def fetch_data_from_api(campaign_profile, selected_products, primary_objective, num_contents):
    # Ensure campaign_profile contains required fields
    campaign_profile['product'] = selected_products
    campaign_profile['primary_objective'] = primary_objective

    lst = []
    for ch in campaign_profile['channel']:
        if ch == "LinkedIn":
            ch = "SM-" + ch
        if ch == "Email":
            ch = "DM-" + ch
        if ch == "Google Ads":
            ch = "Google_Ads"
        lst.append(ch)
    campaign_profile["channel"] = lst

    api_url = 'http://35.239.173.177:7999/process-features/'  # Update with your API URL

    print(campaign_profile)

    try:
        response = requests.post(api_url, json=campaign_profile)
        
        if response.status_code != 200:
            st.error(f"API request failed with status code: {response.status_code}")
            return None
        
        external_data = response.json()
        return external_data

    except requests.RequestException as e:
        st.error(f"An error occurred while requesting: {e}")
        return None

def main():
    st.header('Enter your Objective and Product/Services description')
    
    objectives = [
        'Increase Brand Awareness', 'Generate Leads or Sales', 'Engage with Audience', 
        'Boost Website Traffic', 'Improve SEO Rankings'
    ]

    if 'selected_campaign_profile' in st.session_state:
        campaign_data = st.session_state.selected_campaign_profile
        st.subheader(f"Selected Campaign Profile: {campaign_data['profile_name']}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Age:** {', '.join(campaign_data['age'])}")
            st.write(f"**Gender:** {', '.join(campaign_data['gender'])}")
            st.write(f"**Income Level:** {', '.join(campaign_data['income_level'])}")
            st.write(f"**Region:** {', '.join(campaign_data['region'])}")
            st.write(f"**Marital Status:** {', '.join(campaign_data['marital_status'])}")
        with col2:
            st.write(f"**Online Presence:** {', '.join(campaign_data['online_presence'])}")
            st.write(f"**Device Preference:** {', '.join(campaign_data['device_preference'])}")
            st.write(f"**Internet Usage:** {', '.join(campaign_data['internet_usage'])}")
            st.write(f"**Channel:** {', '.join(campaign_data['channel'])}")

        primary_objective = st.multiselect("Primary Objectives", objectives)
        custom_products = st.text_area("Enter Product/service description (comma separated)").split(',')

        # Remove any empty strings from the list
        selected_products = [product.strip() for product in custom_products if product.strip()]

        num_contents = st.selectbox("Number of Contents", range(1, 11), index=0)
        
        if st.button("Generate"):
            if selected_products and primary_objective:
                # Fetch data from API based on selected products, objectives, and number of contents
                generated_content = fetch_data_from_api(campaign_data, selected_products, primary_objective, num_contents)
                print(generated_content)
        
                if generated_content:
                    st.header('The MAGIC is here⚡')
                    
                    # Display LLM Response
                    with st.expander("CampAIgn Suggestions"):
                        st.write("##### Here's the Campaign for you (LLM Response)")
                        for idx,response in enumerate(generated_content.get("LLM_Response", [])):
                            st.subheader(f'**LLM Response {idx + 1}**')
                            st.write(response)
                            st.write(f"**Market Score:** {generated_content['Market_score'][idx]}/10")  # Assuming it's a single score
                            st.write(f"**Market Reason:** {generated_content['Market_score_reason'][idx]}")
                            st.write(f"**Legal Score:** {generated_content['Legal_score'][idx]}/10")  # Assuming it's a single score
                            st.write(f"**Legal Reason:** {generated_content['Legal_score_reason'][idx]}") 

                    
                    # Display Campaigns with expanders
                    with st.expander("View Reference Campaigns"):
                        for idx, campaign in enumerate(generated_content.get("Campaigns", [])):
                            st.write(f"### Campaign {idx + 1}")
                            st.write(campaign)
                            st.write(f"**Similarity Percentage:** {generated_content['Score'][idx]*100:.2f}")

                    # Display Market Score with expander
                    
                else:
                    st.warning("No content fetched from API.")
            else:
                st.warning("Please enter at least one product and select at least one objective.")
    else:
        st.warning("Please select a campaign profile from CohortProfiles.py.")

if __name__ == '__main__':
    main()
