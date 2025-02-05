import math


def load_curve(c):
    hz = c.lstrip('GraphicEQ: ').split(';')
    hz = [(float(x.strip().split(' ')[0]), float(x.strip().split(' ')[1])) for x in hz]
    return hz


def wavelet_special_points():
    hz = open('wavelet_flat.txt', 'r').read().lstrip('GraphicEQ: ').split(';')
    hz = [int(x.strip().split(' ')[0]) for x in hz]
    return hz


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
    final_curve = [sum([interpolated_curves[i][u] for i in range(len(curves))]) for u in range(len(curves[0]))]
    ra = 6.0 - max(final_curve)
    final_curve = [x + ra for x in final_curve]

    eq_points = []
    for i in range(len(sp)):
        eq_points.append(f"{sp[i]} {final_curve[i]:.1f}")
    print("GraphicEQ: " + "; ".join(eq_points))
    print("This aint' perfect, but your ears aren't likely to notice any difference")
