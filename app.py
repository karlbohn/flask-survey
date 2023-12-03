from flask import Flask, render_template, flash, redirect, session, request
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

response_key = "response"

@app.route("/")
def survey_init():
    """Initializes survey on homepage"""

    return render_template("survey-init.html", survey=survey)

@app.route("/start", methods=["POST"])
def start():
    """Clear session of responses"""
    session[response_key] = []
    return redirect("/questions/0")

@app.route("/answer", methods=["POST"])
def handle_question():
    """Save response and redirect to next question."""

    choice = request.form['answer']

    responses = session[response_key]
    responses.append(choice)
    session[response_key] = responses

    if (len(responses) == len(survey.questions)):

        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")

@app.route("/questions/<int:question_num>")
def show_question(question_num):
    """Show current question"""

    responses = session.get(response_key)

    if (responses is None):
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        return redirect("/complete")

    if (len(responses) != question_num):
        flash(f"Invalid question id: {question_num}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[question_num]
    return render_template(
        "question.html", question_num=question_num, question=question)

@app.route("/complete")
def complete():
    """Survey complete. Shows completion page."""

    return render_template("completion.html")