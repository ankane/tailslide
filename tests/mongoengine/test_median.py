from .conftest import User
from mongoengine.errors import LookUpError
import pytest


class TestMedian:
    def setup_method(self, test_method):
        User.objects.all().delete()

    def test_even(self):
        for n in [1, 1, 2, 3, 4, 100]:
            User(visits_count=n).save()

        assert 2.5 == User.objects.median('visits_count')

    def test_odd(self):
        for n in [1, 1, 2, 4, 100]:
            User(visits_count=n).save()

        assert 2 == User.objects.median('visits_count')

    def test_empty(self):
        assert User.objects.median('visits_count') is None

    def test_null(self):
        for n in [1, 1, 2, 3, 4, 100, None]:
            User(visits_count=n).save()

        assert 2.5 == User.objects.median('visits_count')

    def test_all_null(self):
        for n in [None, None, None]:
            User(visits_count=n).save()

        assert User.objects.median('visits_count') is None

    def test_decimal(self):
        for n in range(6):
            User(latitude=n * 0.1).save()

        assert 0.25 == User.objects.median('latitude')

    def test_float(self):
        for n in range(6):
            User(rating=n * 0.1).save()

        assert 0.25 == User.objects.median('rating')

    def test_missing_column(self):
        with pytest.raises(LookUpError) as excinfo:
            User.objects.median('missing')
        assert 'Cannot resolve field "missing"' in str(excinfo.value)
