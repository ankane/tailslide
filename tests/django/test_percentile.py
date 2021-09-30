from .conftest import User
from django.core.exceptions import FieldError
from tailslide import Percentile
import pytest


class TestPercentile:
    def setup_method(self, test_method):
        User.objects.all().delete()

    def test_even(self):
        for n in [1, 2, 3, 4]:
            User(visits_count=n).save()

        assert 3.25 == User.objects.aggregate(Percentile('visits_count', .75))['visits_count__percentile']

    def test_odd(self):
        for n in [15, 20, 35, 40, 50]:
            User(visits_count=n).save()

        assert 29 == User.objects.aggregate(Percentile('visits_count', .4))['visits_count__percentile']

    def test_empty(self):
        assert User.objects.aggregate(Percentile('visits_count', .75))['visits_count__percentile'] is None

    def test_null(self):
        for n in [1, 2, 3, 4, None]:
            User(visits_count=n).save()

        assert 3.25 == User.objects.aggregate(Percentile('visits_count', .75))['visits_count__percentile']

    def test_all_null(self):
        for n in [None, None, None]:
            User(visits_count=n).save()

        assert User.objects.aggregate(Percentile('visits_count', .75))['visits_count__percentile'] is None

    def test_zero(self):
        for n in [1, 2, 3, 4]:
            User(visits_count=n).save()

        assert 1 == User.objects.aggregate(Percentile('visits_count', 0))['visits_count__percentile']

    def test_one(self):
        for n in [1, 2, 3, 4]:
            User(visits_count=n).save()

        assert 4 == User.objects.aggregate(Percentile('visits_count', 1))['visits_count__percentile']

    def test_high(self):
        for n in [1, 1, 2, 3, 4, 100]:
            User(visits_count=n).save()

        assert pytest.approx(95.2) == User.objects.aggregate(Percentile('visits_count', .99))['visits_count__percentile']

    def test_missing_column(self):
        with pytest.raises(FieldError) as excinfo:
            User.objects.aggregate(Percentile('missing', 0.75))
        assert "Cannot resolve keyword 'missing' into field" in str(excinfo.value)

    def test_percentile_out_of_range(self):
        with pytest.raises(ValueError) as excinfo:
            User.objects.aggregate(Percentile('visits_count', 1.1))

    def test_percentile_non_numeric(self):
        with pytest.raises(ValueError) as excinfo:
            User.objects.aggregate(Percentile('visits_count', 'bad'))
        assert 'could not convert string to float' in str(excinfo.value)
