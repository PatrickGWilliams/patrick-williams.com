import json
import os
from flask import Blueprint, flash, json, redirect, render_template, request, url_for, current_app
from PatrickWilliamsWebsite.db import get_db
from .app import lbHelper
from .app.shared import checkDictionary


bp = Blueprint("solver", __name__, url_prefix="/solver")


def getTodaysLetters():
    todaysLetters = (
        get_db().execute("SELECT letters" " FROM bees" " ORDER BY id DESC").fetchone()
    )
    return json.loads(todaysLetters["letters"])


def getDict():
    file_path = os.path.join(current_app.root_path, "app/shared", "words_alpha.txt")
    with open(file_path) as word_file:
        lines = word_file.readlines()
    return lines


@bp.route("/spellingbee", methods=("GET", "POST"))
def spellingbee():
    todaysLetters = getTodaysLetters()

    if todaysLetters is None:
        fillLetters = "abcdefg"
    else:
        fillLetters = todaysLetters

    error = None

    if request.method == "POST":

        requiredLetter = request.form["required"]
        letters = (
            request.form["firstl"]
            + request.form["secondl"]
            + request.form["thirdl"]
            + request.form["fourthl"]
            + request.form["fifthl"]
            + request.form["sixthl"]
        )
        repeatChar = False
        requiredLetter = requiredLetter.lower()
        letters = letters.lower()
        letters = sorted(letters)
        letters.insert(0, requiredLetter)
        letters = "".join(letters)

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

    if (len(letters) != 7) or (not letters.isalpha()):
        return redirect(url_for("solver.spellingbee"))
    db = get_db()
    dbLetters = db.execute(
        "SELECT accepted, pangrams" " FROM bees" " WHERE letters = ?", (letters,)
    ).fetchone()

    if dbLetters is None:
        checker = checkDictionary.dictionaryChecker(letters,getDict())
        checker.findPangrams(letters, checker.answer)
        answer = checker.answer
        pangrams = checker.pangrams
        rejected = ""
        fromDB = False
    else:
        answer = json.loads(dbLetters["accepted"])
        pangrams = json.loads(dbLetters["pangrams"])
        rejected = json.loads(dbLetters["rejected"])
        fromDB = True

    answerTitle = "Answers"
    pangramTitle = "Pangrams"

    if len(answer) < 1:
        answer.append("No suitable words found.")
    elif len(answer) == 1:
        answerTitle = "Answer"

    length = ((len(answer) / 5) * 20) + 200

    if length < 500:
        length = 500

    if len(pangrams) < 1:
        pangrams.append("No panagrams can be made with the provided letters.")
    elif len(pangrams) == 1:
        pangramTitle = "Pangram"

    return render_template(
        "solver/answer.html",
        answer=answer,
        pangrams=pangrams,
        rejected=rejected,
        fromDB=fromDB,
        pangramTitle=pangramTitle,
        answerTitle=answerTitle,
        length=length,
    )


@bp.route("/letter_box", methods=("GET", "POST"))
def letterBox():
    error = None
    oneWord = None
    twoWord = None
    sides = None
    length = 0
    db = get_db()
    lbData = db.execute(
        "SELECT one_word, two_word, sides" " FROM boxes" " ORDER BY id DESC"
    ).fetchone()

    if lbData is not None:
        oneWord = json.loads(lbData["one_word"])
        twoWord = json.loads(lbData["two_word"])
        sides = json.loads(lbData["sides"])

    if twoWord:
        length = 400 + (25 * (len(twoWord) / 2))

    if length < 1000:
        length = 1000
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
    db = get_db()
    lbData = db.execute(
        "SELECT dictionary" " FROM boxes" " ORDER BY id DESC"
    ).fetchone()
    answerList = lbHelper.helper(json.loads(lbData["dictionary"]), remaining, starter)
    return render_template("solver/letter_box_help.html", answerList=answerList)
