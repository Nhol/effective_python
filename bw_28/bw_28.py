import logging
from pprint import pprint
from sys import stdout as STDOUT

# 모든 파이썬 클래스는 일종의 컨테이너로 속성과 기능을 함께 캡슐화한다.


# Example 1
class FrequencyList(list):
    def __init__(self, members):
        super().__init__(members)

    def frequency(self):
        counts = {}
        for item in self:
            counts.setdefault(item, 0)
            counts[item] += 1
        return counts


foo = FrequencyList(['a', 'b', 'a', 'c', 'b', 'a', 'd'])
print('Length is', len(foo))
foo.pop()
print('After pop:', repr(foo))
print('Frequency:', foo.frequency())
print()


# Example 2. list의 서브클래스가 아니어도 인덱스로 접근할 수는 클래스 만들기
class BinaryNode(object):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


bar = [1, 2, 3]
print(bar[0])
print(bar.__getitem__(0))
print()


class IndexableNode(BinaryNode):
    def _search(self, count, index):
        found = None
        if self.left:
            found, count = self.left._search(count, index) # self.left도 IndexableNode의 객체이면 _search 메서드 재귀적으로 동작
        if not found and count == index:
            found = self
        else:
            count += 1
        if not found and self.right:
            found, count = self.right._search(count, index)
        return found, count
        # Returns (found, count)

    def __getitem__(self, index):
        found, _ = self._search(0, index)
        if not found:
            raise IndexError('Index out of range')
        return found.value


tree = IndexableNode(
    1,
    left=IndexableNode(
        15,
        left=IndexableNode(28),
        right=IndexableNode(
            6, right=IndexableNode(7))),
    right=IndexableNode(
        2, left=IndexableNode(4)))

print('LRR = ', tree.left.right.right.value)
print('Index 0 =', tree[0])
print('Index 1 =', tree[1])
print('11 in the tree?', 11 in tree)
print('17 in the tree?', 17 in tree)
print('Tree is', list(tree))
# len(tree)
print(tree[0], tree[1], tree[2], tree[3], tree[4], tree[5], tree[6])

# 그러나 sequence semantic(의미의, 의미론적)의 기능(index, len, count, ...)을 모두 제공하기에 __getitem__은 부족
# len을 쓰려면 __len__  구현 필요


# example 3.
class SequenceNode(IndexableNode):
    def __len__(self):
        _, count = self._search(0, None)
        return count


tree = SequenceNode(
    10,
    left=SequenceNode(
        5,
        left=SequenceNode(2),
        right=SequenceNode(
            6, right=SequenceNode(7))),
    right=SequenceNode(
        15, left=SequenceNode(11))
)

print('Tree has %d nodes' % len(tree))
print(tree[0])


# custom container type을 정의하는 일은 생각보다 어려우므로 파이썬에서는 컨테이너 타입에 필요한 일반적인 추상기반 클래스 제공
try:
    from collections.abc import Sequence


    class BadType(Sequence):
        pass


    foo = BadType() # Sequence 클래스를 상속받아도 필수 메서드 구현이 누락되면 바로 예외 발생
except:
    logging.exception('Expected')
else:
    assert False


class BetterNode(SequenceNode, Sequence):
    pass

tree = BetterNode(
    10,
    left=BetterNode(
        5,
        left=BetterNode(2),
        right=BetterNode(
            6, right=BetterNode(7))),
    right=BetterNode(
        15, left=BetterNode(11))
)

print('Index of 7 is', tree.index(7))
print('Count of 10 is', tree.count(10))
print()