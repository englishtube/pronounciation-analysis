import os
import nltk
from nltk.corpus import wordnet
import random
import re


def meaning(word):
  synset_array = wordnet.synsets(word)
  meaning_raw = synset_array[1].definition()
  meaning = re.sub(r'[?|$|.|!|)|(|;|_]', r'', meaning_raw)
  return meaning
  
def generate_option1():
  verb_synsets = list(wordnet.all_synsets(pos='v'))
  verb_lemmas = [lemma for synset in verb_synsets for lemma in synset.lemmas()]
  verb_names = [lemma.name() for lemma in verb_lemmas]
  option1 = random.choice(verb_names).replace('_',' ')
  return option1

def word_def1(option1):
  try:
    synset_array = wordnet.synsets(option1)
    meaning_raw = synset_array[0].definition()
    meaning = re.sub(r'[?|$|.|!|)|(|;|_]', r'', meaning_raw)
    return meaning
  except Exception as e:
    option1 = generate_option1()
    meaning = word_def1(option1)
    return meaning

def generate_option2():
  verb_synsets = list(wordnet.all_synsets(pos='v'))
  verb_lemmas = [lemma for synset in verb_synsets for lemma in synset.lemmas()]
  verb_names = [lemma.name() for lemma in verb_lemmas]
  option2 = random.choice(verb_names).replace('_',' ')
  return option2

def word_def2(option2):
  try:
    synset_array = wordnet.synsets(option2)
    meaning_raw = synset_array[0].definition()
    meaning = re.sub(r'[?|$|.|!|)|(|;|_]', r'', meaning_raw)
    return meaning
  except Exception as e:
    option2 = generate_option2()
    meaning = word_def2(option2)
    return meaning
  
def word_quiz(word, meaning, option1, option2):
    QUESTIONS = {
        word: [
            meaning, option1, option2
        ]
    }

    for question, alternatives in QUESTIONS.items():
        correct_answer = alternatives[0]
        sorted_alternatives = sorted(alternatives)
        # for label, alternative in enumerate(sorted_alternatives):
            # print(f"  {label}) {alternative}")
    return correct_answer
