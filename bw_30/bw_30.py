# Better Way 30. 속성 리팩토링 대신 @property를 고려
"""
내장 @property 데코레이터를 사용하면 더 간결한 방식으로 인스턴스 속성에 접근 가능
호출하는 쪽을 변경하지 않고도 기존 클래스를 사용한 곳이 새로운 동작을 하게 해주므로 유용.
시간이 지나면서 인터페이스를 개선할 때 중요한 임시방편
"""


"""
Part 1.

구멍 난 양동이(leaky bucket) 알고리즘

구멍이 나서 내용물의 양이 감소하는 양동이에 input을 넣되 양이 넘치지 않도록 관리하는 알고리즘
이를 관리하기 위해서는 다음 조건을 고려해야 함
    1. 감소하는 양과 같거나 적은 input을 투입
    2. input이 양동이의 최대 부피를 넘지 않을 것
"""
from datetime import datetime, timedelta


class Bucket(object):
    def __init__(self, period):
        # 양동이를 내용물로 채우고 나서 그 내용물을 사용할 수 있는 시간
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.quota = 0

    def __repr__(self):
        return 'Bucket(quota={quota})'.format(quota=self.quota)


def fill(bucket, amount):
    now = datetime.now()
    if now - bucket.reset_time > bucket.period_delta:
        bucket.quota = 0
        bucket.reset_time = now
    bucket.quota += amount


def deduct(bucket, amount):
    now = datetime.now()
    if now - bucket.reset_time > bucket.period_delta:
        return False
    if bucket.quota - amount < 0:
        return False
    bucket.quota -= amount
    return True


"""
구현한 Bucket 클래스 사용해보기

1. 한번 채우며 유효시간이 60초인 양동이 생성
2. 100만큼 채우기
3. 99만큼 소진하기
4. 3만큼 소진하기 > False
"""
# 양동이 인스턴스를 생성하고 유효기간(period_delta) = 60초로 설정
bucket_1 = Bucket(60)

# 양동이를 100만큼 채움
fill(bucket_1, 100)
print(bucket_1)

# 99를 뺴기
if deduct(bucket_1, 99):
    print('Had 99 quota')
else:
    print('Not enough for 99 quota')
print(bucket_1)

# 다시 3을 더 빼려고 하면 남아있는 양이 1이므로 False를 반환
if deduct(bucket_1, 3):
    print('Had 3 quota')
else:
    print('Not enough for 3 quota')
print(bucket_1)


"""
Part 2. 

Bucket 클래스에서 인스턴스 생성 후 사용기간 동안 발생한 투입량(fill), 사용량(deduct)을 추적하기 위해 max_quota, quota_consumed 속성들을 추가함 
그리고 bucket에 남아있는 양 quota를 실시간으로 알 수 있도록 property method와 setter 추가
기존의 fill, deduct 메서드 코드는 수정하지 않아도 되도록 처리
"""


class Bucket(object):
    def __init__(self, period):
        self.period_delta = timedelta(period)
        self.reset_time = datetime.now()
        self.max_quota = 0
        self.quota_consumed = 0

    def __repr__(self):
        return 'Bucket(max_quota={max_quota}, quota_consumed={quota_consumed})'.format(
            max_quota=self.max_quota,
            quota_consumed=self.quota_consumed
        )

    # 새로 정의한 속성인 max_quota, quota_consumed을 이용해서 실시간으로 quota를 산출하기 위해 property 메서드 사용
    @property
    def quota(self):
        return self.max_quota - self.quota_consumed

    @quota.setter
    def quota(self, amount):
        delta = self.max_quota - amount
        if amount == 0:
            self.quota_consumed = 0
            self.max_quota = 0
        elif delta < 0:
            assert self.quota_consumed == 0
            self.max_quota = amount
        else:
            assert self.max_quota >= self.quota_consumed
            self.quota_consumed += delta


bucket_2 = Bucket(60)
print('Initial', bucket_2)
fill(bucket_2, 100)
print('Filled', bucket_2)

if deduct(bucket_2, 99):
    print('Had 99 quota')
else:
    print('Not enough for 99 quota')

print('Now', bucket_2)

if deduct(bucket_2, 3):
    print('Had 3 quota')
else:
    print('Not enough for 3 quota')

print('Still', bucket_2)


"""
위와 같이 작성함으로써 Bucket.quota를 사용하는 코드는 변경하거나 Bucket 클래스가 변경된 사실을 몰라도 무방하게 된다.
Bucket의 새 용법은 잘 동작하며 max_quota와 quota_consumed에 직접 접근할 수 있다.

<핵심정리>
기존의 인스턴스 속성에 새 기능을 부여하려면 @property를 사용하자
@property를 사용하여 점점 나은 데이터 모델로 발전시키자
@property를 너무 많이 사용한다면 클래스와 이를 호출하는 모든 곳을 리팩토링하는 방안을 고려하자.
"""

