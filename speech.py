# this module is used for producing voice output from text

import pyttsx3
from time import sleep


class Speech:   
    def __init__(self, words_nouns):
        self.words_nouns = words_nouns


    # internal function
    # adds 'a' or 'an' to a word
    def add_article(self, word):                
        a = "a "
        an = "an "
        if word[0] in "aeiou":
            an +=  word
            return an
        return a + word


    # internal function
    # adds 'a' or 'an' to all words
    def add_all_articles(self):
        words_w_articles = []
        for word in self.words_nouns:
            words_w_articles.append(self.add_article(word))
        return words_w_articles


    # internal function
    # creates a sequence of words, e.g. "an apple, an orange and a computer"
    def create_sequence(self):
        if not self.words_nouns:
            return "nothing"
        sequence = ""
        words = self.add_all_articles()
        if len(self.words_nouns) > 1:
            for word in words:
                sequence += word + ", "
            sequence = sequence[:-2]
            sequence += " and " + words[-1]
        else:
            sequence += words[0]
        return sequence


    # creates a whole sentence
    def create_sentence(self, sentence_beginning):
        sentence_ending = self.create_sequence()
        return sentence_beginning + sentence_ending


    def speak(self, text, words_per_minute=130):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')          # getting details of current voice
        engine.setProperty('voice', voices[0].id)      # changing voices; 0 for male
        engine.setProperty('rate', words_per_minute)
        engine.say(text)
        engine.runAndWait()
        engine.stop()