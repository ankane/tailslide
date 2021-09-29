from .conftest import User
from django.core.exceptions import FieldError
from django.db.models.aggregates import Avg
from tailslide import Median
import os
import pytest


class TestMedian:
    def setup_method(self, test_method):
        User.objects.all().delete()

    def test_even(self):
        for n in [1, 1, 2, 3, 4, 100]:
            User(visits_count=n).save()

        assert 2.5 == User.objects.aggregate(Median('visits_count'))['visits_count__median']

    def test_odd(self):
        for n in [1, 1, 2, 4, 100]:
            User(visits_count=n).save()

        assert 2 == User.objects.aggregate(Median('visits_count'))['visits_count__median']

    def test_empty(self):
        assert User.objects.aggregate(Median('visits_count'))['visits_count__median'] is None

    def test_null(self):
        for n in [1, 1, 2, 3, 4, 100, None]:
            User(visits_count=n).save()

        assert 2.5 == User.objects.aggregate(Median('visits_count'))['visits_count__median']

    def test_all_null(self):
        for n in [None, None, None]:
            User(visits_count=n).save()

        assert User.objects.aggregate(Median('visits_count'))['visits_count__median'] is None

    def test_decimal(self):
        for n in range(6):
            User(latitude=n * 0.1).save()

        assert 0.25 == User.objects.aggregate(Median('latitude'))['latitude__median']

    def test_float(self):
        for n in range(6):
            User(rating=n * 0.1).save()

        assert 0.25 == User.objects.aggregate(Median('rating'))['rating__median']

    def test_group(self):
        for n in [1, 2, 3, 4, 5, 6]:
            User(visits_count=n, name=('A' if n < 4 else 'B')).save()

        expected = [{'name': 'A', 'value': 2.0}, {'name': 'B', 'value': 5.0}]
        assert expected == list(User.objects.values('name').annotate(value=Avg('visits_count')).order_by('name'))

        if os.environ.get('ADAPTER') == 'mariadb' or os.environ.get('ADAPTER') == 'sqlserver':
            pytest.skip("Not supported yet")

        assert expected == list(User.objects.values('name').annotate(value=Median('visits_count')).order_by('name'))

    def test_missing_column(self):
        with pytest.raises(FieldError) as excinfo:
            User.objects.aggregate(Median('missing'))
        assert "Cannot resolve keyword 'missing' into field" in str(excinfo.value)
