import streamlit as st
from ai import get_json_response

system_prompt_flexibility = """
Role: You are a specialized Health & Fitness Architect focused on flexibility and mobility. Your goal is to gather user data and generate a structured JSON response containing a customized flexibility strategy.

Phase 1: Information Gathering
Before generating the plan, you must ensure you have the following data points from the onboarding questions. If they are missing from the user's input, ask for them:

- Email: User's email address.
- Age: User's age in years.
- Birth: User's birth date.
- Gender: User's gender.
- Access: Access to gym or equipment (e.g., full gym, home equipment, bodyweight only).
- Weight: User's weight in pounds.
- Height: User's height in feet.
- Allergies: Any allergies.
- Diet: Dietary preferences or restrictions (e.g., Vegan, Keto).
- Health: Any health conditions.
- Goal: Specific goal (e.g., Mobility, Flexibility, Injury Prevention).
- Timeline: Timeline for achieving goals.
- Activity Level: Current activity level (Sedentary to Athlete).
- Sleep Patterns: Average sleep per night.
- Daily Schedule: User's daily availability for workouts.

Phase 2: JSON Response Requirements
Once the data is collected, your response must be valid JSON only. Use the following schema:

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
  "flexibility_strategy": {
    "focus_areas": ["string"],
    "session_duration": "string",
    "weekly_frequency": "string",
    "sample_routine": [
      {
        "exercise_name": "string",
        "duration_or_reps": "string",
        "focus": "string"
      }
    ],
    "recovery_recommendations": "string"
  },
  "safety_disclaimer": "This plan is for informational purposes. Consult a physician before beginning any new physical activity or exercise regimen."
}
"""

def flexibility_plans():
    st.subheader("🧘 Flexibility & Mobility Plan Recommendations")

    if st.session_state.get('user_questions') is not None:
        if st.button("🚀 Generate Flexibility Plan", key="flexibility_generate_button"):
            answer = st.session_state['user_questions']
            user_prompt = f"the user is {answer.get('email', 'unknown')} and the user is {answer.get('age', 'unknown')} years old, and the user is born on {answer.get('birth', 'unknown')} and the user is {answer.get('gender', 'unknown')} and the user has {answer.get('access', 'unknown')} access to a gym and the user weighs {answer.get('weight', 'unknown')} pounds and the user is {answer.get('height', 'unknown')} feet tall and the user has allergies of {answer.get('allergies', [])} and the user's diet is {answer.get('diet', [])} and the user's health conditions are {answer.get('health', [])} and the user's goal is {answer.get('goal', 'unknown')} with a timeline of {answer.get('timeline', 'unknown')} and activity level is {answer.get('activity_level', 'unknown')} and sleep patterns are {answer.get('sleep_patterns', 'unknown')} and daily schedule is {answer.get('daily_schedule', 'unknown')}"

            response = get_json_response(system_prompt_flexibility, user_prompt)

            if 'flexibility_strategy' in response:
                st.session_state['flexibility_plan'] = response
                st.success("✅ Flexibility plan generated successfully!")
            else:
                st.error("❌ Error: Unable to generate flexibility plan. Response received:")
                st.json(response)

        if st.session_state.get('flexibility_plan') is not None:
            response = st.session_state['flexibility_plan']
            st.markdown("### 🧘 Flexibility Strategy")
            st.markdown(f"**Focus Areas:** {', '.join(response['flexibility_strategy']['focus_areas'])}")
            st.markdown(f"**Session Duration:** {response['flexibility_strategy']['session_duration']}")
            st.markdown(f"**Weekly Frequency:** {response['flexibility_strategy']['weekly_frequency']}")

            with st.expander("📅 Sample Routine"):
                for item in response['flexibility_strategy']['sample_routine']:
                    st.markdown(f"- {item['exercise_name']}: {item['duration_or_reps']} ({item['focus']})")

            st.markdown(f"**Recovery Recommendations:** {response['flexibility_strategy']['recovery_recommendations']}")

            st.markdown("### ⚠️ Safety Disclaimer")
            st.info(response.get('safety_disclaimer', 'Consult a physician before beginning any new exercise regimen.'))
    else:
        st.warning("📝 Please complete onboarding first.")
        if st.button("🔄 Go to Onboarding", key="flexibility_onboarding_button"):
            st.session_state['needs_onboarding'] = True
            st.rerun()