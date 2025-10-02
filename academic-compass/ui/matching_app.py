
import streamlit as st
from matching.matcher import OrgMatcher

# Initialize matcher
@st.cache_resource
def load_matcher():
    return OrgMatcher()

matcher = load_matcher()

st.set_page_config(page_title="Organization Name Matcher", layout="centered")
st.title("🏢 Organization Name Matcher")
st.markdown("""
Enter any organization or funder name.  
The system will normalize, match it using vector similarity, and return the canonical name.
""")

org_input = st.text_input("🔍 Enter organization/funder name", placeholder="e.g., NIH, Stanford Univ., UCLA Med Ctr")

if org_input:
    with st.spinner("Matching..."):
        result = matcher.match(org_input)
    
    st.markdown("### 🧾 Match Result")
    st.write(f"**Input:** `{result['input']}`")
    st.write(f"**Normalized:** `{result['normalized']}`")
    st.write(f"**Top Match:** `{result['match']}`")
    st.write(f"**Canonical:** `{result['canonical']}`")

