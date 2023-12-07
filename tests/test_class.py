"""
Something to be aware of when grouping tests inside classes is that each test has
a unique instance of the class.
"""


class TestClass:
    def test_one(self):
        x = "this"
        assert "h" in x

    def test_two(self):
        x = "hello"
        print(x)
        # assert hasattr(x,"check")
