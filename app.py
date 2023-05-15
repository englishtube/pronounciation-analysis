from flask import Flask, request, send_from_directory
import os
import shutil
import json
import speech_score as ss

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

@app.route('/download/analysis_audio')
def downloadaudio():
  audio_filename = "analysis_audio.wav"
  path = os.path.join(audio_folder_path, audio_filename)
  if os.path.isfile(path):
    return send_from_directory(audio_folder_path, audio_filename)
  return "No file found"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)