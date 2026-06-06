import streamlit as st
import sounddevice as sd
from scipy.io.wavfile import write
import whisper
from ollama import chat
import re
from reportlab.pdfgen import canvas

model = whisper.load_model("base")
scores = []

try:
    with open("scores.txt", "r") as file:
        for line in file:
            scores.append(int(line.strip()))
except:
    pass


st.set_page_config(
    page_title="AI Speaking Coach",
    page_icon="🎤",
    layout="wide"
)

st.title("🎤 AI Speaking Coach")

st.write(
    "Improve your English speaking with AI feedback."
)
seconds = st.selectbox("Select Recording Duration", [5,10,15,20])

if st.button("🎙 Start Recording"):
    


    fs = 44100

    recording = sd.rec(
        int(seconds * fs),
        samplerate=fs,
        channels=1
    )

    sd.wait()

    write("voice.wav", fs, recording)

    st.success("Recording Complete!")

    result = model.transcribe("voice.wav")

    sentence = result["text"]
    st.session_state["sentence"] = sentence

    st.subheader("Your Speech")
    st.write(sentence)

    response = chat(
    model="llama3:8b",
    messages=[
        {
            "role": "user",
            "content": f"""
            You are an English speaking coach.

            Analyze this sentence:

            {sentence}

Return exactly in this format:

Corrected sentence:
<corrected sentence>

Mistakes:
- mistake 1
- mistake 2

Explanation:
<short explanation>

Fluency score:
<number>/10
"""
            }
        ]
    )

    analysis = response.message.content
    from datetime import datetime

    current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    with open("history.txt", "a", encoding="utf-8") as file:
        file.write("\n" + "=" * 60 + "\n")
        file.write(f"[{current_time}]\n")
        file.write(f"Sentence: {sentence}\n")
        file.write(analysis + "\n")
    st.subheader("Analysis")
    st.write(analysis)
    match = re.search(r'(\d+)/10', analysis)

    if match:
        score = int(match.group(1))
        st.session_state["score"] = score

        scores.append(score)

        with open("scores.txt", "a") as file:
            file.write(f"{score}\n")

        st.subheader("Fluency Score")
        st.success(f"{score}/10")
        if score < 4:
            level = "Beginner"

        elif score < 7:
            level = "Intermediate"

        elif score < 9:
            level = "Advanced"

        else:
            level = "Fluent"

        st.session_state["level"] = level

        st.subheader("Speaking Level")
        st.success(level)
        

    st.sidebar.header("📊 Statistics")

    if len(scores) > 0:

        average_score = sum(scores) / len(scores)
        best_score = max(scores)

        st.sidebar.write(f"Total Sessions: {len(scores)}")
        st.sidebar.write(f"Average Score: {average_score:.1f}/10")
        st.sidebar.write(f"Best Score: {best_score}/10")
    st.sidebar.subheader("📈 Progress Chart")

    if len(scores) > 0:
         st.sidebar.line_chart(scores)
st.sidebar.divider()

if st.sidebar.button("📜 View History"):

    try:
        with open(
            "history.txt",
            "r",
            encoding="utf-8"
        ) as file:

            st.subheader("📜 Speaking History")

            st.text(file.read())

    except:
        st.error("History file not found")

if "sentence" in st.session_state:

    if st.button("📄 Generate PDF Report"):

            pdf = canvas.Canvas("Speaking_Report.pdf")

            pdf.setTitle("AI Speaking Coach Report")

            pdf.drawString(
                100,
                800,
                "AI Speaking Coach Report"
            )

            pdf.drawString(
                100,
                760,
                f"Sentence: {st.session_state.get('sentence','No Data')}"
            )

            pdf.drawString(
                100,
                730,
                f"Fluency Score: {st.session_state.get('score',0)}/10"
            )

            pdf.drawString(
                100,
                700,
                f"Speaking Level: {st.session_state.get('level','Unknown')}"
            )

            pdf.save()

            st.success("PDF Generated Successfully!")

            with open("Speaking_Report.pdf", "rb") as pdf_file:
                st.download_button(
                    label="⬇ Download PDF",
                    data=pdf_file,
                    file_name="Speaking_Report.pdf",
                    mime="application/pdf"
                )