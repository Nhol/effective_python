from collections import defaultdict

# example 1: sort 메서드의 key hook로 lambda 함수 사
names = ['Socrates', 'Archimedes', 'Plato', 'Aristotle']
names.sort(key=lambda x: len(x))
print(names)


# example 2: defaultdict의 custom 사용
def log_missing():
    print('Key added')
    return 0


current = {'green': 12, 'blue': 3}
increments = [
    ('red', 5),
    ('blue', 17),
    ('orange', 9)
]
result_2 = defaultdict(log_missing, current)
print('Before:', dict(result_2))
for key, amount in increments:
    result_2[key] += amount
print('After: ', dict(result_2))


# example 3: 상태 보존 클로저를 defaultdict의 기본값 hook로 사용하는 헬퍼 함수
def increment_with_report(current, increments):
    added_count = 0

    def missing():
        nonlocal added_count # 상태보존 클로저
        added_count += 1
        return 0

    result = defaultdict(missing, current)
    for key, amount in increments:
        result[key] += amount

    return result, added_count


result_3 = increment_with_report(current, increments)


# example 4
class CountMissing(object):
    def __init__(self):
        self.added = 0

    def missing(self):
        self.added += 1
        return 0


counter = CountMissing()
result_4 = defaultdict(counter.missing, current)
for key, amount in increments:
    result_4[key] += amount
assert counter.added == 2


# example 5
class BetterCountMissing(object):
    def __init__(self):
        self.added = 0

    # __call__ 메서드를 정의하면 객체를 함수처럼 호출 가능
    def __call__(self):
        self.added += 1
        return 0


counter = BetterCountMissing()
counter()

# 내장함수 callable은 callable 인스턴스(즉, __call__ 메서드가 정의된 클래스 인스턴스)가 입력 파라미터로 들어오면 True 반환
assert callable(counter)


counter = BetterCountMissing()
result_5 = defaultdict(counter, current)
for key, amount in increments:
    result_5[key] += amount
assert counter.added == 2

# 결론: 상태 보존 함수가 필요할 때 closure를 정의하는 대신 __call__ method를 제공하는 클래스를 정의하는 방법을 고려할 것
print()



