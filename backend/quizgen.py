import sys
import random
from summarizer import extract_keywords

def generate_cloze_questions(text: str, num_questions: int = 5):
    # get top keywords
    keywords = extract_keywords(text, top_n=num_questions*2)
    # pick a subset for questions
    chosen = keywords[:num_questions]
    questions = []
    for kw in chosen:
        # find a sentence containing the keyword
        for sent in text.split('.'):
            if kw.lower() in sent.lower():
                sentence = sent.strip()
                break
        else:
            sentence = text[:100]
        # create the cloze
        blanked = sentence.replace(kw, "____")
        # build choices: correct + 3 random other keywords
        others = [k for k in keywords if k != kw]
        choices = random.sample(others, min(3, len(others)))
        choices.append(kw)
        random.shuffle(choices)
        questions.append({
            "question": blanked,
            "choices": choices,
            "answer": kw
        })
    return questions

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quizgen.py path/to/textfile.txt")
        sys.exit(1)
    path = sys.argv[1]
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    qs = generate_cloze_questions(text)
    for i, q in enumerate(qs, 1):
        print(f"Q{i}: {q['question']}?")
        for idx, c in enumerate(q['choices'], 1):
            print(f"  {idx}. {c}")
        print(f"  [Answer: {q['answer']}]\n")

