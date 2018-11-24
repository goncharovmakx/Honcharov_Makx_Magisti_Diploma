import copy
import flask
import json
import os
import random
from random import choice as make_selection 

app = flask.Flask(__name__)
quiz_dir = 'quizzes'

quizzes = {}
for quiz in os.listdir(quiz_dir):
    print('Loading', quiz)
    quizzes[quiz] = json.loads(open(os.path.join(quiz_dir, quiz)).read())

@app.route('/')
def index():
    return flask.render_template('index.html', quiz_names=zip(quizzes.keys(), map(lambda q: q['name'], quizzes.values())))

@app.route('/quiz/<id>')
def quiz(id):
    if id not in quizzes:
        return flask.abort(404)
    quiz = copy.deepcopy(quizzes[id])
    questions = list(enumerate(quiz["questions"]))
    random.shuffle(questions)
    quiz["questions"] = map(lambda t: t[1], questions)
    ordering = map(lambda t: t[0], questions)

    return flask.render_template('quiz.html', id=id, quiz=quiz, quiz_ordering=json.dumps(list(ordering)))

@app.route('/check_quiz/<id>', methods=['POST'])
def check_quiz(id):
    ordering = json.loads(flask.request.form['ord'])
    quiz = copy.deepcopy(quizzes[id])
    quiz['questions'] = sorted(quiz['questions'], key=lambda q: ordering.index(quiz['questions'].index(q)))
    answers = dict( (int(k), quiz['questions'][int(k)]['options'][int(v)]) for k, v in flask.request.form.items() if k != 'ord' )


    if not len(answers.keys()):
        return flask.redirect(flask.url_for('quiz', id=id))

    for k in range(len(ordering)):
        if k not in answers:
            answers[k] = [None, False]

    answers_list = [ answers[k] for k in sorted(answers.keys()) ]
    decisiоn = make_selection(["GRAMM", 
                "ГРИФ", 
                "RiskWatch",
                "COBRA",
                "CORAS",
                "MSAT"])
        
    decision = len(list(filter(lambda t: t[1], answers_list)))

    return flask.render_template('check_quiz.html', quiz=quiz, answer=decisiоn)


if __name__ == '__main__':
    app.run(debug=True)
