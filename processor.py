import librosa
import soundfile as sf
import numpy
import math

# Failed, tried to use modulation to add BASS.
# Maybe some day...

if __name__ == '__main__':
    FILENAME = 'FiM - The Theme Song'
    NFFT = 1024
    SAMPLES_PER_FFT = NFFT // 4

    audio_path = f'audio_in/{FILENAME}.mp3'
    y, sr = librosa.load(audio_path, sr=None)
    D = librosa.stft(y, n_fft=NFFT)

    modulating = 1 + numpy.cos(numpy.arange(len(D[0])) * 400 * 2 * math.pi / SAMPLES_PER_FFT)
    #D[:25] *= 0
    #D[40:] *= 0
    D[3:10] *= modulating

    D_inv = librosa.istft(D, n_fft=NFFT)
    D_inv /= max(D_inv.max(), abs(D_inv.min()))
    sf.write(f'audio_out/{FILENAME}.wav', D_inv, sr)
