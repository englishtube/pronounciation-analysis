import os
import nltk
from nltk.corpus import wordnet
import translators as ts
import random

def translator(word, lang):
    if lang == "zh":
        eng_trans = ts.translate_text(word, translator='google', from_language=lang, to_language='en-US')
        return eng_trans
    elif lang == "ja":
        eng_trans = ts.translate_text(word, translator='google', from_language=lang, to_language='en-US')
        return eng_trans
    elif lang == "ko":
        eng_trans = ts.translate_text(word, translator='google', from_language=lang, to_language='en-US')
        return eng_trans

def generate_option1():
  verb_synsets = list(wordnet.all_synsets(pos='v'))
  verb_lemmas = [lemma for synset in verb_synsets for lemma in synset.lemmas()]
  verb_names = [lemma.name() for lemma in verb_lemmas]
  option1 = random.choice(verb_names).replace('_',' ')
  return option1

def generate_option2():
  verb_synsets = list(wordnet.all_synsets(pos='v'))
  verb_lemmas = [lemma for synset in verb_synsets for lemma in synset.lemmas()]
  verb_names = [lemma.name() for lemma in verb_lemmas]
  option2 = random.choice(verb_names).replace('_',' ')
  return option2

def word_quiz(word, eng_trans, option1, option2):
    QUESTIONS = {
        word: [
            eng_trans, option1, option2
        ]
    }

    for question, alternatives in QUESTIONS.items():
        correct_answer = alternatives[0]
    return correct_answer
