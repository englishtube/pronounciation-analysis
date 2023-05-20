import os
import nltk
from nltk.corpus import wordnet as wn

def meaning(word):
  synset_array = wn.synsets(word)
  meaning = synset_array[0].definition()
  return meaning

def definitions(word):
  synset_array = wn.synsets(word)
  sameaning = synset_array[0].definition()
  return sameaning

def synonym(word):

    synonyms = []

    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())

    syno = list(synonyms)[1]
    return syno

      
def antonym(word):

    antonyms = []

    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            if lemma.antonyms():
                antonyms.append(lemma.antonyms()[0].name())

    anto = list(antonyms)[0]

    return anto

def word_quiz(word, meaning, option1, option2):
    QUESTIONS = {
        word: [
            meaning, option1, option2
        ]
    }

    for question, alternatives in QUESTIONS.items():
        correct_answer = alternatives[0]
        sorted_alternatives = sorted(alternatives)
    return correct_answer
