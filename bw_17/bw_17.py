def normalize(numbers):
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = value / total * 100
        result.append(percent)
    return result


visits = [15, 35, 80]
percentages_1 = normalize(visits)
print('example 1')
print(percentages_1)


def read_visits(data_path):
    with open(data_path) as f:
        for line in f:
            yield int(line)


def normalize_copy(iterator_obj):
    numbers = list(iterator_obj)
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result


path = './my_numbers.txt'
it = read_visits(path)
percentages_2 = normalize_copy(it)
print('example 2')
print(percentages_2)


def normalize_func(get_iter):
    total = sum(get_iter())
    result = []
    for value in get_iter():
        percent = 100 * value / total
        result.append(percent)
    return result


percentages_3 = normalize_func(lambda: read_visits(path))
print('example 3')
print(percentages_3)


class ReadVisit(object):
    def __init__(self, data_path):
        self.data_path = data_path

    def __iter__(self):
        with open(self.data_path) as f:
            for line in f:
                yield int(line)


visits = ReadVisit('./my_numbers.txt')


print()
