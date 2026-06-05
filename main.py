
def correct_sentence(sentence):
    corrections = {
        "i am work in GIS": "I work in GIS",
        "he don't like cricket": "He doesn't like cricket",
        "she go to school": "She goes to school",
        "they is playing": "They are plaing"
    }

    if sentence in corrections:
        return corrections[sentence]
    else:
        return "Sentence not found"
sentence = input("Enter a sentence: ")
result = correct_sentence(sentence)
print("Correct sentence:")
print(result)