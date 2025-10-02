# app.py

import streamlit as st
from agent.run_agent import ResearchExpertAgent

st.set_page_config(page_title="🔬 Research Expert Agent Chat")

# Initialize agent
if "agent" not in st.session_state:
    st.session_state.agent = ResearchExpertAgent()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🧑‍🔬 Research Expert Agent (Chat Mode)")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input box
user_input = st.chat_input("Ask your research question here!")

if user_input:
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Agent processes query
    summary, eval_score = st.session_state.agent.process_query(user_input)

    # Build response
    response = f"**Summary:** {summary}\n\n**Self-Eval Score:** {eval_score:.2f}"

    # Add agent response to chat
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Display agent response
    with st.chat_message("assistant"):
        st.markdown(response)

# Optionally: Feedback input
with st.expander("💬 Provide Feedback"):
    feedback_text = st.text_area("What feedback do you have for the agent?")
    if st.button("Submit Feedback"):
        st.session_state.agent.store_feedback(feedback_text)
        st.success("✅ Feedback submitted!")

# Debug: Show episodic memory
with st.sidebar:
    st.subheader("🧠 Episodic Memory")
    st.write(st.session_state.agent.episodic_memory.get_recent_events())

    st.subheader("📚 Feedback Log")
    st.write(st.session_state.agent.feedback_handler.get_all_feedback())

with st.sidebar:
    st.subheader("🗂️ Interaction Logs")
    logs = st.session_state.agent.logger.read_logs()
    st.json(logs[-5:] if logs else "No logs yet.")  # Show last 5 turns


# feedback loop: 
# Query ➜ Retrieval ➜ Rerank ➜ LLM ➜ Self-Eval ➜ Self-Tune ➜ Log ➜ Feedback ➜ Log

# Run the app with:
# streamlit run app.py
# Make sure to have the required packages installed:
