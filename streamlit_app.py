import streamlit as st
from pages.home import home
from pages.onboarding import onboarding
from ai import get_json_response
from openai import OpenAI
from db import sign_in, sign_up, sign_out, save_profile, get_profile

# system_prompt = """
# You will give the user Fitness and Diet plans recommendations based on the user's profile. The user will input from thr form Question Form. 
# The user will input their email, age, date of birth, gender, gym acess, weight, height, allergies, Diet, and Health information.

# """

# from supabase import create_client, Client

# @st.cache_resource
# def init_supabase() -> Client:
#     url = st.secrets["SUPABASE_URL"]
#     key = st.secrets["SUPABASE_KEY"]
#     return create_client(url, key)

# supabase = init_supabase()





def initalize_state():
    if 'login_user' not in st.session_state:
        st.session_state['login_user'] = False

    if 'current_user' not in st.session_state:
        st.session_state['current_user'] = None

    if 'user_db' not in st.session_state:
        st.session_state['user_db'] = {"User1": "password1"}
    if 'needs_onboarding' not in st.session_state:
        st.session_state['needs_onboarding'] = False
    if 'user_questions' not in st.session_state:
        st.session_state['user_questions'] = None

initalize_state()





def login():
    with st.form("Login Form"):
        st.title("Login")
        username = st.text_input("Enter your Username")
        password = st.text_input("Enter your Password", type="password")
        
        if st.form_submit_button("Login"):
            # user, err = sign_in(username, password)
            # if err:
            #     st.error(f"Login failed: {err}")
            # else:
                st.session_state['login_user'] = True
                st.session_state['current_user'] = username
                st.rerun()



def signup():
    with st.form("Signup Form"):
        st.title("Sign Up")
        new_username = st.text_input("Choose a Username")
        new_password = st.text_input("Choose a Password", type="password")
        
        if st.form_submit_button("Sign Up"):
            # user, err = sign_up(new_username, new_password)
            # if err:
            #     st.error("Username already exists")
            # else:
                st.session_state['user_db'][new_username] = new_password

                st.session_state['login_user'] = True
                st.session_state['current_user'] = new_username

                st.session_state['needs_onboarding'] = True

                st.success("Account created successfully! Please log in.")
                st.rerun()

def logout():
    st.session_state['login_user'] = False
    st.session_state['current_user'] = None
    st.success("Logged out successfully!")
    st.rerun()






if st.session_state['login_user'] == False:
    st.title("Welcome to Core Up!")
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    with tab1:
        login()
    with tab2: 
        signup()
elif st.session_state['needs_onboarding'] == True:
    onboarding()

else:
    home()
