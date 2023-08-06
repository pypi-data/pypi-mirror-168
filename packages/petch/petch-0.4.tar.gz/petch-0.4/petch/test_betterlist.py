from unittest import TestCase
from betterlist import BetterList as BL


class TestBetterList(TestCase):
    def test_copy(self):
        _list1 = BL([1, 2, 3, 4])
        self.assertEqual(_list1, _list1.copy())

    def test_sort(self):
        _list1 = BL([2, 3, 1, 0])
        _sorted_list1 = BL([0, 1, 2, 3])
        self.assertEqual(_list1.sort(), _sorted_list1)

        _sorted_list2 = BL([3, 1, 0, 2])
        self.assertEqual(_list1.sort(lambda x: (-2) ** x), _sorted_list2)

    def test_min(self):
        _list1 = BL([2, 3, 1, 4])
        self.assertEqual(_list1.min(1)[0], 1)
        self.assertEqual(_list1.min(2, lambda x: (-2) ** x), [3, 1])

    def test_max(self):
        _list1 = BL([2, 3, 1, 4, 5])
        self.assertEqual(_list1.max(1)[0], 5)
        self.assertEqual(_list1.max(2, lambda x: (-2) ** x), [4, 2])

    def test_value_after(self):
        _list1 = BL([2, 1, 4, 5, 3])
        self.assertEqual(_list1.value_after(1), 4)

    def test_first(self):
        _list1 = BL([2, 1, 4, 5])
        self.assertEqual(_list1.first(3), BL([2, 1, 4]))

    def test_create_list(self):
        _list1 = BL(range(3))
        self.assertEqual(_list1, BL([0, 1, 2]))

    def test_add(self):
        _list1 = BL(range(5))
        self.assertEqual(_list1, BL([0, 1, 2, 3]) + BL([4]))
        self.assertEqual(type(_list1), type(BL([0, 1, 2, 3]) + BL([4])))
        _list1 += BL([5])
        self.assertEqual(_list1, BL([0, 1, 2, 3]) + BL([4, 5]))
        self.assertEqual(type(_list1), type(BL([0, 1, 2, 3]) + BL([4, 5])))

    def test_mul(self):
        _list1 = BL(range(3)) * 3
        _result = BL([0, 1, 2, 0, 1, 2, 0, 1, 2])
        self.assertEqual(_list1, _result)
        self.assertEqual(type(_list1), type(_result))
        _list1 = BL(range(3))
        _list1 *= 3
        _result = BL([0, 1, 2, 0, 1, 2, 0, 1, 2])
        self.assertEqual(_list1, _result)
        self.assertEqual(type(_list1), type(_result))

    def test_getitem(self):
        list1 = BL(range(4))
        self.assertEqual(list1[1], 1)
        self.assertEqual(list1[0:2], BL([0, 1]))
        self.assertEqual(type(list1[0:2]), BL)
        self.assertEqual(list1[::-1], BL([3, 2, 1, 0]))
        self.assertEqual(type(list1[::-1]), BL)
