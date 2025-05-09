import math

def generate_wave_fdf(size, filename):
    with open(filename, 'w') as f:
        for y in range(size):
            row = []
            for x in range(size):
                # Высота как комбинация синусов
                z = int(10 * math.sin(x * 0.5) * math.cos(y * 0.5))
                row.append(z)
            f.write(' '.join(map(str, row)) + '\n')

generate_wave_fdf(20, 'wave.fdf')