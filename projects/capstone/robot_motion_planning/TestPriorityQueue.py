import unittest
from PriorityQueue import *


class TestPriorityQueue(unittest.TestCase):
    def test_pop_min(self):
        q1 = PriorityQueue()
        q1.insert(3, 'c')
        q1.insert(2, 'b')
        q1.insert(1, 'a')

        self.assertEqual(q1.pop_min(), 'a')
        self.assertEqual(q1.pop_min(), 'b')
        self.assertEqual(q1.pop_min(), 'c')

    def test_pop_min_is_depth_first(self):
        q = PriorityQueue(lifo=True)
        q.insert(1, 'b')
        q.insert(2, 'c')
        q.insert(1, 'a')

        self.assertEqual(q.pop_min(), 'a')
        self.assertEqual(q.pop_min(), 'b')
        self.assertEqual(q.pop_min(), 'c')

    def test_pop_min_is_breadth_first(self):
        q = PriorityQueue(lifo=False)
        q.insert(1, 'b')
        q.insert(2, 'c')
        q.insert(1, 'a')

        self.assertEqual(q.pop_min(), 'b')
        self.assertEqual(q.pop_min(), 'a')
        self.assertEqual(q.pop_min(), 'c')


if __name__ == '__main__':
    unittest.main()
