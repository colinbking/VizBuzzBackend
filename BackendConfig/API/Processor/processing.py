import matplotlib.pyplot as plt
import numpy as np
import torchcrepe
from scipy import stats, signal
import math
import torch
import wave

frame_from_ns = lambda x: int((((x * 10**-4) / 1000) * 16000))

def add_pitch_to_output(transcription_filename:str = "data.json", filename = "out_wavs/The_smoking_tire_daniel_osborne.wav", cut = None, plot = False):

    with open(transcription_filename, 'r') as fp:
        output_format = json.load(fp)

    rigged_format = wave.open(filename)
    rigged_format.rewind()

    running_frame_count = 0
    last_o_d = 0
    avgs = []

    med_output = output_format[1:cut]

    if plot:
        rownum = int(((cut-2) / 4) + 1)
        pitchfig, axs = plt.subplots(rownum, 4, figsize = (20, rownum * 5))
        pitchfig.subplots_adjust(hspace=0.4, wspace = 0.3)

    for idx, tes in enumerate(med_output):

        throwaway = rigged_format.readframes(frame_from_ns(tes['Offset'] - last_o_d))
        
        # if idx > 0:
        #     noise_output = wave.open(f'out_wavs/tst{idx}word.wav', 'w')
        #     noise_output.setparams((1, 2, 16000, 4824898, 'NONE', 'not compressed'))
        
        frame_count = frame_from_ns (tes['Duration'])
        frames_to_process = rigged_format.readframes(frame_count)

        frames = np.frombuffer(frames_to_process, np.int16)

        # plt.plot(frames)
        # plt.title(f"word: {tes['display']}")
        # plt.show()
        # plt.plot(frames_to_process)

        avgi = np.average(stats.tmean(np.abs(frames), (0, 2000)))
        avgs.append(avgi)

        # if idx > 0:
        #     noise_output.writeframes(frames_to_process)
        #     noise_output.close()

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



        med_output[idx]['Pitch'] = 1 if max(np_downsampled_pitch) - min(np_downsampled_pitch) > 40 else 0 #extroidinarily robust
        med_output[idx]['Volume'] = avgi

        if plot:
            l1 = axs[x, y].plot(np_downsampled_pitch, c = 'b', label = f"Downsampled Pitch, len {len(np_downsampled_pitch)}")
            ax2 = axs[x, y].twiny()
            # axs[x, y].scatter(np_downsampled_pitch, c = 'b')
            l2 = ax2.plot(np_pitch, c = 'red', label = f"Pitch, len {len(np_pitch)}")
            axs[x, y].set_title(f"\"{tes['Display']}\"",  fontsize=20)
            lns = l1 + l2
            labs = [l.get_label() for l in lns]
            axs[x, y].legend(lns, labs, loc=0)
            axs[x, y].set_xlabel("Duration (ms)")
            axs[x, y].set_ylabel("Pitch (Hz)")
        

        running_frame_count += 1
        last_o_d = tes['Duration'] + tes['Offset']

    plt.savefig("test.png", facecolor='w')
    plt.show()
    plt.close()
    maxvol = max(avgs)
    minvol = min(avgs)

    for m in med_output: #forced run-through tro normalize volume
        m['Volume'] = (m['Volume'] - minvol) / (maxvol - minvol)
    

    if plot:
        fig = plt.figure(figsize=(6,6))
        plt.plot(avgs)
        plt.title("volume per word")
        for idx, mo in enumerate(med_output):
            plt.text(idx, avgs[idx], med_output[idx]['Display'])
        plt.show()
        # plt.savefig("test.png")
        # plt.close()

    return med_output