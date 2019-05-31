"""
Better Way 31.

재사용 가능한 @property 메서드에는 디스크립터를 사용하자.
@property로 데코레이트하는 메서드는 같은 클래스에 속한 여러 속성에 사용하지 못함.
관련 없는 클래스에서도 재사용 할 수 없음.
"""

# Part 1.


class Homework(object):
    def __init__(self):
        self._grade = 0

    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._grade = value


her = Homework()
her.grade = 95

"""
위의 예에서는 간편하게 grade 속성을 사용할 수 있으나 grade와 같이 @property로 데코레이트 된 메서드는 같은 클래스에 속한 여러 속성에 사용하지 못함
관련 없는 클래스에서도 재사용 불가
"""



# Part 2.
"""
시험 성적을 과목 별로 매기는 경우 Part 1의 예시처럼 과목별 점수를 관리하려면 과목마다 @property 데코레이터, setter 메서드가 필요.
이는 코드가 지나치게 장황해짐
"""


class Exam(object):
    def __init__(self):
        self._writing_grade = 0
        self._math_grade = 0

    @staticmethod
    def _check_grade(value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be in between 0 and 100')

    @property
    def writing_grade(self):
        return self._writing_grade

    @writing_grade.setter
    def writing_grade(self, value):
        self._check_grade(value)
        self._writing_grade = value

    @property
    def math_grade(self):
        return self._math_grade

    @math_grade.setter
    def math_grade(self, value):
        self._check_grade(value)
        self._math_grade = value

"""
이와 같은 방식으로는 과목이 늘어날 수록 반복적으로 @property method와 _check_grade메서드를 작성해야 함
이런 상황에서는 descriptor 사용을 권장

descriptor protocol은 속성에 대한 접근을 언어에서 해석할 방법을 정의해줌.
descriptor 클래스는 반복코드 없이도 성적 검증 동작을 재사용할 수 있게 해주는 __get__, __set__ 메서드를 제공,
한 클래스의 서로 다른 많은 속성에 같은 로직을 재사용할 수 있게 됨

새로운 Exam 클래스는 다음과 같은 방법으로 구현

1. Grade 클래스를 정의하고 그 인스턴스를 Exam 클래스의 속성으로 가짐
2. Grade 클래스는 디스크립터 프로토콜 구현
"""


# Part 3.
"""
아래의 Grade1 class는 Grade1의 인스턴스가 모든 Exam 인스턴스의 클래스 속성으로 공유됨 

"""


class Grade1(object):
    def __init__(self):
        self._value = 0

    def __get__(self, instance, instance_type):
        return self._value

    def __set__(self, instance, value):
        if not(0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._value = value


class Exam1(object):
    math_grade = Grade1()
    writing_grade = Grade1()
    science_grade = Grade1()


first_exam = Exam1()
first_exam.writing_grade = 82
first_exam.science_grade = 99
print('writing ', first_exam.writing_grade)
print('science ', first_exam.science_grade)

'''
위처럼 하나의 Exam2 클래스 인스턴스의 속성에 접근할 때는 정상 동작함.
하지만 아래처럼 Exam2 클래스 인스턴스를 2개 이상 생성한 경우에는 속성 접근 시 기대하지 않은 동작을 할 수 있음
문제는 한 Grade 인스턴스가 모든 Exam2 인스턴스의 속성으로 공유되는 것

'''

second_exam = Exam1()
second_exam.writing_grade = 75
print('Second', second_exam.writing_grade, 'is right')
print('First', first_exam.writing_grade, 'fist_exam의 writing_grade는 82점이지만 second_exam의 writing_grade에 할당한 75점이 출력됨')


# Part 4.
"""
각 Exam2 인스턴스별로 값을 추적하는 Grade 클래스 필요
딕셔너리에 각 인스턴스의 상태를 저장하는 방법으로 값 추적

단, 이 방식은 프로그램의 수명동안 _values 딕셔너리에 모든 Exam2 인스턴스의 참조를 저장하기 때문에 인스턴스의 참조 갯수가 절대로 0이 되지 않아 
가비지 컬렉터가 정리하지 못하기 때문에 메모리 누수 문제가 발생하게 됨  
"""


class Grade2(object):
    def __init__(self):
        self._values = {}

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._values[instance] = value


class Exam2(object):
    math_grade = Grade2()
    writing_grade = Grade2()
    science_grade = Grade2()


spring_exam = Exam2()
spring_exam.writing_grade = 98
spring_exam.math_grade = 100
print('spring exam, writing grade: ', spring_exam.writing_grade)
print('spring exam, math grade: ', spring_exam.math_grade)


autumn_exam = Exam2()
autumn_exam.writing_grade = 70
autumn_exam.math_grade = 87
print('autumn exam, writing grade: ', autumn_exam.writing_grade)
print('autumn exam, math grade: ', autumn_exam.math_grade)


# Part 5.
'''
파이썬 내장모듈 weakref(약한 참조)를 사용해서 문제 해결 가능
weakref는 _values에 사용한 dict를 대체할 수 있는 WeakKeyDictionary라는 특별한 클래스를 제공
이 클래스는 런타임에 마지막으로 남은 Exam2 인스턴스의 참조를 갖고 있다는 사실을 알면 키 집합에서 Exam2 인스턴스를 제거 
모든 Exam2 인스턴스가 더이상 사용되지 않으면 _values 딕셔너리가 비어있게 하는 동작
'''


from weakref import WeakKeyDictionary


class Grade3(object):
    def __init__(self):
        self._values = WeakKeyDictionary()

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._values[instance] = value


class Exam3(object):
    math_grade = Grade3()
    writing_grade = Grade3()
    science_grade = Grade3()


summer_exam = Exam3()
summer_exam.writing_grade = 98
print('summer exam, writing grade: ', summer_exam.writing_grade)

winter_exam = Exam3()
winter_exam.writing_grade = 72
print('winter exam, writing grade: ', winter_exam.writing_grade)\

print()