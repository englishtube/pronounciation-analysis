from flask import Flask, request, send_from_directory
import os
import shutil
import json
import speech_score as ss
import quiz
import quiz2

location = os.getcwd()
audio_dir = "audios"
audio_folder_path = os.path.join(location, audio_dir)

AUDIO_UPLOAD_FOLDER = audio_folder_path
ALLOWED_EXTENSIONS = {'wav'}

app = Flask(__name__)
app.config['AUDIO_UPLOAD_FOLDER'] = AUDIO_UPLOAD_FOLDER

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

            audio = request.files['audio']
            actual_text = request.form['text']

            if audio and allowed_file(audio.filename):
                analysis_audio = os.path.join(app.config['AUDIO_UPLOAD_FOLDER'], "analysis_audio.wav")
                audio.save(analysis_audio)

            transcribe = ss.speechrecg(analysis_audio)
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
            json_d = {"status":"success", "analysis_audio" : analysis_audio, "actual_text" : actual_text, "transcribe" : transcribe, 'pronouciation_score' : pronouciation_score}
            json_data=json.dumps(json_d, ensure_ascii=False).encode('utf8')
            print("json_data",json_data)
            return json_data
        except Exception as e:
            json_d = {"status":"failed","error":str(e)}
            json_data=json.dumps(json_d)
            return json_data
        
# Download wav file
@app.route('/download/analysis_audio')
def downloadaudio():
  audio_filename = "analysis_audio.wav"
  path = os.path.join(audio_folder_path, audio_filename)
  if os.path.isfile(path):
    return send_from_directory(audio_folder_path, audio_filename)
  return "No file found"

#For Word Review1 
@app.route("/word_quiz1",methods=['POST','GET'])
def word_quiz1():
    word = ""
    json_data = ""
    if(request.method == 'POST'):
        word=request.form['word']
        word_definition = quiz.meaning(word)
        syno = quiz.synonym(word)
        anto = quiz.antonym(word)
        option1 = quiz.definitions(syno)
        option2 = quiz.definitions(anto)
        correct_answer = quiz.word_quiz(word, word_definition, option1, option2)
        json_d = {"word" : word, "option1" : word_definition, "option2" : option1, "option3" : option2, "correct_answer" : correct_answer}
        json_data=json.dumps(json_d)
        print("json_data",json_data)
    return json_data

# For Word Review2 
@app.route("/word_quiz2",methods=['POST','GET'])
def word_quiz2():
    chainese_word = ""
    japanese_word = ""
    korean_word = ""
    json_data = ""
    if request.method == 'POST':
        if 'chainese_word' in request.form:
            chainese_word = request.form['chainese_word']
            eng_trans = quiz2.translatorch(chainese_word)
            option1 = quiz2.synonym(eng_trans)
            option2 = quiz2.antonym(eng_trans)
            correct_answer = quiz2.word_quizch(chainese_word, eng_trans, option1, option2)
            json_d = {
                "chainese_word": chainese_word,
                "option1": eng_trans,
                "option2": option1,
                "option3": option2,
                "correct_answer": correct_answer
            }
            json_data=json.dumps(json_d, ensure_ascii=False).encode('utf8')
            return json_data
        if 'japanese_word' in request.form:
            japanese_word = request.form['japanese_word']
            eng_trans = quiz2.translatorja(japanese_word)
            option1 = quiz2.synonym(eng_trans)
            option2 = quiz2.antonym(eng_trans)
            correct_answer = quiz2.word_quizja(japanese_word, eng_trans, option1, option2)
            json_d = {
                "japanese_word": japanese_word,
                "option1": eng_trans,
                "option2": option1,
                "option3": option2,
                "correct_answer": correct_answer
            }
            json_data=json.dumps(json_d, ensure_ascii=False).encode('utf8')
            return json_data
        if 'korean_word' in request.form:
            korean_word = request.form['korean_word']
            eng_trans = quiz2.translatorko(korean_word)
            option1 = quiz2.synonym(eng_trans)
            option2 = quiz2.antonym(eng_trans)
            correct_answer = quiz2.word_quizko(korean_word, eng_trans, option1, option2)
            json_d = {
                "korean_word": korean_word,
                "option1": eng_trans,
                "option2": option1,
                "option3": option2,
                "correct_answer": correct_answer
            }
            json_data=json.dumps(json_d, ensure_ascii=False).encode('utf8')
            return json_data

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
