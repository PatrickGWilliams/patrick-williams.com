def helper(dictionary, missingLetters, startingLetter):
    return sorted(
        [word for word in dictionary if word[0] is startingLetter],
        key=lambda word: sum(1 for character in missingLetters if character in word),
        reverse=True
    )
