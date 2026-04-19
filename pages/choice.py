import streamlit as st
from ai import get_json_response

system_prompt_choice = """
Role: You are a specialized Health & Fitness Architect. Your goal is to gather user data and generate a structured JSON response containing a customized fitness plan based on the user's specific choice of what they want to do.

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
- Goal: Specific goal (e.g., Muscle Growth, Abs Definition, Strength Building, Fat Loss).
- Timeline: Timeline for achieving goals.
- Activity Level: Current activity level (Sedentary to Athlete).
- Sleep Patterns: Average sleep per night.
- Daily Schedule: User's daily availability for workouts.
- User Choice: What the user specifically wants to do (e.g., "Run a 5K", "Get Six Pack Abs", "Deadlift 300lbs", "Lose 20 pounds").

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
  "user_choice_analysis": {
    "choice_summary": "string",
    "feasibility": "string",
    "estimated_duration": "string",
    "difficulty_level": "string"
  },
  "customized_strategy": {
    "dietary_approach": "string",
    "exercise_program": "string",
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
    ],
    "progress_milestones": ["string"]
  },
  "safety_disclaimer": "This plan is for informational purposes. Consult a physician before beginning any new physical activity or restrictive diet."
}
"""

def choice_plans():
    st.subheader("🏋️‍♂️ Custom Fitness Plan Based on Your Choice")

    if st.session_state.get('user_questions') is not None:
        user_choice = st.text_input("🎯 What do you want to achieve? (e.g., 'Run a 5K', 'Get Six Pack Abs', 'Deadlift 300lbs')", key="user_fitness_choice")

        if st.button("🚀 Generate Custom Plan", key="choice_generate_button"):
            if user_choice.strip() == "":
                st.error("❌ Please enter what you want to achieve.")
            else:
                answer = st.session_state['user_questions']
                user_prompt = f"the user is {answer.get('email', 'unknown')} and the user is {answer.get('age', 'unknown')} years old, and the user is born on {answer.get('birth', 'unknown')} and the user is {answer.get('gender', 'unknown')} and the user has {answer.get('access', 'unknown')} access to a gym and the user weighs {answer.get('weight', 'unknown')} pounds and the user is {answer.get('height', 'unknown')} feet tall and the user has allergies of {answer.get('allergies', [])} and the user's diet is {answer.get('diet', [])} and the user's health conditions are {answer.get('health', [])} and the user's goal is {answer.get('goal', 'unknown')} with a timeline of {answer.get('timeline', 'unknown')} and activity level is {answer.get('activity_level', 'unknown')} and sleep patterns are {answer.get('sleep_patterns', 'unknown')} and daily schedule is {answer.get('daily_schedule', 'unknown')}. Most importantly, the user specifically wants to: {user_choice}"

                response = get_json_response(system_prompt_choice, user_prompt)

                if 'user_choice_analysis' in response and 'customized_strategy' in response:
                    st.session_state['choice_plan'] = response
                    st.success("✅ Custom plan generated successfully!")
                else:
                    st.write("❌ Error: Unable to generate custom plan. Response received:")
                    st.json(response)
        
        if st.session_state.get('choice_plan') is not None:
            response = st.session_state['choice_plan']
            
            # Use columns for better layout
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📊 Choice Analysis")
                st.markdown(f"**Summary:** {response['user_choice_analysis']['choice_summary']}")
                st.markdown(f"**Feasibility:** {response['user_choice_analysis']['feasibility']}")
                st.markdown(f"**Estimated Duration:** {response['user_choice_analysis']['estimated_duration']}")
                st.markdown(f"**Difficulty Level:** {response['user_choice_analysis']['difficulty_level']}")
            
            with col2:
                st.markdown("### 🥗 Customized Strategy")
                st.markdown(f"**Dietary Approach:** {response['customized_strategy']['dietary_approach']}")
                st.markdown(f"**Exercise Program:** {response['customized_strategy']['exercise_program']}")
                
                with st.expander("📅 Weekly Schedule"):
                    for day in response['customized_strategy']['weekly_schedule']:
                        st.markdown(f"**Day {day['day_number']}: {day['focus']}**")
                        for ex in day['exercises']:
                            st.markdown(f"- {ex['name']}: {ex['sets']} sets, {ex['reps_or_duration']}, rest {ex['rest_period']}")
                
                with st.expander("🏆 Progress Milestones"):
                    for milestone in response['customized_strategy']['progress_milestones']:
                        st.markdown(f"- {milestone}")
            
            st.markdown("### ⚠️ Safety Disclaimer")
            st.info(response.get('safety_disclaimer', 'Consult a physician before starting any new exercise program.'))
    else:
        st.warning("📝 Please complete onboarding first.")
        if st.button("🔄 Go to Onboarding", key="choice_onboarding_button"):
            st.session_state['needs_onboarding'] = True
            st.rerun()