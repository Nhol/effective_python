import os
# 다형성: 계층 구조에 속한 여러 클래스가 자체의 메서드를 독립적인 버전으로 구현하는 방식


# example 1
class InputData(object): # 입력데이터를 표현할 공통 클래스 InputData
    def read(self): # 서브 클래스에서 정의해야 하는 read method(정의하지 않으면 NotImplementedError 발생)
        raise NotImplementedError


class PathInputData(InputData): # 파일에서 데이터를 읽어오도록 구현한 InputData 클래스의 서브클래스
    def __init__(self, path):
        # super 메서드로 부모 클래스를 초기화하여 path 속성 정의
        super().__init__()
        self.path = path

    def read(self):
        return open(self.path).read()


# example 2: MapReduce 작업 클래스 구현

class Worker(object):
    def __init__(self, input_data): # 입력데이터를 표현
        self.input_data = input_data
        self.result = None

    def map(self): # 서브 클래스에서 정의해야 할 map 메서드
        raise NotImplementedError

    def reduce(self, other): # 서브 클래스에서 정의해야 할 reduce 메서드
        raise NotImplementedError


# 적용하려는 특정 맵리듀스 함수를 구현한 Worker의 구체적인 서브 클래스
class LineCountWorker(Worker):
    def map(self):
        data = self.input_data.read() # input data를 읽어서 줄바꿈 문자를 카운트하는 map 함수
        self.result = data.count('\n')

    def reduce(self, other): # 결과들을 더해주는 reduce 함수
        self.result += other.result


# example 3: MapReduce 코드를 연결할 helper 함수 작성
def generate_inputs(data_dir):
    for name in os.listdir(data_dir): # 디렉터리의 내용을 나열하고 순회함
        yield PathInputData(os.path.join(data_dir, name)) # 디렉터리 안에 있는 각 파일로 PathInputData 인스턴스를 생성하는 제너레이터


# generate_inputs 함수에서 반환한 InputData 인스턴스를 사용하는 LineCountWorker 인스턴스 생성
# 이 함수는 list comprehension을 사용하면 다음과 같이 한줄로도 작성 가능: return [LineCountWorker(input_data) for input_data in input_list]
def create_workers(input_list):
    workers = []
    for input_data in input_list:
        workers.append(LineCountWorker(input_data))
    return workers


# map 단계를 여러 스레드로 나눠서 이 worker 인스턴스들을 실행. 그 다음 reduce를 반복적으로 호출 후 결과를 최종값 하나로 합치기
from threading import Thread


def execute(workers):
    threads = [Thread(target=w.map) for w in workers]
    for thread in threads: thread.start()
    for thread in threads: thread.join()

    first, rest = workers[0], workers[1:]
    for worker in rest:
        first.reduce(worker)
    return first.result


# mapreduce 함수에서 모든 조각을 연결
def mapreduce(data_dir):
    inputs = generate_inputs(data_dir)
    workers = create_workers(inputs)
    return execute(workers)


from tempfile import TemporaryDirectory # 임시 폴더, 파일 생성을 위한 라이브러리
import random


def write_test_files(tmpdir):
    for i in range(100):
        with open(os.path.join(tmpdir, str(i)), 'w') as f: # 반복문을 순회하며 temp directory에 숫자를 조합해 100개의 파일을 open
            f.write('\n' * random.randint(0, 100)) # 오픈한 파일에 줄바꿈 문자를 0 ~ 100개까지 랜덤으로 쓰기


with TemporaryDirectory() as tmpdir: # TemporaryDirectory를 tmpdir이란 이름으로 open
    write_test_files(tmpdir) # tmpdir에 파일 100개 생성
    result = mapreduce(tmpdir) # mapreduce 함수로 100개의 파일에서 줄바꿈 문자 카운터를 병렬로 100개 실행 후 각각의 카운트 결과를 더해줌

print('There are', result, 'lines')

# 위의 MapReduce 함수는 전혀 범용적이지 않음. InputData, Worker 서브 클래스를 변경하면 generate_input, create_worker, execute 모두 수정 필요
# 이를 보완하기 위해 @classmethod의 다형성 이용
