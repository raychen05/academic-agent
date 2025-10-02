import streamlit as st
from agent.memory import MemoryManager
from agent.self_learning import SelfLearningAgent

# ---------------------------
# Init
# ---------------------------
st.set_page_config(page_title="🧠 Self-Learning Agent", layout="centered")
st.title("🧠 Self-Learning Agent")
st.write("Personalize your AI research assistant.")

memory = MemoryManager()
agent = SelfLearningAgent(memory)

# ---------------------------
# User ID
# ---------------------------
user_id = st.text_input("👤 User ID", placeholder="alice")

# ---------------------------
# Profile Form
# ---------------------------
st.subheader("🗂️ Create or Update Profile")

interests = st.text_area(
    "🔬 Research Interests (one per line)",
    placeholder="machine learning\ncomputational biology"
)

pref_format = st.selectbox(
    "📋 Preferred Output Format",
    ["brief", "detailed", "bullet points"]
)

fav_journals = st.text_input(
    "📚 Favorite Journals (comma separated)",
    placeholder="Nature, Neuron"
)

if st.button("✅ Save Profile"):
    interests_list = [i.strip() for i in interests.splitlines() if i.strip()]
    preferences = {
        "format": pref_format,
        "favorite_journals": [j.strip() for j in fav_journals.split(",") if j.strip()]
    }

    agent.store_user_profile(user_id, interests_list, preferences)
    st.success(f"✅ Profile for {user_id} saved!")

# ---------------------------
# Retrieve Profile
# ---------------------------
st.subheader("🔍 View Your Stored Profile")

if st.button("🔎 Retrieve Profile"):
    profile = agent.retrieve_user_profile(user_id)
    if profile:
        st.text_area("🧾 Stored Profile", value=profile, height=150)
    else:
        st.warning("No profile found for this user!")

# ---------------------------
# Personalized Query
# ---------------------------
st.subheader("🤖 Personalized Recommendation")

query = st.text_input("💡 Ask your AI a question", placeholder="Find latest papers on GNNs")

if st.button("🚀 Get Personalized Answer"):
    answer = agent.recommend(user_id, query)
    st.text_area("🎯 Personalized Response", value=answer, height=200)