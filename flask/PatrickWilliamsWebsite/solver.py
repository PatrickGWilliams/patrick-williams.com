import json
import sqlalchemy as sa
import os
from flask import (
    Blueprint,
    flash,
    json,
    redirect,
    render_template,
    request,
    url_for,
    current_app,
)
from .models import Bees, Boxes
from . import db
from .app import lbHelper, checkDictionary


bp = Blueprint("solver", __name__, url_prefix="/solver")


def getTodaysLetters():
    todaysLetters = db.session.scalars(sa.select(Bees).order_by(Bees.id.desc())).first()
    if todaysLetters is not None:
        return todaysLetters.letters
    else:
        return "!error!"


def getDict():
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    with open(file_path) as word_file:
        lines = word_file.readlines()
    return lines


@bp.route("/spellingbee", methods=("GET", "POST"))
def spellingbee():
    fillLetters = getTodaysLetters()
    error = None

    if request.method == "POST":

        requiredLetter = request.form["required"]
        letters = sorted(request.form.getlist("letters[]"))
        letters.insert(0, requiredLetter)
        letters = "".join(letters)
        letters = letters.lower()


        repeatChar = False
        for char in letters:
            if letters.count(char) > 1:
                repeatChar = True
                break

        if (len(letters) != 7) or (not letters.isalpha()) or (repeatChar):
            error = "Please enter only one unique letter per field"

        if error is None:
            return redirect(url_for("solver.sbAnswers", letters=letters))

        flash(error)

    return render_template("solver/spellingbee.html", fillLetters=fillLetters)


@bp.route("/spelling_bee_answers/<letters>", methods=("GET", "POST"))
def sbAnswers(letters):
    answer = []
    pangrams = []
    rejected = []
    fromDB = False
    length = 500

    if (len(letters) != 7) or (not letters.isalpha()):
        return redirect(url_for("solver.spellingbee"))

    dbLetters = db.session.scalars(sa.select(Bees).where(Bees.letters == letters)).first()

    if dbLetters is None:
        checker = checkDictionary.dictionaryChecker(letters, getDict())
        checker.findPangrams(letters, checker.answer)
        answer = checker.answer
        pangrams = checker.pangrams
        fromDB = False
    else:
        answer = json.loads(dbLetters.accepted)
        pangrams = json.loads(dbLetters.pangrams)
        fromDB = True

    answerTitle = "Answers"
    pangramTitle = "Pangrams"

    if answer is None:
        answer = "No suitable words found."
    elif len(answer) == 1:
        answerTitle = "Answer"

    if answer is not None:
        length = ((len(answer) / 5) * 20) + 200
        if length < 1000:
         length = 1000

    if pangrams is None:
        pangrams = ["No panagrams can be made with the provided letters."]
    elif len(pangrams) == 1:
        pangramTitle = "Pangram"

    return render_template(
        "solver/answer.html",
        answer=answer,
        pangrams=pangrams,
        fromDB=fromDB,
        length=length,
    )


@bp.route("/letter_box", methods=("GET", "POST"))
def letterBox():
    error = None
    oneWord = None
    twoWord = None
    sides = None
    length = 0

    lbData = db.session.scalars(sa.select(Boxes).order_by(Boxes.id.desc())).first()

    if lbData is not None:
        oneWord = json.loads(lbData.one_word)
        twoWord = json.loads(lbData.two_word)
        sides = json.loads(lbData.sides)

    if twoWord:
        length = 400 + (25 * (len(twoWord) / 2))

    if length < 1300:
        length = 1300

    if request.method == "POST":
        starter = request.form["starter"]
        remaining = request.form.getlist("remaining[]")

        remainingLength = len(remaining)
        if remainingLength > 10:
            error = "You can only select 10 letters remaining"
        elif remainingLength < 1:
            error = "You must select at least 1 remaining letter"

        if error is None:
            remainingLetters = "".join(remaining)
            return redirect(
                url_for("solver.lbAnswers", starter=starter, remaining=remainingLetters)
            )

        flash(error)

    return render_template(
        "solver/letter_box.html",
        oneWord=oneWord,
        twoWord=twoWord,
        sides=sides,
        length=length,
    )


@bp.route("/letter_boxed_help/<starter>/<remaining>", methods=("GET", "POST"))
def lbAnswers(starter, remaining):
    lbData = db.session.scalars(sa.select(Boxes).order_by(Boxes.id.desc())).first()
    if lbData is not None:
        answerList = lbHelper.helper(json.loads(lbData.dictionary), remaining, starter)
    else:
        answerList = "Error"
    return render_template("solver/letter_box_help.html", answerList=answerList)
