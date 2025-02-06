import streamlit as st
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]  # or replace with openai.api_key = "YOUR_OPENAI_API_KEY"
client = openai.OpenAI(api_key=openai.api_key)

def get_feedback(objective: str) -> str:

    # Here is a simple example prompt. You would replace it with the actual requirements/rules you want to check.
    prompt = f"""
You are a helpful assistant. The user has provided an agent story:
"{objective}"

Please assign an alignment grade from A to F and provide constructive feedback on whether this objective follows 
these guidelines. You do not talk about anything else. 
An agent story has the following usual format: As an [Agent Role], operating in 
[Context/Environment], I want to [Objective] by [Actions/Behaviors], interacting with
[Users/Systems/Agents], so that [Desired Outcome/Benefit], success is measure by 
[Success Criteria].

[Agent Role] defines a specific function or identity, for example: predictive maintenance agent, customer support agent,
inventory management agent, etc.
[Context/Environment] describes where and under what conditions the agent operates, for example: within the
manufacturing facility, on an e-commerce website during peak hours, during flight disruptions, etc.
[Objective] specifies what the agent aims to achieve and it should be clear and concise, for example: prevent equipment
failures, proactively manage passenger itineraries, etc.
[Actions/Behaviors] outlines the specific tasks the agent will perform and includes the methods or strategies the agent
uses, for example: analyzing sensor data to predict potential malfunctions and scheduling maintenance activities.
[Users/Systems/Agents] details how the agent communicates or interfaces with users, systems, or other agents, focusing
on understanding integration points and user experience, for example: maintenance scheduling systems and technicians.
[Desired Outcome/Benefit] explains the value provided by the agent’s actions and it should align with business goals, for
example: production processes run smoothly without unexpected interruptions.
[Success Criteria] defines how success will be measured and includes quantitative and qualitative metrics, for example:
reduced equipment downtime, lower maintenance costs, and improved production efficiency.

Here is an example applied to Retail:
As a Personalized Shopping Assistant, operating on the online retail platform, I want to enhance customer shopping experiences by
providing personalized product recommendations and answering customer queries, interacting with customers in real-time via chat
and voice interfaces, so that customers find products they love quickly, increasing satisfaction and sales conversion rates. Success
is measured by increased average order value, higher conversion rates, and positive customer feedback scores.
"""

    # Example for text-davinci-003 or gpt-3.5-turbo. Adjust parameters as needed.

    # If using text-davinci-003:
    # response = openai.Completion.create(
    #     engine="text-davinci-003",
    #     prompt=prompt,
    #     max_tokens=150,
    #     temperature=0.7
    # )
    # feedback = response["choices"][0]["text"].strip()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
             "content": "You are a helpful AI assistant that evaluates agent stories based on specific guidelines."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.7,
    )

    feedback = response.choices[0].message.content.strip()

    return feedback


def main():
    st.title("Agent Story Reviewer")

    # Initialize session state if it doesn't exist
    if "page" not in st.session_state:
        st.session_state.page = "input"
        st.session_state.objective = ""
        st.session_state.feedback = ""

    # Screen 1: Input
    if st.session_state.page == "input":
        st.subheader("Enter your agent story")
        user_objective = st.text_area("Agent Story")

        if st.button("Submit"):
            # Call the OpenAI API to get feedback
            feedback = get_feedback(user_objective)

            # Store results in session state
            st.session_state.objective = user_objective
            st.session_state.feedback = feedback

            # Go to Screen 2
            st.session_state.page = "review"

    # Screen 2: Review
    elif st.session_state.page == "review":
        st.subheader("Review your agent story")
        st.write(f"**Your Agent Story:** {st.session_state.objective}")
        st.write("**Feedback:**")
        st.write(st.session_state.feedback)

        if st.button("One more"):
            # Reset session state for a fresh start
            st.session_state.page = "input"
            st.session_state.objective = ""
            st.session_state.feedback = ""


if __name__ == "__main__":
    main()