from PIL import Image
from math import log, exp

LEFT = 85
TOP = 56
WIDTH = 1258
HEIGHT = 617

FREQ_BORDERS = [((261, 200), (1253, 700)),((161, 500), (1226, 1750)),((329, 2000), (1240, 6000)),((291, 5000), (1256, 20000))]  # Pos, hz
AMP_BORDERS = [((169, -30), (577, -60)),((169, -30), (577, -60)),((169, -30), (577, -60)),((212, -30), (621, -60))]
RED = (196, 10, 52)

if __name__ == '__main__':
    eq_vals = {}  # rounded to hz, 0.1db
    # Process Spectroid (Android app) screenshots
    # We get plenty o' accuracy, we are bottlenecked by having only one pass
    # (speedrun quality project!) and how bad phone mic is
    # (probably not horribly bad - my ears kinda agreed with the dips that Spectroid showed)
    for pi in range(4):
        freq_span = FREQ_BORDERS[pi][1][0] - FREQ_BORDERS[pi][0][0]
        freq_log_dist = log(FREQ_BORDERS[pi][1][1]) - log(FREQ_BORDERS[pi][0][1])
        freq_log_density = freq_log_dist / freq_span
        freq_log_anchor = log(FREQ_BORDERS[pi][0][1]) - FREQ_BORDERS[pi][0][0] * freq_log_density

        amp_span = AMP_BORDERS[pi][1][0] - AMP_BORDERS[pi][0][0]
        amp_dist = AMP_BORDERS[pi][1][1] - AMP_BORDERS[pi][0][1]
        amp_density = amp_dist / amp_span
        amp_anchor = AMP_BORDERS[pi][0][1] - AMP_BORDERS[pi][0][0] * amp_density

        img = Image.open(f'eqsrc/{pi}.png')
        for i in range(img.size[0]):  # width
            for u in range(img.size[1]):  # height
                if img.getpixel((i, u)) == RED:
                    px_hz = amp_density * u + amp_anchor
                    px_freq_log = freq_log_density * i + freq_log_anchor
                    px_freq = exp(px_freq_log)
                    eq_vals[int(px_freq)] = int(px_hz * 10)

    offset = -38.2
    wetness = 0.8
    clipping = 6.0
    low_cutoff = 295  # Did I tell you just *how* trash the speaker is?
    high_cutoff = 17000  # I don't hear anything above this lol. Not a big deal honestly.

    vals = list(eq_vals.items())
    vals = [(x, y) for x, y in vals if low_cutoff <= x <= high_cutoff]
    vals = [(x, min(clipping, -wetness * (y / 10) + offset)) for x, y in vals]

    print(sum([y > clipping - 0.1 for x, y in vals]), len(vals))
    print(min([x[1] for x in vals]))

    # AutoEQ
    vals = [(20, vals[0][1])] + vals + [(20000, vals[-1][1])]
    t = [20, 21, 22, 23, 24, 26, 27, 29, 30, 32, 34, 36, 38, 40, 43, 45, 48, 50, 53, 56, 59, 63, 66, 70, 74, 78, 83, 87, 92, 97, 103, 109, 115, 121, 128, 136, 143, 151, 160, 169, 178, 188, 199, 210, 222, 235, 248, 262, 277, 292, 309, 326, 345, 364, 385, 406, 429, 453, 479, 506, 534, 565, 596, 630, 665, 703, 743, 784, 829, 875, 924, 977, 1032, 1090, 1151, 1216, 1284, 1357, 1433, 1514, 1599, 1689, 1784, 1885, 1991, 2103, 2221, 2347, 2479, 2618, 2766, 2921, 3086, 3260, 3443, 3637, 3842, 4058, 4287, 4528, 4783, 5052, 5337, 5637, 5955, 6290, 6644, 7018, 7414, 7831, 8272, 8738, 9230, 9749, 10298, 10878, 11490, 12137, 12821, 13543, 14305, 15110, 15961, 16860, 17809, 18812, 19871]
    autoeq_vals = []
    for i in range(len(vals) - 1):
        while len(autoeq_vals) < len(t) and vals[i][0] <= t[len(autoeq_vals)] <= vals[i + 1][0]:
            a = (t[len(autoeq_vals)] - vals[i][0]) / (vals[i + 1][0] - vals[i][0])
            b = a * vals[i + 1][1] + (1 - a) * vals[i][1]
            autoeq_vals += [(t[len(autoeq_vals)], b)]
    export = '; '.join([f'{x} {y:.1f}' for x, y in autoeq_vals])
    open('one_euro_speaker_autoeq.txt', 'w').write(export)  # AKA handmade Friendship is Magic speaker

    # Equalizer APO
    vals = vals[:len(vals)+2:3]  # Otherwise Equalizer APO dies, RIP ;(
    export = f"GraphicEQ: " + '; '.join([f"{x} {y:.1f}" for x, y in vals])
    open('one_euro_speaker_apo.txt', 'w').write(export)
