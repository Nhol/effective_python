def log(message, values):
    if not values:
        print(message)
    else:
        values_str = ','.join(str(x) for x in values)
        print('%s: %s' % (message, values_str))


print('example 1')
log('My Numbers are', [1, 2])
log('Hi there', []) # 로그로 남길 값이 없을 때 빈 리스트를 넘겨야 함. 불필요


def log(message, *values):
    if not values:
        print(message)
    else:
        values_str = ','.join(str(x) for x in values)
        print('%s: %s' % (message, values_str))


print('example 2')
log('My Numbers are', 1, 2)
log('Hi there')


print('example 3')
favorites = [7, 33, 99]
log('favorite colors', *favorites)


def my_generator():
    for i in range(10):
        yield i


def my_func(*args):
    print(args)


print('example 4')
it = my_generator()
my_func(*it)


def log(sequence, message, *values):
    if not values:
        print('%s: %s' % (sequence, message))
    else:
        values_str = ','.join(str(x) for x in values)
        print('%s: %s: %s' % (sequence, message, values_str))


print('example 5')
log(1, 'Favorites', 7, 33)
log('Favorite numbers', 7, 33) # 의도한 대로 동작하지 않음

print()
