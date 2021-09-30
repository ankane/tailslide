from tailslide import percentile


class TestPercentile:
    def test_even(self):
        assert 3.25 == percentile([1, 2, 3, 4], .75)

    def test_odd(self):
        assert 29 == percentile([15, 20, 35, 40, 50], .4)
