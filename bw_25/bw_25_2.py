# example 4: 다이아몬드 상속 문제


class MyBaseClass(object):
    def __init__(self, value):
        self.value = value


class TimesFive(MyBaseClass):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        self.value *= 5


class PlusTwo(MyBaseClass):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        self.value += 2


# MyBaseClass가 다이아몬드 상속의 꼭대기가 됨
class ThisWay(TimesFive, PlusTwo):
    def __init__(self, value):
        TimesFive.__init__(self, value)
        PlusTwo.__init__(self, value) # 이 과정에서 MyBaseClass의 __init__ 메서드를 호출하면서 self.value를 다시 5로 리셋


foo = ThisWay(5)
print('Should be (5 * 5) + 2 = 27 but is', foo.value)


# 이 문제를 해결하기 위해 python 2.2에서부터 super라는 내장함수 추가, 메서드 해석순서(MRO, Method Resolution Order) 정의
# MRO는 어떤 슈퍼클래스부터 초기화 하는지 정함: 오른쪽에서 왼쪽으로


# Example
# This is pretending to be Python 2 but it's not
class MyBaseClass(object):
    def __init__(self, value):
        self.value = value


class TimesFiveCorrect(MyBaseClass):
    def __init__(self, value):
        super(TimesFiveCorrect, self).__init__(value)
        self.value *= 5


class PlusTwoCorrect(MyBaseClass):
    def __init__(self, value):
        super(PlusTwoCorrect, self).__init__(value)
        self.value += 2


class GoodWay(TimesFiveCorrect, PlusTwoCorrect):
    def __init__(self, value):
        super(GoodWay, self).__init__(value)


from pprint import pprint
pprint(GoodWay.mro())
pprint = pprint

# 위의 출력 결과 호출 순서 파악 가능:
#   GoodWay(5) 호출 > TimesFiveCorrect.__init__ 호출 > PlusTwoCorrect.__init__ 호출 > MyBaseClass.__init__ 호출
# 이 호출이 다이아몬드의 꼭대기에 도달하면 모든 초기화 메서드는 실제 __init__ 함수가 호출된 순서의 역순으로 실행됨

foo = GoodWay(5)
print('Should be 5 * (5 + 2 ) = 35 and is', foo.value)


# Example
class Explicit(MyBaseClass):
    def __init__(self, value):
        super(__class__, self).__init__(value * 2)


class Implicit(MyBaseClass):
    def __init__(self, value):
        super().__init__(value * 2)


assert Explicit(10).value == Implicit(10).value


print()


