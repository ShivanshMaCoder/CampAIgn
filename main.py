import streamlit as st
from streamlit_option_menu import option_menu
import os
import firebase_admin
from firebase_admin import credentials

# Initialize Firebase if not already initialized

fb_credentials=st.secrets['firebase']['my_project']
if not firebase_admin._apps:
    cred = credentials.Certificate(fb_credentials)
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