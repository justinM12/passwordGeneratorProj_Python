
#PasswordGenerator

""" This is a multiline doc comment

-- link to word list: https://github.com/dwyl/english-words
-- link to word list discussion: https://stackoverflow.com/questions/2213607/how-to-get-english-language-word-database
-- verb list gotten from https://7esl.com/english-verbs/

Operation:
- takes in a sentence or a list of words and then randomly puts them in a random order.
- then the program will randomly add a random word to the phrase in a random position
- then program will insert a random number and a random special character at the end.

- or ask user for a noun and then the program picks a random verb and then a random word
 
Features to include:
- add special character option
- add number option
- add option for making first character of each word capitalize
- add option for making password a certian length
- add option for choosing where numbers and special characters will be placed
- random word is selected from a word database

Password Formats:
- UVU: [user selected noun/word][randomly chosen verb][user selected noun/verb]
- randomly combine [user selected word/s][randomly chosen word]
"""

import json
import random
from abc import ABC, abstractmethod

#setupStart
def getWordListFromTextFile():
    with open('words_alpha.txt', 'r') as wordFile:
        return wordFile.read().split()

def getRandomItemFromList(li):
    lengthOfList = len(li) - 1
    randomIndexInList = random.randint(0, lengthOfList)
    return li[randomIndexInList]

def getVerbListFromTextFile():
    with open('verbList.txt', 'r') as verbFile:
        verbFileData = verbFile.read()
        return verbFileData.split( )

def capitalizeFirstLetterOfWord(word):
    if word[0].isupper():
        return word
    else:
        return word[0].upper() + word[1:len(word)]

wordList = getWordListFromTextFile()
verbList = getVerbListFromTextFile()


class InFormalPasswordGeneratorInterface:
    def generatePassword(self):
        pass

class AbstractPasswordGenerator(ABC, InFormalPasswordGeneratorInterface):
    _passwordString = ""

    @abstractmethod
    def generatePassword(self):
        pass

    @abstractmethod
    def getPassword(self):
        return self._passwordString

class UVUPasswordGenerator(AbstractPasswordGenerator):
    """
        UVU is a password output format: U = user chosen noun/word, V = randomly generated verb
    """
    def generatePassword(self):
        firstWord = input("Enter a word to be used in the password:")
        secondWord = input("Enter another word to be used in the password:")

        firstWord = capitalizeFirstLetterOfWord(firstWord)
        secondWord = capitalizeFirstLetterOfWord(secondWord)
        verb = capitalizeFirstLetterOfWord(getRandomItemFromList(verbList))
        self._passwordString = firstWord + verb + secondWord
        return self._passwordString

    def getPassword(self):
        return super(UVUPasswordGenerator, self).getPassword()

class UserWordsAndOneRandomWordPasswordGenerator(AbstractPasswordGenerator):
    """
        Combines a list of user chosen words and a random word together in a random order
    """
    _firstWord = True
    _isUserDoneChoosingWords = False

    def _getUserWordsAndAddWordsToList(self, listWords):
        if self._firstWord == True:
            self._firstWord = False
            word = input("Enter a word to be used in the password:")
            word = capitalizeFirstLetterOfWord(word)
            listWords.append(word)
        else:
            word = input("Enter another word to be used in the password, or leave break and press enter to finish:")
            if word == "":
                self._isUserDoneChoosingWords = True
                #print(listWords)
                return
            else:
                word = capitalizeFirstLetterOfWord(word)
                listWords.append(word)

    def _getRandomWordAndCombineWithUserWordsInRandomOrder(self, listWords):
        randomWord = getRandomItemFromList(wordList)
        randomWord = capitalizeFirstLetterOfWord(randomWord)

        listWords.append(randomWord)
        resultString = ""
        #print(listWords)
        while len(listWords) > 0:
            selectedWord = getRandomItemFromList(listWords)
            resultString = resultString + selectedWord
            listWords.remove(selectedWord)
        return resultString

    def generatePassword(self):
        listOfUserWords = []
        while self._isUserDoneChoosingWords == False:
            self._getUserWordsAndAddWordsToList(listOfUserWords)
        self._passwordString = self._getRandomWordAndCombineWithUserWordsInRandomOrder(listOfUserWords)

    def getPassword(self):
        return super(UserWordsAndOneRandomWordPasswordGenerator, self).getPassword()

class AbstractPasswordGeneratorDecorator(ABC, InFormalPasswordGeneratorInterface):
    passwordGenerator = False
    _passwordString = ""
    def __init__(self, pGenerator):
        passwordGenerator = pGenerator

    @abstractmethod
    def generatePassword(self):
        self.passwordGenerator.generatePassword()

    @abstractmethod
    def getPassword(self):
        return self._passwordString

class RandomNumberAtEndPasswordDecorator(AbstractPasswordGeneratorDecorator):
    def __init__(self, pGenerator):
        super(pGenerator)

    def _addRandomNumberAtEndOfPassword(self, password):
        return password + random.randint(0, 9)

    def generatePassword(self):
        unModdedPass = self.passwordGenerator.generatePassword()
        self._passwordString = self._addRandomNumberAtEndOfPassword(unModdedPass)
        #possiblly remove
        return self._passwordString
#setupEnd

#start
class AppMain():
    _uvuPassGen = UVUPasswordGenerator()
    _userAndRandWordPassGen = UserWordsAndOneRandomWordPasswordGenerator()
    _passwordString = ""

    def run(self):
        #self._uvuPassGen.generatePassword()
        #self._passwordString = self.uvuPassGen.getPassword()

        self._userAndRandWordPassGen.generatePassword()
        self._passwordString = self._userAndRandWordPassGen.getPassword()
        print(self._passwordString)

appMain = AppMain()
appMain.run()


