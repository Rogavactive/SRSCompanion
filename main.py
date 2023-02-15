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

def askQuestions(questions):
    questionsToShow = []
    for elem in questions:
        elem.showAfterRuns = max(0, elem.showAfterRuns - 1)
        if elem.showAfterRuns == 0:
            questionsToShow.append(elem)
    questionCount = len(questionsToShow)
    print("\n \033[1m *** " + str(questionCount) + " question(s) *** \033[0m" )
    correctCount = 0
    for i, elem in enumerate(questionsToShow):
        print("\nQuestion (" + str(i+1) + "/" + str(questionCount) + "): \033[94m" + elem.question + "\033[0m")
        userAnswer = input("What's your answer:\033[92m")
        print("\033[0mCorrect answer was:\033[92m" + elem.answer + "\033[0m")
        if elem.answer.lower() == userAnswer.lower():
            correctCount = correctCount + 1
            elem.previousEasiness = elem.previousEasiness + 1
        else:
            correctString = ""
            while correctString != "y" and correctString != "n":
                correctString = input("was it correct?(\033[92my\033[0m/\033[91mn\033[0m):")
                if correctString == "y":
                    correctCount = correctCount + 1
                    elem.previousEasiness = elem.previousEasiness + 1
                else:
                    elem.previousEasiness = 1
        elem.showAfterRuns = elem.previousEasiness

    print("\n You answered correctly to \033[92m" + str(correctCount) + "\033[0m questions out of " + str(questionCount))
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
    askQuestions(questions)