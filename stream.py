import streamlit as st
import json
from app import extract_memories, respond_with_memories, respond_with_memories_personality

st.title("Personalized Memory Assistant")

st.markdown("""
Enter up to 30 past user messages, your current question, and select a personality for the assistant.
""")

st.subheader("Step 1: Enter User Messages")
messages_input = st.text_area(
    "Enter up to 30 messages (one per line):",
    height=300,
)
user_messages = [msg.strip() for msg in messages_input.split("\n") if msg.strip()][:30]


st.subheader("Step 2: Enter Your Question")
user_question = st.text_input("Your question to the assistant:")

st.subheader("Step 3: Select Personality")
personality = st.selectbox(
    "Choose personality:",
    options=["calm_mentor", "witty_friend", "therapist"],
    index=0
)

if st.button("Generate Responses"):
    if not user_messages:
        st.error("Please enter at least one user message.")
    else:
        with st.spinner("Extracting memories..."):
            memories = extract_memories(user_messages)

        st.subheader("Extracted Memories")
        st.json(memories)

        with st.spinner("Generating response without personality..."):
            response_no_personality = respond_with_memories(user_question, memories)

        st.subheader("Response Without Personality")
        st.text_area("Response:", value=response_no_personality, height=150)

        with st.spinner(f"Generating response with personality ({personality})..."):
            response_with_personality = respond_with_memories_personality(user_question, memories, personality=personality)

        st.subheader(f"Response With Personality ({personality})")
        st.text_area("Response:", value=response_with_personality, height=150)
