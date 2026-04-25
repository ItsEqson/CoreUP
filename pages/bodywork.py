import streamlit as st
from ai import get_json_response

system_prompt_bodywork = """
Role: You are a specialized Health & Fitness Architect focused on bodywork and muscle growth. Your goal is to gather user data and generate a structured JSON response containing a customized exercise and bodywork strategy.

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
- Goal: Specific goal (e.g., Muscle Growth, Abs Definition, Strength Building).
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
  "bodywork_strategy": {
    "focus_areas": ["string"],
    "progressive_overload_plan": "string",
    "recovery_recommendations": "string",
    "supplementation_suggestions": ["string"]
  },
  "safety_disclaimer": "This plan is for informational purposes. Consult a physician before beginning any new physical activity or exercise regimen."
}
"""

def bodywork_plans():
    st.subheader("💪 Bodywork & Muscle Growth Plan Recommendations")

    if st.session_state.get('user_questions') is not None:
        if st.button("🚀 Generate Bodywork Plan", key="bodywork_generate_button"):
            answer = st.session_state['user_questions']
            user_prompt = f"the user is {answer.get('email', 'unknown')} and the user is {answer.get('age', 'unknown')} years old, and the user is {answer.get('gender', 'unknown')} and the user {'has' if answer.get('gym_access') else 'does not have'} access to a gym and the user weighs {answer.get('weight', 'unknown')} pounds and the user is {answer.get('height', 'unknown')} feet tall and the user has allergies of {answer.get('allergies', [])} and the user's diet is {answer.get('diet', [])} and the user's health conditions are {answer.get('health', [])} and the user's goal is {answer.get('goal', 'unknown')} with a timeline of {answer.get('timeline', 'unknown')} and activity level is {answer.get('activity_level', 'unknown')} and sleep patterns are {answer.get('sleep_patterns', 'unknown')} and daily schedule is {answer.get('daily_schedule', 'unknown')}"

            response = get_json_response(system_prompt_bodywork, user_prompt)

            if 'exercise_strategy' in response and 'bodywork_strategy' in response:
                st.session_state['bodywork_plan'] = response
                st.success("✅ Bodywork plan generated successfully!")
            else:
                st.error("❌ Error: Unable to generate bodywork plan. Response received:")
                st.json(response)

        if st.session_state.get('bodywork_plan') is not None:
            response = st.session_state['bodywork_plan']

            # Use columns for better layout
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 🏋️‍♂️ Exercise Strategy")
                st.markdown(f"**Program Split:** {response['exercise_strategy']['program_split']}")

                with st.expander("📅 Weekly Schedule"):
                    for day in response['exercise_strategy']['weekly_schedule']:
                        st.markdown(f"**Day {day['day_number']}: {day['focus']}**")
                        for ex in day['exercises']:
                            st.markdown(f"- {ex['name']}: {ex['sets']} sets, {ex['reps_or_duration']}, rest {ex['rest_period']}")

            with col2:
                st.markdown("### 🧘 Bodywork Strategy")
                st.markdown(f"**Focus Areas:** {', '.join(response['bodywork_strategy']['focus_areas'])}")
                st.markdown(f"**Progressive Overload Plan:** {response['bodywork_strategy']['progressive_overload_plan']}")
                st.markdown(f"**Recovery Recommendations:** {response['bodywork_strategy']['recovery_recommendations']}")
                st.markdown(f"**Supplementation Suggestions:** {', '.join(response['bodywork_strategy']['supplementation_suggestions'])}")

            st.markdown("### ⚠️ Safety Disclaimer")
            st.info(response.get('safety_disclaimer', 'Consult a physician before starting any new exercise program.'))
    else:
        st.warning("📝 Please complete onboarding first.")
        if st.button("🔄 Go to Onboarding", key="bodywork_onboarding_button"):
            st.session_state['needs_onboarding'] = True
            st.rerun()