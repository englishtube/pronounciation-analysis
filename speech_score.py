import speech_recognition as sr
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import jiwer
from phonemizer.backend import EspeakBackend

# Speech Recognition
def speechrecg(analysis_audio):
    r = sr.Recognizer()
    # load speech file
    audio_file = sr.AudioFile(analysis_audio)

    # transcribe speech using Google Speech Recognition
    with audio_file as source:
        audio = r.record(source)

    # Recognize speech using Google Cloud Speech

    try:
        transcribe = r.recognize_google(audio, language="en")
        
    except sr.UnknownValueError:
        print("Sorry, I didn't understand what you said")
    except sr.RequestError as e:
        print("Could not request results from Google Cloud Speech service; {0}".format(e))
    return transcribe

# Get Phonemes
def phoneme(text):
    backend = EspeakBackend('en-us', preserve_punctuation=True, with_stress=True)
    word_list = text.lower()
    phonemes_list = []
    text = text.split()
    phonemized = backend.phonemize(text, strip=True)
    phonemes_list.extend(phonemized)
    return(phonemes_list)

# Word Error Rate
def wer(input_ref, input_hyp ,debug=False):
    remove_punctuation = False 

    if remove_punctuation == True:
        ref = jiwer.RemovePunctuation()(input_ref)
        hyp = jiwer.RemovePunctuation()(input_hyp)
    else:
        ref = input_ref
        hyp = input_hyp

    r = ref
    h = hyp
    #costs will holds the costs, like in the Levenshtein distance algorithm
    costs = [[0 for inner in range(len(h)+1)] for outer in range(len(r)+1)]
    # backtrace will hold the operations we've done.
    # so we could later backtrace, like the WER algorithm requires us to.
    backtrace = [[0 for inner in range(len(h)+1)] for outer in range(len(r)+1)]

    OP_OK = 0
    OP_SUB = 1
    OP_INS = 2
    OP_DEL = 3

    DEL_PENALTY=1 # Tact
    INS_PENALTY=1 # Tact
    SUB_PENALTY=1 # Tact
    # First column represents the case where we achieve zero
    # hypothesis words by deleting all reference words.
    for i in range(1, len(r)+1):
        costs[i][0] = DEL_PENALTY*i
        backtrace[i][0] = OP_DEL

    # First row represents the case where we achieve the hypothesis
    # by inserting all hypothesis words into a zero-length reference.
    for j in range(1, len(h) + 1):
        costs[0][j] = INS_PENALTY * j
        backtrace[0][j] = OP_INS

    # computation
    for i in range(1, len(r)+1):
        for j in range(1, len(h)+1):
            if r[i-1] == h[j-1]:
                costs[i][j] = costs[i-1][j-1]
                backtrace[i][j] = OP_OK
            else:
                substitutionCost = costs[i-1][j-1] + SUB_PENALTY # penalty is always 1
                insertionCost    = costs[i][j-1] + INS_PENALTY   # penalty is always 1
                deletionCost     = costs[i-1][j] + DEL_PENALTY   # penalty is always 1

                costs[i][j] = min(substitutionCost, insertionCost, deletionCost)
                if costs[i][j] == substitutionCost:
                    backtrace[i][j] = OP_SUB
                elif costs[i][j] == insertionCost:
                    backtrace[i][j] = OP_INS
                else:
                    backtrace[i][j] = OP_DEL

    # back trace though the best route:
    i = len(r)
    j = len(h)
    numSub = 0
    numDel = 0
    numIns = 0
    numCor = 0
    if debug:
        lines = []
        compares = []
    while i > 0 or j > 0:
        if backtrace[i][j] == OP_OK:
            numCor += 1
            i-=1
            j-=1
            if debug:
                lines.append("OK\t" + r[i]+"\t"+h[j])
                compares.append(h[j])
        elif backtrace[i][j] == OP_SUB:
            numSub +=1
            i-=1
            j-=1
            if debug:
                lines.append("SUB\t" + r[i]+"\t"+h[j])
                compares.append(h[j] +  r[i])
        elif backtrace[i][j] == OP_INS:
            numIns += 1
            j-=1
            if debug:
                lines.append("INS\t" + "****" + "\t" + h[j])
                compares.append(h[j])
        elif backtrace[i][j] == OP_DEL:
            numDel += 1
            i-=1
            if debug:
                lines.append("DEL\t" + r[i]+"\t"+"****")
                compares.append(r[i])
    if debug:
        compares = reversed(compares)
        for line in compares:
            print(line, end=" ")
        
    wer_result = round( (numSub + numDel + numIns) / (float) (len(r)), 3)
    return {'WER':wer_result, 'Cor':numCor, 'Sub':numSub, 'Ins':numIns, 'Del':numDel}, compares

# Sentiment Analysis score and pronounciation score
def pronoun_score(transcribe,cwr):
    sa_obj = SentimentIntensityAnalyzer() 
    polarity_dict = sa_obj.polarity_scores(transcribe) 

    print("Raw sentiment dictionary : ", polarity_dict) 
    print("polarity percentage of sentence ", polarity_dict['neg']*100, "% :: Negative") 
    print("polarity percentage of sentence ", polarity_dict['neu']*100, "% :: Neutral") 
    print("polarity percentage of sentence ", polarity_dict['pos']*100, "% :: Positive") 

    if polarity_dict['pos'] > polarity_dict['neg'] and polarity_dict['pos'] > polarity_dict['neu']:
      print("Positive : ", polarity_dict['pos'])
      pos = polarity_dict['pos']
      pronouciation_score = ((pos + cwr) / 2)
      print("Pronouciation Score: {0:.2f}".format(pronouciation_score))

    elif polarity_dict['neg'] > polarity_dict['pos'] and polarity_dict['neg'] > polarity_dict['neu']:
      print("Negative : ", polarity_dict['neg'])
      neg = polarity_dict['neg']
      pronouciation_score = ((neg + cwr) / 2)
      print("Pronouciation Score: {0:.2f}".format(pronouciation_score))
    else :
      print("Neutral : ", polarity_dict['neu'])
      neu = polarity_dict['neu']
      pronouciation_score = ((neu + cwr) / 2)
      print("Pronouciation Score: {0:.2f}".format(pronouciation_score))
    return pronouciation_score
