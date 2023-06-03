from flask import Flask, request, send_from_directory
import os
import shutil
import random
import json
import speech_score as ss
import quiz
import quiz2

location = os.getcwd()
audio_dir = "audios"
audio_folder_path = os.path.join(location, audio_dir)

wav_dir = "wav_file"
wav_folder_path = os.path.join(location, wav_dir)

AUDIO_UPLOAD_FOLDER = audio_folder_path
ALLOWED_EXTENSIONS = {'aac'}

app = Flask(__name__)
app.config['AUDIO_UPLOAD_FOLDER'] = AUDIO_UPLOAD_FOLDER

# Set the path to your JSON key file
key_file_path = os.path.join(location, "academic-timing-383003-bc950b6b4496.json")

# Set the environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_file_path

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Index
@app.route("/")
def index():
    return "Pronounciation Analyse API Test OKAY!!"

# Pronouciation Score
@app.route("/pronouciation_score",methods=['POST','GET'])
def pronouciation_analyse():
    data = ""
    json_data = ""
    if(request.method == 'POST'):
        try:
            isExistinput = os.path.exists(audio_folder_path)
            if(isExistinput == True):
                shutil.rmtree(audio_folder_path)
                os.mkdir(audio_folder_path)
            elif(isExistinput == False):
                os.mkdir(audio_folder_path)

            isExistinput = os.path.exists(wav_folder_path)
            if(isExistinput == True):
                shutil.rmtree(wav_folder_path)
                os.mkdir(wav_folder_path)
            elif(isExistinput == False):
                os.mkdir(wav_folder_path)

            audio = request.files['audio']
            actual_text = request.form['text']

            if audio and allowed_file(audio.filename):
                analysis_audio = os.path.join(app.config['AUDIO_UPLOAD_FOLDER'], "analysis_audio.aac")
                audio.save(analysis_audio)

            wav_audio = ss.convert(analysis_audio, wav_folder_path)
            transcribe = ss.transcribe_speech(wav_audio)
            input_ref = ss.phoneme(actual_text)
            input_hyp = ss.phoneme(transcribe)
            output, compares = ss.wer(input_ref,input_hyp,debug=True)

            print('-'* 30)
            print(f"REF: {actual_text}\n")
            print(f"HYP: {transcribe}")
            print('-'* 30)
            print(f"REF-PHONEME: {input_ref}\n")
            print(f"HYP-PHONEME: {input_hyp}")
            print('-'* 30)
            print()
            print("N CORRECT   :", output['Cor'])
            print("N DELETE    :", output['Del'])
            print("N SUBSTITUTE:", output['Sub'])
            print("N INSERT    :", output['Ins'])
            print("WER: ", output['WER'])
            cwr = (1 - output['WER'])

            pronouciation_score = ss.pronoun_score(transcribe,cwr)
            json_d = {"status":"success", "analysis_audio" : analysis_audio, "wav_audio" : wav_audio, "actual_text" : actual_text, "transcribe" : transcribe, 'pronouciation_score' : pronouciation_score}
            json_data=json.dumps(json_d, ensure_ascii=False).encode('utf8')
            print("json_data",json_data)
            return json_data
        except Exception as e:
            json_d = {"status":"failed","error":str(e)}
            json_data=json.dumps(json_d)
            return json_data
        
#For Word Review1 
@app.route("/word_quiz1",methods=['POST','GET'])
def word_quiz1():
    word = ""
    json_data = ""
    if(request.method == 'POST'):
        word=request.form['word']
        word_definition = quiz.meaning(word)
        word1 = quiz.generate_option1()
        while word == word1:
            word1 = quiz.generate_option1()
        option1 = quiz.word_def1(word1)
        word2 = quiz.generate_option2()
        while word == word2 and word1 == word2:
            word2 = quiz.generate_option2()
        option2 = quiz.word_def2(word2)
        correct_answer = quiz.word_quiz(word, word_definition, option1, option2)
        json_d = {"word" : word, "option1" : word_definition, "option2" : option1, "option3" : option2, "correct_answer" : correct_answer}
        json_data=json.dumps(json_d)
        print("json_data",json_data)
    return json_data

# For Word Review2 
@app.route("/word_quiz2",methods=['POST','GET'])
def word_quiz2():
    word = ""
    json_data = ""
    if request.method == 'POST':
        word = request.form['word']
        lang = request.form['lang']
        eng_trans = quiz2.translator(word,lang)
        option1 = quiz2.generate_option1()
        while eng_trans == option1:
            option1 = quiz2.generate_option1()
        option2 = quiz2.generate_option2()
        while eng_trans == option2 and option1 == option2 :
            option2 = quiz2.generate_option2()
        correct_answer = quiz2.word_quiz(word, eng_trans, option1, option2)
        json_d = {
            "word": word,
            "option1": eng_trans,
            "option2": option1,
            "option3": option2,
            "correct_answer": correct_answer
        }
        json_data=json.dumps(json_d, ensure_ascii=False).encode('utf8')
    return json_data

# For Sentence Review 
@app.route("/sentence_review",methods=['POST','GET'])
def sentence_review():
    input_sentence = ""
    json_data = ""
    if request.method == 'POST':
        input_sentence = request.form['input_sentence']
        words = input_sentence.split()
        random.shuffle(words)
        jumble_output = ' '.join(words)
        json_d = {
            "input_sentence": input_sentence,
            "jumble_output": jumble_output
            }
        json_data=json.dumps(json_d)
    return json_data

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
