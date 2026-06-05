from ollama import chat
from datetime import datetime
while True:

    sentence = input("Enter a sentence (type 'exit' to quit): ")
    if sentence.lower() == "exit":
        print("Goodbye!")
        break

    response = chat(
        model="llama3:8b",
        messages=[
            {
                "role": "user",
                "content": f"""
                You are an English speaking coach.

                Analyze this sentnece:
                {sentence}
                
                Return exactly in this format:
                Corrected sentence:
                <corrected sentence>
                Mistakes:
                - mistake 1
                - mistake 2
                Explanation
                <short explanation in one sentence
                Fluency score:
                <number>/10

                Only list real mistakes.
                Only identify actual grammer mistake.

                If the sentence is already grammatically correct, write:

                Mistakes:
                - No grammer mistkaes found.
                Do not explain words that are already correct.
                Do not invent mistakes.
                Do not suggest changes unless they are necessary.
                """
            }
        ]   
    )
    result = response.message.content
    print("\n" + "=" * 50)
    print(result)
    print("=" * 50 + "\n")

    current_time = datetime.now().strftime("%d-%m-%Y %H:%M:S")

    with open("history.txt", "a",encoding="utf-8") as file:
        file.write(f"\n[{current_time}]\n")
        file.write(f"Sentence: {sentence}\n")
        file.write(result)
        file.write("\n" + "=" * 50 + "\n\n")
