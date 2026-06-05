import sounddevice as sd
from scipy.io.wavfile import write
from datetime import datetime
from reportlab.pdfgen import canvas
import whisper
from ollama import chat
import re

# Load Whisper model once
model = whisper.load_model("base")

scores =[]

try:
     with  open ("scores.txt", "r") as file:
          for line in file:
               scores.append(int(int.strip()))
except FileNotFoundError:
     pass            

while True:

    print("\n===== AI SPEAKING COACH=====")
    print("1. Practice Speaking")
    print("2. View History")
    print("3. View Statistics")
    print("4. Generate PDF Report")
    print("5. Exit")

    menu_choice = input("\nChoose option:")

    fs = 44100
    seconds = 5
    if menu_choice== "1":
        print("Speak now...")

        recording =sd.rec(int(seconds * fs),samplerate=fs,channels=1)
        sd.wait()
        write("voice.wav", fs, recording)
        print("Recording saved as voice.wav")

        # Convert speech to text
        result = model.transcribe("voice.wav")

        sentence = result["text"]

        print("\nYou said:")
        print(sentence)

        # Send text to Ollama & Grammar Analysis

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

        Only identify genuine grammar mistakes.
        Do not invent mistakes.
        Do not suggest unnecessary corrections.
        If the sentence is already correct, say:

        Mistakes:
        - No grammar mistakes found.
        """
                }
            ]
        )

        analysis = response.message.content

        print("\n" + "=" * 50)
        print(response.message.content)
        print("=" * 50)

        #Score Tracking
        match = re.search(r'(\d+)/10',analysis)

        if match:
            score = int(match.group(1))
            scores.append(score)
            with open("scores.txt","a") as file:
                file.write(f"{score}\n")

            average_score = sum(scores)/len(scores)
            best_score = max(scores)
            print("\n ------ Progress Tracker ------")
            print(f"Current Score : {score}/10")
            print(f"Average Score : {average_score:.1f}/10")
            print(f"Best Score : {best_score}/10")
            if len(scores)>1:
                       improvement = scores[-1]-scores[0]
                       print(f"Improvement : {improvement:+}points")

        print("-----------------------------------------------")

        
    # Save History
        current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        with open("history.txt", "a",encoding="utf-8") as file:
                file.write("\n" + "=" * 60 + "\n")
                file.write(f"\n[{current_time}]\n")
                file.write(f"Sentence: {sentence}\n")
                file.write(analysis)
                if match:
                    file.write("\n")
                    print(f"Current Score : {score}/10")
                    print(f"Average Score : {average_score:.1f}/10")
                    print(f"Best Score     : {best_score}/10")
                    if len(scores)>1:
                       improvement = scores[-1]-scores[0]
                       print(f"Improvement : {improvement:+}points\n")

                file.write("\n" + "=" * 60 + "\n")

# To open History    
    elif menu_choice=="2":
            try:
                 with open("history.txt", "r",encoding="utf-8") as file:
                      print(file.read())
            except:
                 print("History file not found.")

# To open Statistics   
    elif menu_choice=="3":
            if len(scores)>0:
                 
                 average_score = sum(scores)/len(scores)
                 best_score = max(scores)
                 print("\n ======STATISTICS======")
                 print(f"Total Sessions : {len(scores)}")
                 print(f"Average Score : {average_score:.1f}/10")
                 print(f"Best Score     : {best_score}/10")
                 good_sessions = len([s for s in scores if s>=7])
                 print(f"Good Sessions(7+)):{good_sessions}")

                 if len(scores)>1:
                       improvement = scores[-1]-scores[0]
                       print(f"Improvement : {improvement:+}points")
            else:
                 print("No scores available.")
            
            print("\nLast 5 Scores:")
            for s in scores[-5:]:
                 print(f"-{s}/10")

#PDF GENERATION
    elif menu_choice =="4":

        pdf=canvas.Canvas("Speaking_Report.pdf")
        pdf.setTitle("AI Speaking Coach Report")

        pdf.setFont("Helvetica-Bold",18)
        
        pdf.drawString(100,800,"AI Speaking Coach Report")

        pdf.setFont("Helvetica",12)

        pdf.drawString(100,760,f"Total Sessions: {len(scores)}")
        if len(scores)>0:
              average_score =sum(scores)/len(scores)
              best_score = max(scores)

              pdf.drawString(100,730,f"Average Sccore: {average_score:.1f}/10")
              pdf.drawString(100,700,f"Best Score: {best_score}/10")
        if len(scores)>1:
              improvement = scores[-1]-scores[0]
              pdf.drawString(100, 670,f"Improvement: {improvement:+}points")
        if len(scores) > 0:
            if average_score <4:
                level= "Beginner"
            elif average_score <7:
                level= "Intermediate"      
            elif average_score <9:
                level = "Advanced"
            else:
                level = "Fluent"
        else:
             level ="No Data"
        pdf.drawString(
              100,
              640,
              f"Speaking Level: {level}"
        )
        pdf.save()
        print( "\nSpeaking_Report.pdf generated successfully!")
    
# Continue or Exit
    elif menu_choice == "5":
        print("Goodbye!")
        break
