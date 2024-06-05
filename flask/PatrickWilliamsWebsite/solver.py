import json

from flask import (Blueprint, flash, json, redirect, render_template, request,
                   url_for)
from PatrickWilliamsWebsite.db import get_db

from . import checkDictionary



bp = Blueprint("solver", __name__, url_prefix="/solver")


def getTodaysLetters():
    todaysLetters = (
        get_db()
        .execute("SELECT letters" " FROM bees" " ORDER BY id DESC")
        .fetchone()
    )
    return todaysLetters


@bp.route("/spellingbee", methods=("GET", "POST"))
def spellingbee():
    todaysLetters = getTodaysLetters()
    
    if todaysLetters is None:
        fillLetters="abcdefg"
    else:
        fillLetters=todaysLetters["letters"]

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
            return redirect(url_for("solver.answer", letters=letters))

        flash(error)

    return render_template(
        "solver/spellingbee.html", fillLetters=fillLetters
    )


@bp.route("/answer/<letters>", methods=("GET", "POST"))
def answer(letters):
    answer = []
    pangrams = []
    rejected = []
    fromDB = False

    if (len(letters) != 7) or (not letters.isalpha()):
        return redirect(url_for("solver.spellingbee"))
    db = get_db()
    dbLetters = db.execute(
        "SELECT accepted, pangrams, rejected"
        " FROM bees"
        " WHERE letters = ?",
        (letters,)
    ).fetchone()



    if dbLetters is None:
        checker = checkDictionary.dictionaryChecker(letters)
        checker.findPangrams(letters,checker.answer)
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
    lengthLongest=len(rejected)
    if len(answer)>lengthLongest:
        lengthLongest = len(answer)
    
    length = ((lengthLongest / 5) * 20) + 500
    
    if length < 1000:
        length = 1000

    if len(pangrams) < 1:
        pangrams.append("No panagrams can be made with the provided letters.")
    elif len(pangrams) == 1:
        pangramTitle = "Pangram"

    

    return render_template(
        "solver/answer.html", answer=answer, pangrams=pangrams, rejected=rejected, fromDB=fromDB, pangramTitle=pangramTitle, answerTitle=answerTitle, length=length
    )
