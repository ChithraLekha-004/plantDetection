import streamlit as st
import pandas as pd
from pymongo import MongoClient

def get_database():
        client = MongoClient(st.secrets["mongo"]["CONNECTION_STRING"])
        return client.get_database("db")

def feedback_section_admin():
    feedback_database = get_database()
    feedback_collection = feedback_database["feedbacks"]

    def get_all_feedback():
        feedbacks = feedback_collection.find({}, {"_id":0})
        return feedbacks
    
    st.title("Feedbacks")
    st.subheader("All Feedbacks")
    feedbacks_all = get_all_feedback()
    df = pd.DataFrame(list(feedbacks_all))
    df.index += 1
    st.table(df)


def feedback_section():
    def get_current_users_feedback(username):   
        feedbacks = feedback_collection.find({"username": username}, {"_id":0})
        return feedbacks
    
    feedback_database = get_database()
    feedback_collection = feedback_database["feedbacks"]
    
    st.title("Feedbacks")

    with st.container():
        feedback_message = st.text_area(label="Enter your feedback here: ")
        send_button = st.button('Send')

    if send_button:
        feedback_collection.insert_one(
            {
                "username": st.session_state["username"],
                "feedback_message": feedback_message
            }
        )
        st.success("Feedback sent successfully.")

    st.divider()
    st.subheader("Your Feedbacks")
    feedbacks_current_user = get_current_users_feedback(st.session_state['username'])
    df = pd.DataFrame(list(feedbacks_current_user))
    df.index += 1
    st.table(df)

if 'authentication_status' not in st.session_state \
    or st.session_state['authentication_status'] == None \
        or st.session_state['authentication_status'] == False:
    st.warning("Login from Services section to access this feature.")
elif st.session_state['username'] == 'admin':
    feedback_section_admin()
else:
    feedback_section()