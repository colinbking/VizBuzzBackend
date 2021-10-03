import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv
import time
import json
from functools import reduce
import wave
import audioop

compresslambda = lambda x: [j for i in x for j in i]
addlambda = lambda x: reduce(lambda a,b: a + " " + b, x)

def add_key(d, k, v):
    d[k] = v
    return d

class Transcriber():
    # given a s3 bucket and a key to a specific file, transcribes it and drops it to a
    # our transcript s3 bucket.
    def transcribe(self, bucket, key):
        print("transcribing audio file with key: ", key)
        vzsr = vz_speech_recog()
        sr = vzsr.speech_recognize_continuous_from_file("The_smoking_tire_daniel_osborne.wav")
        output_format = vzsr.create_output()
        ## what do i do now with this output format?
        return True

class vz_speech_recog:
    def __init__(self):
        self.best_lexs = []
        self.jrds = []
       

    def speech_recognize_continuous_from_file(self, filename):
        """performs continuous speech recognition with input from an audio file"""

        speech_config = speechsdk.SpeechConfig(subscription=os.getenv('SPEECHKEY'), region="eastus")
        speech_config.request_word_level_timestamps()

        # <SpeechContinuousRecognitionWithFile>
        stream = speechsdk.audio.PushAudioInputStream()
        audio_config = speechsdk.audio.AudioConfig(stream=stream)
        # audio_config = speechsdk.audio.AudioConfig(filename=filename)

        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        done = False

        def stop_cb(evt):
            """callback that signals to stop continuous recognition upon receiving an event `evt`"""
#             print('CLOSING on {}'.format(evt))
            nonlocal done
            done = True

        speech_recognizer.recognized.connect(lambda evt: self.save_transcript(evt))
        speech_recognizer.session_stopped.connect(stop_cb)
        speech_recognizer.canceled.connect(stop_cb)

        n_bytes = 3200
        wav_fh = wave.open(filename) # filename can be a file-like object, which is what we will retrieve from AWS
        
        print(wav_fh.getnchannels(), 1)
        print(wav_fh.getsampwidth(), 2)
        print(wav_fh.getframerate(), 16000)
        print(wav_fh.getcomptype(), "NONE")
        
        if(wav_fh.getnchannels() != 1) or (wav_fh.getframerate() != 16000):
            res, loc = downsampleWav(filename, filename[:-4] + "resampled.wav", inrate=wav_fh.getframerate(), outrate=16000, inchannels=wav_fh.getnchannels(), outchannels=1)
            if res:
                wav_fh.close()
                wav_fh = wave.open(loc)
            else:
                print("something broke!!")
        
        print(wav_fh.getnchannels(), 1)
        print(wav_fh.getsampwidth(), 2)
        print(wav_fh.getframerate(), 16000)
        print(wav_fh.getcomptype(), "NONE")
        # Start continuous speech recognition
        # speech_recognizer.start_continuous_recognition()
        # try:
        #     while(True):
        #         frames = wav_fh.readframes(n_bytes // 2)
        #         # print('read {} bytes'.format(len(frames)))
        #         if not frames:
        #             break

        #         stream.write(frames)
        #         time.sleep(.1)
        # finally:
        #     # stop recognition and clean up
        #     wav_fh.close()
        #     stream.close()
        #     speech_recognizer.stop_continuous_recognition()
        # </SpeechContinuousRecognitionWithFile>

    def save_transcript(self, istr):

#         try:
#             text_file = open("sample.txt", "a")
#             n = text_file.write(istr.result + "\n")
#             text_file.close()
#         except:
#             print('error saving')

#         print("-------------------")
        jr = istr.result.properties[speechsdk.PropertyId.SpeechServiceResponse_JsonResult]
        jrd = json.loads(jr)
#         print("_________")
        curmax = {}
        curmaxcond = 0
        for jrdi in jrd['NBest']:
    #         print(jrdi['Confidence'], curmaxcond)
            if jrdi['Confidence'] > curmaxcond:
                curmaxcond = jrdi['Confidence']
                curmax = jrdi
                
#         print(curmax)
        self.jrds.append(jrd)
        self.best_lexs.append(curmax)

    def create_output(self):
        # assert(len(lex_words) == len(words_and_offsets))
        words_and_offsets = compresslambda([self.best_lexs[i]['Words'] for i in range(len(self.best_lexs))])
        lex_words = addlambda([self.best_lexs[i]['Lexical'] for i in range(len(self.best_lexs))]).split(" ")
        return [add_key(d, "display", l) for d, l in zip(words_and_offsets, lex_words)]


def downsampleWav(src, dst, inrate=44100, outrate=16000, inchannels=2, outchannels=1):
    print("-------------", inrate, outrate, inchannels, outchannels)
    if not os.path.exists(src):
        print ('Source not found!')
        return False, ""

    print(dst)
    dst_dir = os.path.dirname(__file__) + "/resampled_files/"
    print(dst_dir)


    try:
        s_read = wave.open(src, 'r')
        s_write = wave.open(dst_dir + dst, 'w')
    except:
        print ('Failed to open files!')
        return False, ""

    n_frames = s_read.getnframes()
    data = s_read.readframes(n_frames)

    try:
        converted = audioop.ratecv(data, 2, inchannels, inrate, outrate, None)
        if outchannels == 1:
            if inchannels != 1:
                converted = audioop.tomono(converted[0], 2, 1, 0)
    except:
        print ('Failed to downsample wav')
        return False, ""

    try:
        s_write.setparams((outchannels, 2, outrate, 0, 'NONE', 'Uncompressed'))
        print('got to setparams')
        s_write.writeframes(converted)
        return True, dst_dir + dst
    except Exception as e:
        print(e)
        print ('Failed to write wav')
        return False, ""