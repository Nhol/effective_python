# Chapter 4. Better Way 29
# getter, setter 메서드 대신 일반 속성을 사용하자.
"""
자바와 같은 언어에서는 class의 속성에 접근(get)하거나 속성을 설정(set)하는
getter, setter 메서드를 작성하는 경우가 많음.
하지만 python에서는 getter, setter 메서드보다는 일반 속성 사용을 권장함.
"""


# Part 1. python은 getter, setter가 필요 없음
class OldResistor(object):
    def __init__(self, ohms):
        self._ohms = ohms

    # getter method: 클래스의 특정 property value를 get하는 함수
    def get_ohms(self):
        return self._ohms

    # setter method: 클래스의 특정 property value를 set하는 함수
    def set_ohms(self, ohms):
        self._ohms = ohms


# 값을 출력하는데는 이상이 없지만 위에서 정의한 getter, setter 메서드 사용은 pythonic 하지 않음
r1 = OldResistor(50e3)
print('Before: %5r' % r1.get_ohms())
r1.set_ohms(10e3)
print('After: %5r' % r1.get_ohms())

# 값을 증가시키는 간단한 연산도 불편해짐
r1.set_ohms(r1.get_ohms() + 5e3)
print('Last: %5r' % r1.get_ohms())


# Part 2: python에서는 위와 같은 명시적인 getter, setter 메서드 보다는 공개 속성을 구현
class Resistor(object):
    def __init__(self, ohms):
        self.ohms = ohms
        self.voltage = 0
        self.current = 0


# 속성 값 호출 및 대입도 간편
r2 = Resistor(50e3)
print(r2.ohms)
r2.ohms = 10e3
print(r2.ohms)

# 값을 증가시키는 연산도 훨씬 간편
r2.ohms += 5e3
print(r2.ohms)


# Part 3: 속성 설정 시 특별한 동작이 발생해야 하는 경우엔 @property 데코레이터와 이에 상응하는 setter 속성을 사용하여 함수 구현
"""
다음의 VoltageResistance 클래스는 위에서 정의한 Resistor 클래스를 상속함. 
즉, 이미 일반 속성값으로 ohms, voltage, current를 가짐.

여기서 첫번째, voltage 메서드에 @property 데코레이터를 사용하면 voltage 메서드를 속성 사용 가능
'class_instance.voltage'처럼 사용 가능

두번째, voltage 메서드에 setter 데코레이터를 설정하면 setter처럼 값을 대입할 수 있음.  
'class_instance.voltage = 3'처럼 입력하면 
    1. 해당 인스턴스의 _voltage 값은 3으로 설정되고,
    2. current 값은 I(current) = V(voltage)/R(resistor) 수식에 따라 설정됨   
"""


class VoltageResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)
        self._voltage = 0

    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, voltage):
        self._voltage = voltage
        self.current = self._voltage / self.ohms


r3 = VoltageResistance(100)
print('Before: %5r amps' % r3.current)

# voltage 메서드에 마치 속성처럼 접근 가능
r3.voltage = 500
print('After: %5r amps' % r3.current)


# Part 4: 모든 저항값이 0옴보다 큼을 보장하는 클래스 정의
"""
@property에 setter를 설정하면 클래스에 전달될 값들의 타입 체크나 검사가 가능
다음은 저항값(ohms)이 0보다 큼을 보장하는 클래스
"""


class BoundedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if ohms <= 0:
            raise ValueError('%f ohms must be > 0' % ohms)
        self._ohms = ohms


r4 = BoundedResistance(1e3)
# r4.ohms = 0  # -> 예외 발생
# >>> 0 ohms must be > 0
# r4 = BoundedResistance(-5) -> 예외 발생
# >>> 0 ohms must be > 0
"""
__init__에 검증식을 넣지 않았는데도 인스턴스를 생성할 때 검증됨.
    1. 왜냐하면 __init__에 ohms를 설정하는 문장이 있고,(self.ohms = ..)
    2. property 메서드 ohms이 정의되어 있으며
    3. @ohms.setter도 정의되어 있기 때문에  
ohms에 값을 대입하려 하면 @ohms.setter 메서드가 호출되어 객체 생성이 완료되기 전에 @ohms.setter 메서드의 검증코드가 먼저 실행됨
"""


# Part 5: 부모 클래스의 속성을 불변(immutable)으로 만들 때 @property 데코레이터 사용 가능
"""
Part 4의 ohms > 0 검증 코드를 hasattr 검증으로 변경하여 해당속성을 바꾸지 못하도록 한 것
"""


class FixedRegistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if hasattr(self, '_ohms'):
            raise AttributeError("Can't set attribute")
        self._ohms = ohms


r5 = FixedRegistance(100)
# r5.ohms = 200 -> 예외 발생
# >>> AttributeError: Can't set attribute



# Part 6: getter의 property method에서 다른 속성을 설정하지 말 것
"""
@property의 가장 큰 단점은 속성에 대응하는 메서드를 서브클래스에서만 공유할 수 있다는 점이다.
서로 관련이 없는 클래스는 같은 구현을 공유하지 못함.
하지만 파이썬은 재사용 가능한 프로퍼티 로직을 비롯해 다른 많은 쓰임새를 가능하게 하는 디스크립터(descriptor)도 지원(31장 참조)

마지막으로 @property 메서드로 게터와 세터를 구현할 때 예상과 다르게 동작하지 않게 해야 한다. 
예를 들면 게터 프로퍼티 메서드에서 다른 속성을 설정하지 말아야 한다.
"""


class MysteriousRegister(Resistor):
    @property
    def ohms(self):
        # 다음과 같은 코드는 아주 이상한 동작을 만들어낸다. ohms 속성의 property 메서드에서 voltage 속성이나 current 속성을 변경하게 되기 때문
        self.voltage = self._ohms * self.current
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        self._ohms = ohms


print('Part 6')
r6 = MysteriousRegister(10) # 이렇게 인스턴스를 생성하면 ohms = 10, _ohms = 10(setter 메서드를 통해), current = voltage = 0로 설정됨.
r6.current = 0.01 # current 속성값을 변경했지만 ohms property 메서드가 호출되지는 않았으므로 current 속성값만 변경되고 voltage는 변화없음
print('Before: %5r' % r6.voltage) # voltage = 0인 상태
r6.ohms # ohms가 호출되서야 property method가 호출되어 voltage 값이 변경됨
print('After: %5r' % r6.voltage)
