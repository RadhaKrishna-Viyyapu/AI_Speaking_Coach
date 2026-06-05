import streamlit as st

st.set_page_config(
    page_title="AI Speaking Coach",
    page_icon="🎤",
    layout="wide"
)

st.title("🎤 AI Speaking Coach")

st.write(
    "Improve your English speaking with AI feedback."
)

if st.button("🎙 Start Recording"):

    st.success(
        "Next step: connect speaking_coach.py here."
    )

st.divider()

st.subheader("Your Speech")

speech_placeholder = st.empty()

st.subheader("Analysis")

analysis_placeholder = st.empty()

st.subheader("Fluency Score")

score_placeholder = st.empty()