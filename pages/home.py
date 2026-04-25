import streamlit as st

from pages.choice import choice_plans
from pages.diet import diet_plans  
from pages.bodywork import bodywork_plans
from pages.exercise import exercise
from pages.flexibility import flexibility_plans

def home():
    st.title("Core Up")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Exercise", "Diet Plans", "Bodywork", "UP Choice", "Flexibility"])
    with tab1:
        exercise()
    with tab2:
        diet_plans()
    with tab3:
        bodywork_plans()
    with tab4:
        choice_plans()
    with tab5:
        flexibility_plans()
