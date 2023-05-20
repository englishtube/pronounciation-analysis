import os
import nltk
from nltk.corpus import wordnet as wn
import translators as ts
    
def translatorch(chinese_word):
    eng_trans = ts.translate_text(chinese_word, translator='google', from_language='zh-CN', to_language='en-US')
    return eng_trans
    
def translatorja(japanese_word):
    eng_trans = ts.translate_text(japanese_word, translator='google', from_language='ja', to_language='en-US')
    return eng_trans

def translatorko(korean_word):
    eng_trans = ts.translate_text(korean_word, translator='google', from_language='ko', to_language='en-US')
    return eng_trans

def synonym(eng_trans):

    synonyms = []

    for syn in wn.synsets(eng_trans):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())

   
    syno=[]
    [syno.append(x) for x in synonyms if x not in syno]
    
    option1 = syno[1]

    return option1

      
def antonym(eng_trans):

    antonyms = []

    for syn in wn.synsets(eng_trans):
        for lemma in syn.lemmas():
            if lemma.antonyms():
                antonyms.append(lemma.antonyms()[0].name())
    
    anto=[]
    [anto.append(x) for x in antonyms if x not in anto]
    
    option2 = anto[0]

    return option2
    

def word_quizch(chinese_word, eng_trans, option1, option2):
    QUESTIONS = {
        chinese_word: [
            eng_trans, option1, option2
        ]
    }

    for question, alternatives in QUESTIONS.items():
        correct_answer = alternatives[0]
        sorted_alternatives = sorted(alternatives)
    return correct_answer
    
def word_quizja(japanese_word, eng_trans, option1, option2):
    QUESTIONS = {
        japanese_word: [
            eng_trans, option1, option2
        ]
    }

    for question, alternatives in QUESTIONS.items():
        correct_answer = alternatives[0]
        sorted_alternatives = sorted(alternatives)
    return correct_answer

def word_quizko(korean_word, eng_trans, option1, option2):
    QUESTIONS = {
        korean_word: [
            eng_trans, option1, option2
        ]
    }

    for question, alternatives in QUESTIONS.items():
        correct_answer = alternatives[0]
        sorted_alternatives = sorted(alternatives)
    return correct_answer
