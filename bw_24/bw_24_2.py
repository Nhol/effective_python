import os


class GenericInputData(object):
    def read(self):
        raise NotImplementedError

    @classmethod
    def generate_inputs(cls, config): # GenericInputData를 구현하는 서브클래스가 해석할 설정 파라미터들을 담은 딕셔너리(config)를 받음
        raise NotImplementedError


class PathInputData(GenericInputData):
    def __init__(self, path):
        super().__init__()
        self.path = path

    def read(self):
        return open(self.path).read()

    @classmethod
    def generate_inputs(cls, config):
        data_dir = config['data_dir'] # 입력 파일들을 얻어올 디렉토리를 config로 알아냄
        for name in os.listdir(data_dir):
            yield cls(os.path.join(data_dir, name))


class GenericWorker(object):
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError

    @classmethod
    def create_workers(cls, input_class, config): # __init__ 메서드를 사용하지 않고 cls를 호출함으로써 GenericWorker를 생성
        workers = []
        for input_data in input_class.generate_inputs(config):
            workers.append(cls(input_data))
        return workers


class LineCountWorker(GenericWorker): # GenericWorker를 구현할 서브 클래스는 부모 클래스만 변경하면 된다
    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')

    def reduce(self, other):
        self.result += other.result


from threading import Thread


def execute(workers):
    threads = [Thread(target=w.map) for w in workers]
    for thread in threads: thread.start()
    for thread in threads: thread.join()

    first, rest = workers[0], workers[1:]
    for worker in rest:
        first.reduce(worker)
    return first.result


# mapreduce 함수를 완전히 범용적으로 재작성
def mapreduce(worker_class, input_class, config):
    workers = worker_class.create_workers(input_class, config)
    return execute(workers)


from tempfile import TemporaryDirectory
import random


def write_test_files(tmpdir):
    for i in range(100):
        with open(os.path.join(tmpdir, str(i)), 'w') as f:
            f.write('\n' * random.randint(0, 100))


with TemporaryDirectory() as tmpdir:
    write_test_files(tmpdir)
    config = {'data_dir': tmpdir}
    result = mapreduce(LineCountWorker, PathInputData, config)
print('There are', result, 'lines')
print()

# python에서는 클래스별로 생성자를 1개만(__init__ 메서드)만 만들 수 있음
# 클래스에 필요한 다른 생성자를 정의하려면 @classmethod를 사용할 것
# 구체 서브 클래스들을 만들고 연결하는 범용적인 방법을 제공하려면 클래스 메서드 다형성을 이용