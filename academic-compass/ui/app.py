# ui/app.py

import streamlit as st
from agent.planner import Planner
from agent.state import AgentState

# Optional: Set Streamlit page config
st.set_page_config(
    page_title="ResearchCompass",
    page_icon="🧭",
    layout="wide"
)

# Initialize the Agent Planner
planner = Planner()

st.title("📚 ResearchCompass")
st.write("Your AI-powered Academic Research Navigator")

# Persistent session state for chat history
if 'history' not in st.session_state:
    st.session_state.history = []

# Input box for user question
query = st.text_input("🔍 Enter your research question:")

# When user clicks the button
if st.button("Ask AI"):
    if query.strip() == "":
        st.warning("Please enter a valid research question.")
    else:
        # Create a new agent state
        state = AgentState(query=query)

        # Run the planner reasoning loop
        answer = planner.plan_steps(state)

        # Save to history
        st.session_state.history.append({
            "query": query,
            "answer": answer,
            "retrieved": state.retrieved_chunks,
            "feedback": state.feedback,
            "self_eval": state.self_eval
        })

# Display chat-like history
if st.session_state.history:
    st.markdown("## 🗂️ Conversation History")
    for i, entry in enumerate(st.session_state.history[::-1], 1):
        st.markdown(f"**Q{i}:** {entry['query']}")
        st.markdown(f"**Retrieved Context:** {entry['retrieved']}")
        st.markdown(f"**🧠 AI Answer:** {entry['answer']}")
        st.markdown(f"**⭐ User Feedback:** {entry['feedback']}")
        st.markdown(f"**✅ Self-Eval Score:** {entry['self_eval']}")
        st.markdown("---")


# Run the Streamlit app with:
# streamlit run ui/app.py
# Open your browser to http://localhost:8501 to view the app
# Make sure to have the vector database initialized before running the app
# python scripts/init_db.py 