# Example 1
class OldResistor(object):
    def __init__(self, ohms):
        self._ohms = ohms

    # getter method: 클래스의 특정 property value를 get하는 함수
    def get_ohms(self):
        return self._ohms

    # setter method: 클래스의 특정 property value를 set하는 함수
    def set_ohms(self, ohms):
        self._ohms = ohms


# 하지만 위에서 정의한 getter, setter 사용법은 pythonic 하지 않음
r0 = OldResistor(50e3)
print('Before: %5r' % r0.get_ohms())
r0.set_ohms(10e3)
print('After: %5r' % r0.get_ohms())
r0.set_ohms(r0.get_ohms() + 5e3)
print('Last: %5r' % r0.get_ohms())


# Example 2: python에서는 위와 같은 명시적인 getter, setter 보다는 공개 속성부터 구현
class Resistor(object):
    def __init__(self, ohms):
        self.ohms = ohms
        self.voltage = 0
        self.current = 0


r1 = Resistor(50e3)
print(r1.ohms)
r1.ohms = 10e3
print(r1.ohms)
r1.ohms += 5e3
print(r1.ohms)


# Example 3: 속성 설정 시 특별한 동작이 발생해야 하는 경우엔 @property 데코레이터와 이에 상응하는 setter 속성을 사용하여 함수 구현
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


r2 = VoltageResistance(1e3)
print('Before: %5r amps' % r2.current)
r2.voltage = 10
print('After: %5r amps' % r2.current)


# Example 4: 모든 저항값이 0옴보다 큼을 보장하는 클래스 정의
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


r3 = BoundedResistance(1e3)
# r3.ohms = 0  -> 예외 발생
# BoundedResistance(-5) -> 예외 발생



# Example 5: 부모 클래스의
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



