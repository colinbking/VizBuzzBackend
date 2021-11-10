import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv
import time
import json
from functools import reduce
import boto3
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
import azure.cognitiveservices.speech as speechsdk
import pyAudioAnalysis.audioBasicIO as aio
import shutil
import wave
import matplotlib.pyplot as plt
import numpy as np
import torchcrepe
from scipy import stats, signal
import math
import torch

load_dotenv()

compresslambda = lambda x: [j for i in x for j in i]
addlambda = lambda x: reduce(lambda a,b: a + " " + b, x)
frame_from_ns = lambda x: int((((x * 10**-4) / 1000) * 16000))

def add_key(d, k, v, i):
    if (k == "Offset" or k == "Duration"):
        d[k] = v * 1e-4
    else:
        d[k] = v
    d['index'] = i
    return d

def truncate_utf8_chars(filename, count, ignore_newlines=True):
    """
    Truncates last `count` characters of a text file encoded in UTF-8.
    :param filename: The path to the text file to read
    :param count: Number of UTF-8 characters to remove from the end of the file
    :param ignore_newlines: Set to true, if the newline character at the end of the file should be ignored
    """
    with open(filename, 'rb+') as f:
        last_char = None

        size = os.fstat(f.fileno()).st_size

        offset = 1
        chars = 0
        while offset <= size:
            f.seek(-offset, os.SEEK_END)
            b = ord(f.read(1))

            if ignore_newlines:
                if b == 0x0D or b == 0x0A:
                    offset += 1
                    continue

            if b & 0b10000000 == 0 or b & 0b11000000 == 0b11000000:
                # This is the first byte of a UTF8 character
                chars += 1
                if chars == count:
                    # When `count` number of characters have been found, move current position back
                    # with one byte (to include the byte just checked) and truncate the file
                    f.seek(-1, os.SEEK_CUR)
                    f.truncate()
                    return
            offset += 1

class Transcriber():
    # given a s3 bucket and a key to a specific file, transcribes it and drops it to a
    # our transcript s3 bucket.

    def __init__(self):
        print("connecting to s3 using boto3")
        self.s3 = boto3.client('s3')


    def transcribe(self, bucket, key):


        print("transcribing audio file with key: ", key)
        s3 = boto3.client('s3')
        s3.Bucket("vizbuzz-podcast-audio-files").download_file(key, "wavs/temp.wav")
        vzsr = vz_speech_recog()
        vzsr.convert_folder('wavs', 'out_wavs');
        vzsr.speech_recognize_continuous_from_file("out_wavs/temp.wav");
        s3.upload_file('new_data.json', env("TRANSCRIPT_BUCKET_NAME"), key + '.json')
        return True

