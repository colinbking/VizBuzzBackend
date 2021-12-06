import matplotlib.pyplot as plt
import numpy as np
import torchcrepe
from scipy import stats, signal
import math
import torch
import wave
import json


def frame_from_ns(x):
    return int((((x * 10**-4) / 1000) * 16000))


def add_pitch_to_output(output_format_name: str = "data.json",
                        filename="out_wavs/The_smoking_tire_daniel_osborne.wav", cut=5, plot=False):

    with open(output_format_name, "r") as fp:
        output_format = json.load(fp)

    rigged_format = wave.open(filename)
    rigged_format.rewind()

    running_frame_count = 0
    last_o_d = 0
    avgs = []

    med_output = output_format[1:cut]

    if plot:
        rownum = int(((cut - 1) / 4) + 1)
        pitchfig, axs = plt.subplots(rownum, 4, figsize=(20, rownum * 5))

    for idx, tes in enumerate(med_output):

        throwaway = rigged_format.readframes(frame_from_ns(tes['Offset'] - last_o_d))  # noqa: F841

        #  if idx > 0:
        #     noise_output = wave.open(f'out_wavs/tst{idx}word.wav', 'w')
        #     noise_output.setparams((1, 2, 16000, 4824898, 'NONE', 'not compressed'))

        frame_count = frame_from_ns(tes['Duration'])
        frames_to_process = rigged_format.readframes(frame_count)

        frames = np.frombuffer(frames_to_process, np.int16)
        avgi = np.average(stats.tmean(np.abs(frames), (0, 500)))
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
        # np_downsampled_pitch = signal.decimate(np_pitch, 6, axis = 0, zero_phase=True if len(np_pitch) > 27 else False
        # np_downsampled_pitch = signal.decimate(np_pitch, 10, axis = 0, ftype="fir" if len(np_pitch) < 27 else "iir")
        np_downsampled_pitch = signal.decimate(np_pitch, 10, axis=0, n=1 if len(np_pitch) < 27 else 8)

        x = math.floor(running_frame_count / 4)
        y = running_frame_count % 4

        med_output[idx]['pitch_vals'] = np_downsampled_pitch

        if plot:
            axs[x, y].plot(np_downsampled_pitch, c='b')
            ax2 = axs[x, y].twiny()
            # axs[x, y].scatter(np_downsampled_pitch, c = 'b')
            ax2.plot(np_pitch, c='red')
            title = f"word: {tes['display']}, number of points: {len(np_pitch)} -> {len(np_downsampled_pitch)}"
            axs[x, y].set_title(title)
            # axs[x, y].set_ylims(250)

        running_frame_count += 1
        last_o_d = tes['Duration'] + tes['Offset']
    if plot:
        plt.savefig("test.png", facecolor='w')
        plt.close()
    # plt.show()

    return med_output

    # fig = plt.figure(figsize=(6,6))
    # plt.plot(avgs)
    # plt.title("volume per word")
    # for idx, mo in enumerate(med_output):å
    #     plt.text(idx, avgs[idx], med_output[idx]['display'])
    # plt.savefig("test.png")
    # plt.close()
