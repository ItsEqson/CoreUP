import streamlit as st
import datetime


def onboarding():
    with st.form("Question Form"):
        email = st.text_input("Input your Email Address")

        age = st.slider("Enter Your Age")

        birth = st.date_input("Enter your Date of Birth", min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today())

        gender = st.radio(
            "Are you,",
            ["Male", "Female"]
            )

        access = st.radio(
            "Do you Have access to a Gym",
            ["Yes", "No"]
            )
        
        weight = st.text_input("Enter your weight in Pounds")

        height = st.text_input("Enter your height in Feet")

        allergies = st.multiselect(
        "What are your allergies?",
        ["None", "Milk", "Eggs", "Fish", "Shellfish", "Tree nuts", "Peanuts", "Wheat", "Soy", "Sesame", "Corn", "Sulfites", "Mustard", "Celery", "Lupin", "Kiwi", "Banana", "Avocado", "Beef", "Pork", "Chicken", "Gelatin", "Honey", "Yeast", "Cocoa", "Garlic", "Onion", "Tomatoes", "Potatoes", "Strawberries", "Chocolate", "Caffeine", "Alcohol", "MSG", "Artificial colors", "Artificial sweeteners", "Rice", "Oats", "Coconut", "Pineapple", "Mango", "Citrus", "Berries"],
        )
        diet = st.multiselect(
        "What is your diet?",
        ["None", "Vegetarian", "Vegan", "Keto", "Paleo", "Mediterranean", "Atkins", "Gluten-free", "Dairy-free", "Low-carb", "High-protein", "Intermittent fasting", "Carnivore", "Pescatarian", "Halal", "Kosher", "Raw food", "Whole30", "DASH", "Flexitarian"]
        )

        health = st.multiselect(
        "What are your health conditions?",
        ["None", "Diabetes", "Hypertension", "Heart Disease", "Asthma", "Arthritis", "Osteoporosis", "Migraine", "Depression", "Anxiety", "Cancer", "Obesity", "Thyroid disorders", "Chronic fatigue syndrome", "Fibromyalgia", "IBS", "GERD", "Kidney disease", "Liver disease", "Stroke", "Epilepsy", "Multiple sclerosis", "Parkinson's disease", "Alzheimer's disease", "Bipolar disorder", "Schizophrenia", "PTSD", "OCD", "Eating disorders", "ADHD", "Autism", "Sleep disorders", "Chronic pain", "Back pain", "Joint pain", "Headaches", "Allergies", "Skin conditions", "Respiratory issues", "Digestive issues"]
        )

        goal = st.selectbox(
            "What is your fitness goal?",
            ["Fat Loss", "Hypertrophy", "Maintenance", "Other"]
        )

        timeline = st.text_input("What is your timeline for achieving this goal? (e.g., 3 months, 6 months)")

        activity_level = st.selectbox(
            "What is your current activity level?",
            ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Athlete"]
        )

        sleep_patterns = st.text_input("Describe your sleep patterns (e.g., 7-8 hours per night)")

        daily_schedule = st.text_area("Describe your typical daily schedule (e.g., work hours, meal times)")

        if st.form_submit_button("Submit"):
            st.session_state['needs_onboarding'] = False

            user_questions = {
                "email": email,
                "age": age,
                "birth": birth,
                "gender": gender,
                "access": access,
                "weight": weight,
                "height": height,
                "allergies": allergies,
                "diet": diet,
                "health": health,
                "goal": goal,
                "timeline": timeline,
                "activity_level": activity_level,
                "sleep_patterns": sleep_patterns,
                "daily_schedule": daily_schedule
            }
            st.session_state['user_questions'] = user_questions

            st.rerun()