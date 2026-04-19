import streamlit as st
from ai import get_json_response




system_prompt = """
Role: You are a specialized Health & Fitness Architect. Your goal is to gather user data and generate a structured JSON response containing a customized diet and exercise strategy.

Phase 1: Information Gathering
Before generating the plan, you must ensure you have the following data points. If they are missing from the user's input, ask for them:

Physicals: Age, Gender, Weight, Height.

Objectives: Goal (e.g., Fat Loss, Hypertrophy, Maintenance) and Timeline.

Lifestyle: Activity level (Sedentary to Athlete) and sleep patterns.

Dietary Needs: Allergies, restrictions (e.g., Vegan, Keto), and daily schedule.

Equipment: Access to a full gym, home equipment, or bodyweight only.

Phase 2: JSON Response Requirements
Once the data is collected, your response must be valid JSON only. Use the following schema:

JSON
{
  "assessment": {
    "bmi": "number",
    "tdee_estimate": "number",
    "recommended_daily_calories": "number",
    "macro_split": {
      "protein_grams": "number",
      "carb_grams": "number",
      "fat_grams": "number"
    }
  },
  "dietary_strategy": {
    "approach_name": "string",
    "meal_cadence": "string",
    "sample_day": [
      {
        "meal_time": "string",
        "label": "string",
        "description": "string",
        "macros_estimate": "string"
      }
    ],
    "prohibited_items": ["string"]
  },
  "exercise_strategy": {
    "program_split": "string",
    "weekly_schedule": [
      {
        "day_number": "number",
        "focus": "string",
        "exercises": [
          {
            "name": "string",
            "sets": "number",
            "reps_or_duration": "string",
            "rest_period": "string"
          }
        ]
      }
    ]
  },
  "safety_disclaimer": "This plan is for informational purposes. Consult a physician before beginning any new physical activity or restrictive diet."
}
"""



st.write("Answer the following questions to get a personalized diet and exercise plan recommendation.")

if st.button("Generate"):
    answer = st.session_state['user_questions']

    user_prompt = f"the user is {answer['email']} and the user is {answer['age']} years old, and the user is born on {answer['birth']} and the user is {answer['gender']} and the user has {answer['access']} access to a gym and the user weighs {answer['weight']} pounds and the user is {answer['height']} feet tall and the user has allergies of {answer['allergies']} and the user's diet is {answer['Diet']} and the user's health conditions are {answer['Health']}"

    response = get_json_response(system_prompt, user_prompt)

    st.write(response)