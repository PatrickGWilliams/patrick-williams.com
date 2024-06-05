import time
import json
import sqlite3

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import \
    ElementNotInteractableException as noninteractable
from selenium.common.exceptions import NoSuchElementException as noElement
from selenium.common.exceptions import TimeoutException as timeOut
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import checkDictionary

class MyWebDriver:

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-extensions")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_page_load_timeout(60)
        self.driver.set_script_timeout(60)
        self.hiveLetters = []
        self.driver.get("https://www.nytimes.com/puzzles/spelling-bee")

        startButton = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div[3]/div[2]/div[2]/div[2]/section[2]/div/div/div/div[2]/div/button[1]",
                )
            )
        )
        startButton.click()
        self.soup = BeautifulSoup(self.driver.page_source, "html.parser")
        hiveElement = self.soup.find(class_="hive")
        self.enterButton = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "div.hive-action:nth-child(1)")
            )
        )
        for letter in hiveElement.contents:
            self.hiveLetters.append(letter.text)

    def clickLetters(self, state, word):
        flag = True
        for letter in word:
            letterIndex = self.hiveLetters.index(letter)
            cssSelector = "svg.hive-cell:nth-child(" + str(letterIndex + 1) + ")"
            letterElement = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, cssSelector))
            )
            letterElement.click()
        self.enterButton.click()

        try:
            self.driver.find_element(By.CLASS_NAME, "sb-message-points")
        except noElement:
            flag = False

        if flag:
            state.acceptedWords.append(word)
        else:
            state.rejectedWords.append(word)

    def getAcceptedWords(self, state):
        source = self.driver.page_source
        limitSoup = BeautifulSoup(source, "html.parser")
        wordList = limitSoup.find(class_="sb-wordlist-items-pag")
        for wordListContents in wordList.contents:
            if wordListContents.text not in state.acceptedWords:
                state.acceptedWords.append(wordListContents.text)


class State:

    def __init__(self):
        self.answer = []
        self.acceptedWords = []
        self.rejectedWords= []
        self.sortedLetters = []

    def checkWords(self, web):
        for word in self.answer:
            atLimit = False

            try:
                web.clickLetters(self, word)
                time.sleep(1)
            except noninteractable:

                atLimit = True
            except timeOut:
                atLimit = True

            if atLimit:
                web.driver.close()
                web = MyWebDriver()
                time.sleep(2)
                web.clickLetters(self, word)
                time.sleep(1)
        self.sortLetters(web.hiveLetters)
        web.driver.quit()

    def sortLetters(self, letters):
        required = letters.pop(0)
        letters.sort()
        letters.insert(0, required)
        stringLetters = "".join(letters)
        self.sortedLetters = stringLetters



def findAcceptedWords():
    web = MyWebDriver()
    state = State()
    checker = checkDictionary.dictionaryChecker(web.hiveLetters)
    if checker.answer is not None:
        state.answer = checker.answer
        print(state.answer)
        state.checkWords(web)
    checker.findPangrams(state.sortedLetters,state.acceptedWords)
    print(checker.pangrams)
    if checker.pangrams is not None:
        for word in checker.pangrams:
            state.acceptedWords.remove(word)
    print("final answer: ",state.acceptedWords)
    print("rejected: ",state.rejectedWords)
    print("pangrams: ",checker.pangrams)
            
    db = sqlite3.connect(
            "/home/pat/projects/patrick-williams/development/docker/shared_directory/spellingBeeDB.sqlite",
            detect_types=sqlite3.PARSE_DECLTYPES
        )
    db.execute(
        "DELETE FROM bees"
        " WHERE letters=?",
        (state.sortedLetters,)
    )
    db.execute(
        "INSERT INTO bees (letters, accepted, pangrams, rejected)"
        " VALUES (?, ?, ?, ?)",
        (state.sortedLetters, json.dumps(state.acceptedWords), json.dumps(checker.pangrams), json.dumps(state.rejectedWords))
    )
    db.commit()
    db.close()


if __name__ == "__main__":
    findAcceptedWords()
