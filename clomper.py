import math


def load_curve(c):
    hz = c.lstrip('GraphicEQ: ').split(';')
    hz = [(float(x.strip().split(' ')[0]), float(x.strip().split(' ')[1])) for x in hz]
    return hz


def wavelet_special_points():
    return [20, 21, 22, 23, 24, 26, 27, 29, 30, 32, 34, 36, 38, 40, 43, 45, 48, 50, 53, 56, 59, 63, 66, 70, 74, 78, 83, 87, 92, 97, 103, 109, 115, 121, 128, 136, 143, 151, 160, 169, 178, 188, 199, 210, 222, 235, 248, 262, 277, 292, 309, 326, 345, 364, 385, 406, 429, 453, 479, 506, 534, 565, 596, 630, 665, 703, 743, 784, 829, 875, 924, 977, 1032, 1090, 1151, 1216, 1284, 1357, 1433, 1514, 1599, 1689, 1784, 1885, 1991, 2103, 2221, 2347, 2479, 2618, 2766, 2921, 3086, 3260, 3443, 3637, 3842, 4058, 4287, 4528, 4783, 5052, 5337, 5637, 5955, 6290, 6644, 7018, 7414, 7831, 8272, 8738, 9230, 9749, 10298, 10878, 11490, 12137, 12821, 13543, 14305, 15110, 15961, 16860, 17809, 18812, 19871]


def interpolate_curve(curve, target_frequencies): # tnx DeepSeek
    frequencies = [x[0] for x in curve]
    gains = [x[1] for x in curve]
    interpolated_gains = []
    for target_freq in target_frequencies:
        if target_freq <= frequencies[0]:
            interpolated_gains.append(gains[0])
        elif target_freq >= frequencies[-1]:
            interpolated_gains.append(gains[-1])
        else:
            for i in range(len(frequencies) - 1):
                if frequencies[i] <= target_freq <= frequencies[i + 1]:
                    x0, x1 = math.log(frequencies[i]), math.log(frequencies[i + 1])
                    y0, y1 = gains[i], gains[i + 1]
                    interpolated_gain = y0 + (y1 - y0) * (math.log(target_freq) - x0) / (x1 - x0)
                    interpolated_gains.append(interpolated_gain)
                    break
    return interpolated_gains


if __name__ == '__main__':
    sp = wavelet_special_points()
    curves = input('Enter your curves, use /// as a delimiter: ').split('///')
    curves = [load_curve(c) for c in curves]
    interpolated_curves = [interpolate_curve(c, sp) for c in curves]
    final_curve = [sum([interpolated_curves[i][u] for i in range(len(interpolated_curves))]) for u in range(len(interpolated_curves[0]))]
    ra = 6.0 - max(final_curve)
    final_curve = [x + ra for x in final_curve]

    assert len(final_curve) == len(sp)
    eq_points = []
    for i in range(len(sp)):
        eq_points.append(f"{sp[i]} {final_curve[i]:.1f}")
    print("GraphicEQ: " + "; ".join(eq_points))
    print("This aint' perfect, but your ears aren't likely to notice any differences")
