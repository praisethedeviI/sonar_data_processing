from PIL import Image
import numpy as np

CONST_BRIGHT = 3


def mid_element(data: list[list[float]]):
    mid_elem = 0
    for i in range(len(data)):
        for j in range(len(data[0])):
            mid_elem += data[i][j]
    mid_elem /= len(data) * len(data[0])
    print('mid element: ' + str(mid_elem))
    return mid_elem


def draw(filename: str,
         data: list[list[float]],
         rgb: tuple[float] = (1, 1, 1)):
    image_data = np.zeros((len(data), len(data[0]), 3), dtype=np.uint8)

    mid_elem = mid_element(data)

    for i, row in enumerate(data):
        for j, elem in enumerate(row):
            tmp = 255 * elem / mid_elem / CONST_BRIGHT
            tmp = 255 if tmp > 255 else tmp
            image_data[i][j] = [tmp * rgb[0], tmp * rgb[1], tmp * rgb[2]]

    img = Image.fromarray(image_data)
    img.save(filename)
    img.show()


def get_data(filename: str, start: int, end: int):
    data = []
    with open(filename, 'r') as file:
        for pos, line in enumerate(file):
            if start <= pos <= end:
                data.append(list(map(float, line.split())))
    return data


def get_mid_line(data: list[list[float]]):
    mid_line = np.zeros(len(data[0]), dtype=np.float32)

    for row in data:
        for j, elem in enumerate(row):
            mid_line[j] += elem

    for i in range(len(mid_line)):
        mid_line[i] /= float(len(data))
    return mid_line


def data_filter(data_: list[list[float]]):
    data = data_.copy()

    mid_line = get_mid_line(data)
    signal_adjustment = (lambda e, m: 0 if m == 0 else e / m)

    for i in range(len(data)):
        for j in range(len(data[0])):
            data[i][j] = signal_adjustment(data_[i][j], mid_line[j])
    return data


def main():
    filename = input('Create name for new image: ') + '.png'
    start, end = list(
        map(int, input('Start and end of lines(min 1, max 7340): ').split()))
    start -= 1
    end -= 1
    rgb = tuple([float(elem) for elem in input('Input color(rgb) ratio from 0 '
                                               'to 1(example: "0 0.5 1") '
                                               '----> ').split()])

    data = get_data('data.txt', start, end)
    data = data_filter(data)
    draw(filename, data, rgb)


if __name__ == '__main__':
    main()
