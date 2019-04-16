# example 1
class MyBaseClass(object):
    def __init__(self, value):
        self.value = value


class MyChildClass(MyBaseClass):
    # 자식 클래스에서 부모 클래스의 __init__ 메서드를 직접 호출하는 방법으로 부모 클래스 초기화하는 방법.
    # 단, 다중 상속을 사용하는 경우 부모 클래스의 __init__ 메서드 직접 호출은 예기치 못한 문제를 일으킬 수 있음
    def __init__(self):
        MyBaseClass.__init__(self, 5)

    def times_two(self):
        return self.value * 2


foo = MyChildClass()
print(foo.times_two())
print()


# example 2
class TimesTwo(object):
    def __init__(self):
        self.value *= 2


class PlusFive(object):
    def __init__(self):
        self.value += 5


class OneWay(MyBaseClass, TimesTwo, PlusFive):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        TimesTwo.__init__(self)
        PlusFive.__init__(self)


foo = OneWay(5)
print('First ordering is (5 * 2) + 5 =', foo.value)


# example 3
# OneWay와 동일한 내용의 함수. 단, 부모 클래스르르 상속하는 순서만 다르게 정의한 클래스
class AnotherWay(MyBaseClass, PlusFive, TimesTwo):
    def __init__(self, value):
        # 호출 순서는 이전과 동일
        MyBaseClass.__init__(self, value)
        TimesTwo.__init__(self)
        PlusFive.__init__(self)


# 이 클래스의 동작은 부모 클래스를 정의한 순서와 일치하지 않음
bar = AnotherWay(5)
print('Second ordering still is', bar.value)
print()
