def test_int_casting():
    assert int('5') == 5


class TestFloats:

    def test_dot(self):
        assert float('3.3') == 3.3

    def test_e(self):
        assert float('3.1e3') == 3100.0