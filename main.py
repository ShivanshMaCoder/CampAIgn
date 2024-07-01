import streamlit as st
from streamlit_option_menu import option_menu
import os
import firebase_admin
from firebase_admin import credentials





if not firebase_admin._apps:
    cred = credentials.Certificate({
        "type": st.secrets["firebase"]["type"],
        "project_id": st.secrets["firebase"]["project_id"],
        "private_key_id": st.secrets["firebase"]["private_key_id"],
        "private_key": st.secrets["firebase"]["private_key"].replace('\\n', '\n'),
        "client_email": st.secrets["firebase"]["client_email"],
        "client_id": st.secrets["firebase"]["client_id"],
        "auth_uri": st.secrets["firebase"]["auth_uri"],
        "token_uri": st.secrets["firebase"]["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["firebase"]["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"]
    })
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'marketing-automation-3098a.appspot.com' 
    })

# Import your app modules here
import CohortProfiles, campaign, account, DocsPortal

# Set the page configuration
st.set_page_config(
    page_title="Marketing CampAIgn Automation✨",
)

# Add Google Analytics
analytics_tag = os.getenv('analytics_tag')
if analytics_tag:
    st.markdown(
        f"""
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id={analytics_tag}"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){{dataLayer.push(arguments);}}
            gtag('js', new Date());
            gtag('config', '{analytics_tag}');
        </script>
        """, unsafe_allow_html=True
    )

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        with st.sidebar:
            app = option_menu(
                menu_title='CampAIgn Generator',
                options=['Account', 'Docs Portal', 'Cohort Profiles', 'Campaign'], 
                icons=['person-circle', 'chat-fill', 'info-circle-fill', 'trophy-fill'], 
                menu_icon='chat-text-fill',
                default_index=0,
                styles={
                    "container": {"padding": "5!important", "background-color": 'black'},
                    "icon": {"color": "white", "font-size": "23px"},
                    "nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "blue"},
                    "nav-link-selected": {"background-color": "#02ab21"},
                }
            )

        try:
            if app == "Account":
                account.app()
            elif app == "Docs Portal":
                DocsPortal.app()
            elif app == "Cohort Profiles":
                print("cohort profile called")
                CohortProfiles.app()
            elif app=="Campaign":
                campaign.main()
        except Exception as e:
            st.error(f"Error running app: {str(e)}")

multi_app = MultiApp()
multi_app.run()