class vz_speech_recog:
    def __init__(self, filename = "out_wavs/test.wav"):
        self.best_lexs = []
        self.jrds = []

        if os.path.exists("data.json"):
            os.remove("data.json")

        self.start_stream(filename)
        # self.os = []

    def start_stream(self, filename):
        self.rigged_format = wave.open(filename)
        self.rigged_format.rewind()
        self.last_o_d_global = 0
        

    def convert_folder(self, input_folder_path, output_folder_path):

        o = aio.convert_dir_fs_wav_to_wav(input_folder_path, 16000, 1)
        if os.path.exists(output_folder_path):
            shutil.rmtree(output_folder_path)
        # print(os.path.exists(f"{input_folder_path}/Fs16000_NC1/"))
        # print(os.path.exists(output_folder_path))
        os.rename(f"{input_folder_path}/Fs16000_NC1/", output_folder_path)
        # shutil.rmtree(f"{input_folder_path}/Fs16000_NC1/")

        # rename input_folder_path + os.sep + "Fs" + str(16000) +  "_" + "NC" + str(1) to 

    def speech_recognition_with_push_stream(self, filename):

        with open('data.json', 'a') as fp:
            fp.write("[ {\"Word\": \"VZBHEADERPLZIGNORE\"} [")

        # Specify the path to an audio file containing speech (mono WAV / PCM with a sampling rate of 16kHz).

        """gives an example how to use a push audio stream to recognize speech from a custom audio
        source"""
        speech_config = speechsdk.SpeechConfig(subscription=os.getenv('SPEECHKEY'), region="eastus")
        speech_config.request_word_level_timestamps()

        # setup the audio stream
        stream = speechsdk.audio.PushAudioInputStream()
        audio_config = speechsdk.audio.AudioConfig(stream=stream)

        # instantiate the speech recognizer with push stream input
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        # Connect callbacks to the events fired by the speech recognizer
        speech_recognizer.recognized.connect(lambda evt: self.save_transcript(evt))
        speech_recognizer.session_stopped.connect(lambda evt: self.end_transcript(evt))
        speech_recognizer.canceled.connect(lambda evt: self.end_transcript(evt))
        # speech_recognizer.recognizing.connect(lambda evt: self.save_partial_transcript(evt))

        # The number of bytes to push per buffer
        n_bytes = 3200
        wav_fh = wave.open(filename)

        # start continuous speech recognition
        speech_recognizer.start_continuous_recognition()

        # start pushing data until all data has been read from the file
        try:
            while(True):
                frames = wav_fh.readframes(n_bytes // 2)
                # print('read {} bytes'.format(len(frames)))
                if not frames:
                    break

                stream.write(frames)
                time.sleep(.1)
        finally:
            # stop recognition and clean up
            wav_fh.close()
            stream.close()
            speech_recognizer.stop_continuous_recognition()
       

    def speech_recognize_continuous_from_file(self, filename):

        # with open('data.json', 'a') as fp:
        #     fp.write("[")

        """performs continuous speech recognition with input from an audio file"""

        speech_config = speechsdk.SpeechConfig(subscription=os.getenv('SPEECHKEY'), region="eastus")
        speech_config.request_word_level_timestamps()

        # <SpeechContinuousRecognitionWithFile>
        audio_config = speechsdk.audio.AudioConfig(filename=filename)

        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        done = False

        def stop_cb(evt):
            """callback that signals to stop continuous recognition upon receiving an event `evt`"""
#             print('CLOSING on {}'.format(evt))
            nonlocal done
            done = True

        # Connect callbacks to the events fired by the speech recognizer
    #     speech_recognizer.recognizing.connect(lambda evt: test_print(evt))
        speech_recognizer.recognized.connect(lambda evt: self.save_transcript(evt))
#         speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
#         speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
#         speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
#         stop continuous recognition on either session stopped or canceled events
        speech_recognizer.session_stopped.connect(stop_cb)
        speech_recognizer.canceled.connect(stop_cb)

        # Start continuous speech recognition
        speech_recognizer.start_continuous_recognition()
        while not done:
            time.sleep(.5)

        speech_recognizer.stop_continuous_recognition()

        # with open('data.json', 'a') as fp:
        #     fp.write("[]]")

        return speech_recognizer
        # </SpeechContinuousRecognitionWithFile>

    def end_transcript(self, istr):
        print("ending transcipt - SESSION STOPPED OR CANCELLED")
        # truncate_utf8_chars('data.json', 1)

        # with open('data.json', 'a') as fp:
        #     fp.write("]")

    def save_transcript(self, istr):
        print("saving transcipt")

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

        o = self.create_output()

        # no = add_pitch_to_output(self, o, cut = None)

        # truncate_utf8_chars('data.json', 1) #remove the ending ]

        # # try:
        # #     print(json.dumps(no))
        # # except Exception as e:
        # #     print(e)


        # with open('data.json', 'a') as fp:
        #     fp.write(",") #add the comma before the next list conent

        #     # print(json.dumps(no).strip('[').strip(']'))

        #     fp.write(json.dumps(no).strip('[').strip(']')) #add the list content

        #     fp.write("]") #end the list

            

        self.jrds = []
        self.best_lexs = []
        self.add_pitch_to_file(o)

    def add_pitch_to_file(self, o):
        no = self.add_pitch_to_output(o)

        truncate_utf8_chars('data.json', 1) #remove the ending ]

        with open('data.json', 'a') as fp:
            fp.write(",") #add the comma before the next list conent

            # print(json.dumps(no).strip('[').strip(']'))

            fp.write(json.dumps(no).strip('[').strip(']')) #add the list content

            fp.write("]") #end the list

            

        self.jrds = []
        self.best_lexs = []

    def create_output(self):
        # assert(len(lex_words) == len(words_and_offsets))
        words_and_offsets = compresslambda([self.best_lexs[i]['Words'] for i in range(len(self.best_lexs))])
        lex_words = addlambda([self.best_lexs[i]['Lexical'] for i in range(len(self.best_lexs))]).split(" ")
        self.lex_final = lex_words
        z = list(zip(words_and_offsets, lex_words))
        mid_output = [add_key(z[zi][0], "display", z[zi][1], zi) for zi in range(len(z))]

        final_chuncks = [{"Words": [], "start_index": 0}]
        curr_index = 0
        seen_words = set()
        for i, w in enumerate(self.lex_final[:240]):
            if w in seen_words:
                curr_index += 1
                final_chuncks.append({"Words": [w], "start_index": i})
                seen_words = set()
            else:
                seen_words.add(w)
                final_chuncks[curr_index]['Words'].append(w)

        for lineiq in final_chuncks:
            sentiq = reduce(lambda a,b: a + " " + b, lineiq['Words'])
            nlp = spacy.load('en_core_web_sm')
            nlp.add_pipe("spacytextblob")
            doc = nlp(sentiq)
            # print(sentiq, doc._.polarity, doc._.subjectivity)
            for phraseassign in doc._.assessments:
                # print(phraseassign)
                for wordassign in phraseassign[0]:
                    idx = lineiq['Words'].index(wordassign) + lineiq['start_index']
                    # print(wordassign, phraseassign[1], idx)
                    mid_output[idx]['Polarity'] = phraseassign[1]
                    mid_output[idx]['Subjective'] = phraseassign[2]

        return mid_output


    def add_pitch_to_output(self, output_format:dict, cut = None, plot = False):

        # print("got here")

        running_frame_count = 0
        avgs = []

        med_output = output_format[:cut]

        if plot:
            rownum = int(((cut - 1) / 4) + 1)
            pitchfig, axs = plt.subplots(rownum, 4, figsize = (20, rownum * 5))

        for idx, tes in enumerate(med_output):

            # print(f"removed {frame_from_ns(tes['Offset'])} frames")
            # print(f"removed {self.last_o_d_global} frames")
            _ = self.rigged_format.readframes(frame_from_ns(tes['Offset'] - self.last_o_d_global))
            
            if idx > 800:
                noise_output = wave.open(f'out_wavs/tst{idx}word.wav', 'w')
                noise_output.setparams((1, 2, 16000, 4824898, 'NONE', 'not compressed'))
            
            frame_count = frame_from_ns (tes['Duration'])
            frames_to_process = self.rigged_format.readframes(frame_count)
            # print(f"init silence {frame_from_ns(tes['Offset'] - self.last_o_d_global)} frames, {tes['display']} is {frame_count} frames, got {len(frames_to_process)} frames")
            frames = np.frombuffer(frames_to_process, np.int16)
            avgi = np.average(stats.tmean(np.abs(frames), (0, 500)))
            avgs.append(avgi)

            if idx > 800:
                noise_output.writeframes(frames_to_process)
                noise_output.close()

            frames = frames.astype(np.float32) / np.iinfo(np.int16).max
            audioload = torch.tensor(np.copy(frames))[None]

            # Compute pitch using first gpu
            pitch = torchcrepe.predict(audioload,
                                    16000,
                                    int(16000 / 200.),
                                    fmin=50,
                                    fmax=550,
                                    model='tiny',
                                    batch_size=2048)
            np_pitch = pitch.numpy()[0]
            # print(f'input number {idx}, len of pitch {len(np_pitch)}')
            # np_downsampled_pitch = signal.decimate(np_pitch, 6, axis = 0, zero_phase=True if len(np_pitch) > 27 else False)
            # np_downsampled_pitch = signal.decimate(np_pitch, 10, axis = 0, ftype="fir" if len(np_pitch) < 27 else "iir")
            np_downsampled_pitch = signal.decimate(np_pitch, 10, axis = 0, n = 1 if len(np_pitch) <= 27 else 8)

            x = math.floor(running_frame_count / 4)
            y = running_frame_count % 4

            med_output[idx]['pitch_vals'] = list(np_downsampled_pitch)

            if plot:
                axs[x, y].plot(np_downsampled_pitch, c = 'b')
                ax2 = axs[x, y].twiny()
                # axs[x, y].scatter(np_downsampled_pitch, c = 'b')
                ax2.plot(np_pitch, c = 'red')
                axs[x, y].set_title(f"word: {tes['display']}, number of points: {len(np_pitch)} -> {len(np_downsampled_pitch)}")
                # axs[x, y].set_ylims(250)
            

            running_frame_count += 1
            self.last_o_d_global = tes['Duration'] + tes['Offset']
        if plot:
            plt.savefig("test.png", facecolor='w')
            plt.close()
        # plt.show()

        return med_output
