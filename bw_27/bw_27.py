import logging
from pprint import pprint
from sys import stdout as STDOUT
# example 1. python의 class 가시성(visibility) 속성은 공개(public)와 비공개(private) 2가지 유형밖에 없음


class MyObject(object):
    def __init__(self):
        self.public_field = 5
        self.__private_field = 10

    def get_private_field(self):
        return self.__private_field


foo = MyObject()
assert foo.public_field == 5


# 동일 클래스의 메서드로 private 속성 접근 가능
assert foo.get_private_field() == 10

# 외부에서 직접 비공개 필드 접근시 예외 발생
# print(foo.__private_field)


# example 2. 클래스 메서드도 비공개 속성 접근 가능(같은 class block에 선언되어 있으므로)
class MyOtherObject(object):
    def __init__(self):
        self.__private_field = 71

    @classmethod
    def get_private_field_of_instance(cls, instance):
        return instance.__private_field


bar = MyOtherObject()
assert MyOtherObject.get_private_field_of_instance(bar) == 71


# example 3. subclass에서는 부모 클래스의 비공개 필드 접근 불가
class MyParentObject(object):
    def __init__(self):
        self.__private_field = 71


class MyChildObject(MyParentObject):
    def get_private_field(self):
        return self.__private_field


baz = MyChildObject()
# subclass에서 부모 클래스의 비공개 필드 접근시 예외 발생
# baz.get_private_field()
print()


# 사실 python의 private field 보호는 엄격하지 않음. instance(or class).__private_field를 _classname__private_field로 변환하는 것에 불과
print(baz._MyParentObject__private_field)

# 인스턴스의 속성 딕셔너리 살펴보기
print(baz.__dict__)


# example 4. 서브 클래스나 외부에서 접근하면 안되는 내부 API를 비공개 필드로 나타낸 예(잘못된 방식)
class MyClass(object):
    def __init__(self, value):
        self.__value = value

    def get_value(self):
        return str(self.__value)


foo = MyClass(5)
assert foo.get_value() == '5'


# 이 경우 서브클래스에서 비공개 필드 접근이 꼭 필요하면 여전히 접근 가능
class MyIntegerSubclass(MyClass):
    def get_value(self):
        return int(self._MyClass__value)


foo = MyIntegerSubclass(5)
assert foo.get_value() == 5


# example 5. 나중에 클래스의 계층이 변경되면 MyIntegerSubClass 같은 클래스는 비공개 참조가 더는 유효하지 않게 됨.
class MyBaseClass(object):
    def __init__(self, value):
        self.__value = value

    def get_value(self):
        return self.__value


class MyClass(MyBaseClass):
    def get_value(self):
        return str(super().get_value())


class MyIntegerSubclass(MyClass):
    def get_value(self):
        return int(self._MyClass__value)


# try:
#     foo = MyIntegerSubclass(5)
#     foo.get_value() # 부모클래스의 비공개 속성이므로 접근 불가하여 예외 발생
# except:
#     logging.exception('Expected')
# else:
#     assert False


# example 6. 무조건 비공개 속성을 사용하기 보다는 보호된 속성을 사용하면서 문서화를 잘 해두는 편이 낫다.
class MyClass(object):
    def __init__(self, value):
        '''
        :param value:
            사용자가 객체에 전달한 값을 저장한다.
            문자열로 강제할 수 있는 값이어야 하며,
            객체에 할당하고 나면 불변으로 취급해야 한다.
        '''
        self._value = value


class MyIntegerSubclass(MyClass):
    def get_value(self):
        return self._value


foo = MyIntegerSubclass(5)
assert foo.get_value() == 5


# example 7. 비공개 속성을 고민할 시점은 서브클래스와 이름이 충돌할 때
class ApiClass(object):
    def __init__(self):
        self._value = 5

    def get(self):
        return self._value


class Child(ApiClass):
    def __init__(self):
        super().__init__()
        self._value = 'hello' # 충돌


a = Child()
# 부모클래스의 _value와 자식 클래스에서 초기화한 _value는 서로 달라야 하지만 아래처럼 동일한 결과가 나타남
print(a.get(), 'and', a._value, 'should be different')


# example 8. 클래스가 공개 API의 일부일 때 문제가 됨
class ApiClass(object):
    def __init__(self):
        self.__value = 5 # 부모 클래스의 value 속성을 비공개로 변경

    def get(self):
        return self.__value


class Child(ApiClass):
    def __init__(self):
        super().__init__()
        self._value = 'hello'


a = Child()
print(a.get(), 'and', a._value, 'are different')

# 파이썬 컴파일러는 비공개 속성을 엄격하게 강요하지 않음
# 서브클래스가 내부 API와 속성에 접근하지 못하게 막기보다는 처음부터 내부 API와 속성으로 더 많은 일을 할 수 있게 설계할 것
# 비공개 속성에 대한 접근을 강제로 제어하지 말고 보호 필드를 문서화해서 지침 제공
# 직접 제어할 수 없는 서브클래스와 이름이 충돌하지 않게 할 때만 비공개 속성을 사용
