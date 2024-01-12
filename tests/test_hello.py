import unittest
from app.hello import hello_word


class TestHelloWord(unittest.TestCase):
    def test_hello_world(self):
        self.assertEqual("hello world", hello_word())


if __name__ == "__main__":
    unittest.main()
