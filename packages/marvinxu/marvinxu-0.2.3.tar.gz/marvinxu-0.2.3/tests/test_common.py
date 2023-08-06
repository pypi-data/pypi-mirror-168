import unittest

from marvinxu import filter_none, is_valid_idcard


class TestCommon(unittest.TestCase):
    def test_is_valid_idcard(self):
        self.assertTrue(is_valid_idcard("441223197807234511"), "valid idcard")
        self.assertFalse(is_valid_idcard("441223197807234512"), "invalid idcard")
        self.assertFalse(is_valid_idcard("00"), "invalid idcard")
        self.assertFalse(is_valid_idcard(0), "invalid idcard")

    def test_filter_none(self):
        assert filter_none({"foo": 1, "bar": None}) == {"foo": 1}


if __name__ == "__main__":
    unittest.main()
