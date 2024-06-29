
import streamlit as st
import pandas as pd
import requests
from firebase_admin import firestore, storage

def app():
    # Initialize Firestore client
    db = firestore.client()

    if 'username' not in st.session_state or not st.session_state['username']:
        st.error("Please log in to upload files.")
        return

    st.title('Upload Files')

    # File upload widgets
    company_file = st.file_uploader("Upload Company/Brand Document", type=["txt", "csv", "xlsx"])
    copywriting_file = st.file_uploader("Upload Copywriting Details", type=["txt", "csv", "xlsx"])
    historical_file = st.file_uploader("Upload Historical Campaign Data", type=["txt", "csv", "xlsx"])

    if st.button("Upload Files"):
        try:
            # Initialize the storage bucket
            bucket = storage.bucket()

            def upload_file(file, file_type):
                if file:
                    blob = bucket.blob(f"{st.session_state['username']}/{file_type}/{file.name}")
                    blob.upload_from_file(file)
                    blob.make_public()  # Make the file publicly accessible
                    file_url = blob.public_url
                    db.collection('Users').document(st.session_state['username']).set({
                        f'{file_type}_file_url': file_url
                    }, merge=True)
                    st.success(f"{file_type.replace('_', ' ').title()} uploaded successfully!")
                    print(file_url)

            # Upload each file
            upload_file(company_file, 'company_brand_document')
            upload_file(copywriting_file, 'copywriting_details')
            upload_file(historical_file, 'historical_campaign_data')

        except Exception as e:
            st.error(f"Error uploading files: {str(e)}")
            print(f"Error uploading files: {str(e)}")

    st.header('Preview Uploaded Files')
    def preview_file(file_type):
        try:
            username = st.session_state['username']
            user_doc = db.collection('Users').document(username).get()
            if user_doc.exists:
                user_data = user_doc.to_dict()
            else:
                user_data = {}

            file_url = user_data.get(f'{file_type}_file_url')
            if file_url:
                st.subheader(f"{file_type.replace('_', ' ').title()} Preview")
                try:
                    response = requests.get(file_url)
                    response.raise_for_status()  # Raise an exception for HTTP errors
                    if file_url.endswith('.txt'):
                        st.text(response.text)
                    elif file_url.endswith('.csv'):
                        df = pd.read_csv(file_url)
                        st.dataframe(df)
                    elif file_url.endswith('.xlsx'):
                        df = pd.read_excel(file_url)
                        st.dataframe(df)
                except requests.exceptions.HTTPError as http_err:
                    st.error(f"HTTP error occurred: {http_err}")
                except Exception as err:
                    st.error(f"Other error occurred: {err}")
            else:
                st.warning(f"No {file_type.replace('_', ' ').title()} uploaded yet.")
        except Exception as e:
            st.error(f"Error loading {file_type.replace('_', ' ').title()}: {str(e)}")
            print(f"Error loading {file_type}: {str(e)}")

    # Preview each file type
    preview_file('company_brand_document')
    preview_file('copywriting_details')
    preview_file('historical_campaign_data')


# Main function to run the Streamlit app
def main():
    app()

if __name__ == '__main__':
    main()