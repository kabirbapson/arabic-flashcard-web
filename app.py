import streamlit as st
import pandas as pd
import random
import arabic_reshaper

# -------- FIX ARABIC --------
def fix_arabic(text):
    return arabic_reshaper.reshape(text)

# -------- LOAD DATA --------
@st.cache_data
def load_data():
    try:
        data = pd.read_csv("data/words_to_learn.csv")
    except FileNotFoundError:
        data = pd.read_csv("data/arabic_words.csv")
    return data.to_dict(orient="records")

# -------- INIT STATE --------
if "words" not in st.session_state:
    st.session_state.words = load_data()

if "current" not in st.session_state:
    st.session_state.current = random.choice(st.session_state.words)

if "show_answer" not in st.session_state:
    st.session_state.show_answer = False

# -------- ACTION FUNCTIONS --------
def next_card():
    if len(st.session_state.words) > 0:
        st.session_state.current = random.choice(st.session_state.words)
        st.session_state.show_answer = False

def flip_card():
    st.session_state.show_answer = not st.session_state.show_answer

def mark_known():
    if st.session_state.current in st.session_state.words:
        st.session_state.words.remove(st.session_state.current)

    pd.DataFrame(st.session_state.words).to_csv(
        "data/words_to_learn.csv", index=False
    )

    if len(st.session_state.words) > 0:
        st.session_state.current = random.choice(st.session_state.words)

    st.session_state.show_answer = False

# -------- PROGRESS --------
total = len(load_data())
remaining = len(st.session_state.words)
learned = total - remaining
percent = int((learned / total) * 100)

# -------- UI --------
st.set_page_config(page_title="Bappi's Arabic Flashcard", page_icon="📚")

st.title("📚 Bappi's Arabic Flashcard")

st.progress(percent)
st.write(f"Learned: {learned}/{total} ({percent}%)")

st.divider()

# -------- CARD DISPLAY --------
if len(st.session_state.words) == 0:
    st.success("🎉 You have learned all words!")
else:
    if not st.session_state.show_answer:
        st.subheader("Arabic")
        st.markdown(
            f"<h1 style='text-align:center; direction:rtl;'>{fix_arabic(st.session_state.current['Arabic'])}</h1>",
            unsafe_allow_html=True
        )
    else:
        st.subheader("English")
        st.markdown(
            f"<h1 style='text-align:center;'>{st.session_state.current['English']}</h1>",
            unsafe_allow_html=True
        )

st.divider()

# -------- BUTTONS --------
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("❌ Don't know"):
        next_card()
        st.rerun()

with col2:
    if st.button("🔄 Flip"):
        flip_card()
        st.rerun()

with col3:
    if st.button("✅ I know"):
        mark_known()
        st.rerun()