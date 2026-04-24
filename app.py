import streamlit as st
import requests
import time

API_URL = "https://uselessfacts.jsph.pl/random.json?language=en"

st.set_page_config(page_title="Fun Fact Generator", page_icon="✨", layout="centered")

# -----------------------
# Session State
# -----------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "current_fact" not in st.session_state:
    st.session_state.current_fact = ""

# -----------------------
# Fetch Function
# -----------------------
def fetch_fact():
    try:
        res = requests.get(API_URL, timeout=5)
        res.raise_for_status()
        return res.json().get("text", "No fact found.")
    except:
        return "⚠️ Couldn't fetch a fact. Try again."

# -----------------------
# Header
# -----------------------
st.markdown("""
    <h1 style='text-align:center;'>✨ Fun Fact Generator</h1>
    <p style='text-align:center; font-size:18px;'>Click below to discover something interesting 👇</p>
""", unsafe_allow_html=True)


st.markdown("<hr style='margin-top:10px;'>", unsafe_allow_html=True)

# -----------------------
# Buttons
# -----------------------
col1, col2, col3 = st.columns([1,2,1])

with col2:
    generate = st.button("✨ Generate Fact", use_container_width=True)
    clear = st.button("🗑 Clear History", use_container_width=True)

# -----------------------
# Generate Logic
# -----------------------
if generate:
    with st.spinner("Fetching something cool..."):
        time.sleep(0.4)
        fact = fetch_fact()
        st.session_state.current_fact = fact

        if fact not in st.session_state.history:
            st.session_state.history.insert(0, fact)

# -----------------------
# Fact Card
# -----------------------
if st.session_state.current_fact:
    st.markdown(f"""
        <div style="
            max-width:700px;
            margin:20px auto;
            background: linear-gradient(135deg, #e0f7fa, #e3f2fd);
            padding:25px;
            border-radius:15px;
            font-size:22px;
            color:#003366;
            line-height:1.7;
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
            text-align:center;
        ">
            {st.session_state.current_fact}
        </div>
    """, unsafe_allow_html=True)

# -----------------------
# Clear History
# -----------------------
if clear:
    st.session_state.history = []
    st.toast("History cleared")

# -----------------------
# History
# -----------------------
if st.session_state.history:
    st.markdown("---")
    st.markdown("<h3 style='text-align:center;'>📜 Previous Facts</h3>", unsafe_allow_html=True)

    for i, fact in enumerate(st.session_state.history[:5]):
        with st.expander(f"Fact #{i+1}"):
            st.write(fact)
