import unittest

from ytmurl.get import get


class TestSimple(unittest.TestCase):

    def test_add(self):
        self.assertIsNotNone(get('降水确率10% Falcom Sound Team J.D.K.'))

if __name__ == '__main__':
    unittest.main()
