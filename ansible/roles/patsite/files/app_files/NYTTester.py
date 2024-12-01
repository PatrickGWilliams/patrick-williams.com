import time
import json
import sqlite3
import logging

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    ElementNotInteractableException as noninteractable,
)
from selenium.common.exceptions import NoSuchElementException as noElement
from selenium.common.exceptions import TimeoutException as timeOut
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import checkDictionary


logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="/home/ansible/app_files/wordChecker/NYTTester.log", level=logging.INFO
)


class MyWebDriver:

    def __init__(self):
        logger.info("starting driver")
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_page_load_timeout(120)
        self.driver.set_script_timeout(120)
        self.hiveLetters = []
        self.soup = []

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

    def getInitialValues(self):

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


class State:

    def __init__(self):
        self.answer = []
        self.acceptedWords = []
        self.rejectedWords = []
        self.sortedLetters = []
        self.attempts = 0
        self.web: MyWebDriver
        self.initializeDriver()

    def checkWords(self):
        for word in self.answer:
            logger.info("checking ")
            logger.info(word)
            atLimit = False

            try:
                self.web.clickLetters(self, word)
                logger.info("At limit")
                time.sleep(1)
            except noninteractable:

                atLimit = True
            except timeOut:
                atLimit = True

            if atLimit:
                self.closeDriver()
                self.initializeDriver()
                time.sleep(2)
                self.web.clickLetters(self, word)
                time.sleep(1)
        self.sortLetters()
        self.closeDriver()

    def closeDriver(self):
            logger.info("closing driver")
            try:
                self.web.driver.close()
                logger.info("dirver successfully closed")
            except timeOut:
                logger.info("Timeout Exception Occured")
                self.web.driver.quit()
                logger.info("dirver quit")


    def sortLetters(self):
        letters = self.web.hiveLetters
        required = letters.pop(0)
        letters.sort()
        letters.insert(0, required)
        stringLetters = "".join(letters)
        self.sortedLetters = stringLetters

    def getWebsite(self):
        getAttempts = 0
        for getAttempts in range(5):
            try:
                logger.info("getting nyt.com")
                self.web.driver.get("https://www.nytimes.com/puzzles/spelling-bee")
                getAttempts = 0
                break
            except timeOut:
                logger.info("nyt.com timed out. attempts: ", getAttempts + 1)
                raise timeOut
        if getAttempts >= 4:
            raise timeOut("failed to load page") 

    def initializeDriver(self):
        fullAttempts = 0

        for fullAttempts in range(5):
            self.web = MyWebDriver()
            try:
                self.getWebsite()
                fullAttempts=0
                break
            except timeOut:
                self.closeDriver()

        if fullAttempts >=4:
            raise Exception("failed to load spelling bee page many times")

        self.web.getInitialValues()




def findAcceptedWords():
    state = State()
    checker = checkDictionary.dictionaryChecker(state.web.hiveLetters)
    if checker.answer is not None:
        state.answer = checker.answer
        logger.info("found words: ")
        logger.info(state.answer)
        state.checkWords()
    checker.findPangrams(state.sortedLetters, state.acceptedWords)
    if checker.pangrams is not None:
        for word in checker.pangrams:
            state.acceptedWords.remove(word)
    logger.info("Accepted Words: ")
    logger.info(state.acceptedWords)
    logger.info("rejected words: ")
    logger.info(state.rejectedWords)
    logger.info("pangrams: ")
    logger.info(checker.pangrams)
    logger.info("letters: ")
    logger.info(state.sortedLetters)

    db = sqlite3.connect(
        "/home/ansible/app_files/shared_files/spellingBeeDB.sqlite",
        detect_types=sqlite3.PARSE_DECLTYPES,
    )
    db.execute("DELETE FROM bees" " WHERE letters=?", (state.sortedLetters,))
    db.execute(
        "INSERT INTO bees (letters, accepted, pangrams, rejected)"
        " VALUES (?, ?, ?, ?)",
        (
            state.sortedLetters,
            json.dumps(state.acceptedWords),
            json.dumps(checker.pangrams),
            json.dumps(state.rejectedWords),
        ),
    )
    db.commit()
    db.close()


if __name__ == "__main__":
    logger.info("Starting the script")
    try:
        findAcceptedWords()
    except Exception as e:
        logger.error("Something went wrong: ", exc_info=True)
    logger.info("Finished the script")
