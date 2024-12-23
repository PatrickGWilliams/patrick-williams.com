import urllib.request
import json
import re
import sqlite3



def getGameData() -> None:

    db = sqlite3.connect(
        "/home/ansible/app_files/shared_dir/app.db",
        detect_types=sqlite3.PARSE_DECLTYPES,
    )

    page = urllib.request.urlopen("https://www.nytimes.com/puzzles/spelling-bee")

    beeRegEx: re.Match[str] | None = re.search(
        r"window\.gameData\s*=\s*\{\"today\":(\{.*?\})", str(page.read())
    )

    if beeRegEx:
        beeJson = json.loads(beeRegEx.group(1))
        for word in beeJson["pangrams"]:
            beeJson["answers"].remove(word)
        letters = ''.join(beeJson["validLetters"])

        db.execute(
            "INSERT INTO bees (letters, accepted, pangrams)"
            " VALUES (?, ?, ?)",
            (
                letters,
                json.dumps(beeJson["answers"]),
                json.dumps(beeJson["pangrams"])
            ),
        )

        db.commit()

    page = urllib.request.urlopen("https://www.nytimes.com/puzzles/letter-boxed")

    letterBoxRegEx: re.Match[str] | None = re.search(
        r"window\.gameData\s*=\s*(\{.*?\})", str(page.read())
    )

    if letterBoxRegEx:
        boxJson = json.loads(letterBoxRegEx.group(1))
        solutions = findSolutions(
            boxJson["dictionary"], makeSideString(boxJson["sides"])
        )
        db.execute(
           "INSERT INTO boxes (sides, one_word, two_word, dictionary)"
           " VALUES (?, ?, ?, ?)",
           (
               json.dumps(boxJson["sides"]),
               json.dumps(solutions["oneWord"]),
               json.dumps(solutions["twoWord"]),
               json.dumps(boxJson["dictionary"])
           ),
        )

        db.commit()

    db.close()


def makeSideString(sides) -> str:
    combinedList = ""
    for side in sides:
        for letter in side:
            combinedList += letter
    return combinedList


def findSolutions(dictionary, combinedList) -> dict:
    solutions = {"oneWord": [], "twoWord": []}
    missingLetterDict = {}
    for word in dictionary:
        missingLetters = """"""
        flag = True
        for letter in combinedList:
            if letter not in word:
                missingLetters += letter
        if missingLetters == """""":
            solutions["oneWord"].append(word)
        else:
            for testWord in missingLetterDict:
                if (testWord not in solutions["oneWord"]) and (
                    (word[-1] == testWord[0]) or (testWord[-1] == word[0])
                ):
                    for letter in missingLetters:
                        flag = True
                        if letter in missingLetterDict[testWord]:
                            flag = False
                            break
                    if flag:
                        if word[-1] == testWord[0]:
                            solutions["twoWord"].append([word, testWord])
                        else:
                            solutions["twoWord"].append([testWord, word])
        missingLetterDict.update({word: missingLetters})
    return solutions


if __name__ == "__main__":
    getGameData()
