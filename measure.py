import numpy as np
import sounddevice as sd
from scipy.signal import stft

VOLUME = 0.8
DURATION = 0.75


def wavelet_special_points():
    hz = open('wavelet_flat.txt', 'r').read().lstrip('GraphicEQ: ').split(';')
    hz = [int(x.strip().split(' ')[0]) for x in hz]
    return hz


def generate_sine_wave(freq, sample_rate=44100):
    t = np.linspace(0, DURATION, int(sample_rate * DURATION), endpoint=False)
    wave = np.cos(2 * np.pi * freq * t) * VOLUME
    return wave


def analyze_frequency(signal, sample_rate, target_freq):
    signal = signal[int(0.1*len(signal)):int(0.9*len(signal))]
    f, t, Zxx = stft(signal, fs=sample_rate, nperseg=4096)
    freq_index = np.argmin(np.abs(f - target_freq))
    magnitude = np.abs(Zxx[freq_index, :]).mean()
    return magnitude


def measure_headphone(name, frequencies, sample_rate):
    print(f"\n=== Measuring {name} headphone ===")
    input(f"Connect the {name} headphone and press Enter to start...")

    results = {}
    for freq in frequencies:
        sine_wave = generate_sine_wave(freq, sample_rate=sample_rate)
        recording = sd.playrec(sine_wave, samplerate=sample_rate, channels=1, dtype='float32')
        sd.wait()
        magnitude = analyze_frequency(recording[:, 0], sample_rate, freq)
        results[freq] = magnitude
        print(f"Measured {freq:5} Hz: {magnitude:.6f}")
    return results


def generate_eq_profile(reference, replica, frequencies):
    def diff(ref, rep):
        with np.errstate(divide='ignore'):
            return 10 * np.log10(ref / rep)

    eq_points = []

    mxx = 0.0

    for freq in frequencies:
        ref = reference.get(freq, 1e-9)
        rep = replica.get(freq, 1e-9)
        mxx = max(mxx, diff(ref, rep))

    dff = max(0.0, mxx - 6.0)

    for freq in frequencies:
        ref = reference.get(freq, 1e-9)
        rep = replica.get(freq, 1e-9)
        gain_db = diff(ref, rep) - dff
        eq_points.append(f"{freq} {gain_db:.1f}")
    return "GraphicEQ: " + "; ".join(eq_points)


def load_measurements(filename):
    d = {}
    with open(filename, 'r') as f:
        t = f.read().replace('Measured', '').replace('Hz', '').split('\n')
        for x in t:
            d[int(x.split(':')[0])] = float(x.split(':')[1])
        return d


if __name__ == '__main__':
    frequencies = wavelet_special_points()
    print(
        generate_eq_profile(load_measurements('measurements/reference'), load_measurements('measurements/replica'),
                        frequencies)
    )
    exit()

    sample_rate = 44100

    reference_results = measure_headphone("REFERENCE", frequencies, sample_rate)
    replica_results = measure_headphone("REPLICA", frequencies, sample_rate)

    eq_profile = generate_eq_profile(reference_results, replica_results, frequencies)
    with open("wavelet_correction.txt", "w") as f:
        f.write(eq_profile)

    print("\nWavelet correction profile generated successfully!")
    print("Saved as 'wavelet_correction.txt'")