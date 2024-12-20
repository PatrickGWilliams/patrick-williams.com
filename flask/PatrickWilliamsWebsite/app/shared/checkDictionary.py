class dictionaryChecker:
    def __init__(self, letters, lines):
        self.pangrams = []
        self.answer = []
        requiredLetter = letters[0]
        for word in lines:
            word = word.rstrip().lower()
            if len(word) > 3 and (requiredLetter in word):
                fits = True
                for char in word:
                    if char not in letters:
                        fits = False
                        break
                if fits:
                    self.answer.append(word)

    def findPangrams(self, letters, words):
        for word in words:
            pangram = True
            for letter in letters:
                if letter not in word:
                    pangram = False
                    break
            if pangram:
                self.pangrams.append(word)
                self.answer.remove(word)
