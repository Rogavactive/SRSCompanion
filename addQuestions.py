from dataclasses import dataclass
import json

@dataclass
class QuizQuestion:
    question: str
    answer: str
    showAfterRuns: int
    previousEasiness: int # higher - easier. If we answer correctly + 1. else equals to 1.

class QuizQuestionEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, QuizQuestion):
            return {
                "question": obj.question,
                "answer": obj.answer,
                "showAfterRuns": obj.showAfterRuns,
                "previousEasiness": obj.previousEasiness
            }
        return super().default(obj)

def addQuestions(questions):
    while True:
        q = input("What is the question ?:")
        if q == "quit()":
            saveJson()
            break
        a = input("How should I answer ?:")
        if a == "quit()":
            saveJson()
            break
        areYouSure = input("Question is:\n" + q + "\n and answer to that is \n" + a + "\nare you sure you want to save this?(y/n)")
        if areYouSure == "quit()":
            saveJson()
            break
        if areYouSure == "y":
            questions.append(
                QuizQuestion(
                    question=q,
                    answer=a,
                    showAfterRuns=1,
                    previousEasiness=1
                )
            )
    saveJson()

def saveJson():
    jsonStr = json.dumps(questions, cls=QuizQuestionEncoder)
    with open("data.json", "w") as f:
        f.write(jsonStr)

if __name__ == '__main__':
    questions = []
    with open("data.json", "r") as f:
        questions = json.load(f)
        questions = [
            QuizQuestion(
                question=dct["question"],
                answer=dct["answer"],
                showAfterRuns=dct["showAfterRuns"],
                previousEasiness=dct["previousEasiness"]
            )
            for dct in questions]
    addQuestions(questions)