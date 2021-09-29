from django.db.models import FloatField
from django.db.models.aggregates import Aggregate
from math import floor
from statistics import median

__all__ = ['Median', 'Percentile', 'percentile']

sqlite_cache = set()


# uses C=1 variant, like percentile_cont
# https://en.wikipedia.org/wiki/Percentile#The_linear_interpolation_between_closest_ranks_method
def percentile(values, p):
    s = sorted(values)
    x = p * (len(s) - 1)
    r = x % 1
    i = floor(x)
    if i == len(s) - 1:
        return s[-1]
    else:
        return s[i] + r * (s[i + 1] - s[i])


class SQLiteHandler:
    def __init__(self):
        self.values = []
        self.percentile = None

    # TODO add checks
    def step(self, value, percentile):
        if value is None:
            return
        self.values.append(value)
        self.percentile = percentile

    def finalize(self):
        if self.percentile is None:
            return None
        elif self.percentile == 50:
            # use built-in method for performance
            return median(self.values)
        else:
            return percentile(self.values, self.percentile / 100.0)


class Percentile(Aggregate):
    name = 'Percentile'
    output_field = FloatField()

    def __init__(self, expression, percentile, **extra):
        # super important!! prevents injection
        percentile = float(percentile)

        if percentile < 0 or percentile > 1:
            raise ValueError('percentile is not between 0 and 1')

        super().__init__(expression, percentile=percentile, percentile100=percentile * 100, **extra)

    def as_sql(self, compiler, connection):
        vendor = connection.vendor
        if vendor == 'sqlite':
            self.function = 'PERCENTILE'
            self.template = '%(function)s(%(expressions)s, %(percentile100)s)'

            # TODO check if extension function exists
            if not id(connection) in sqlite_cache:
                with connection.cursor() as cursor:
                    cursor.connection.create_aggregate('percentile', 2, SQLiteHandler)
                    sqlite_cache.add(id(connection))

        elif vendor == 'postgresql':
            self.function = 'PERCENTILE_CONT'
            self.template = '%(function)s(%(percentile)s) WITHIN GROUP (ORDER BY %(expressions)s)'
        elif vendor == 'mysql':
            if connection.mysql_is_mariadb:
                # TODO support OVER (PARTITION BY ...)
                self.function = 'PERCENTILE_CONT'
                self.template = '%(function)s(%(percentile)s) WITHIN GROUP (ORDER BY %(expressions)s) OVER ()'
            else:
                self.function = 'PERCENTILE_CONT'
                self.template = '%(function)s(%(expressions)s, %(percentile)s)'
        elif vendor == 'microsoft':
            # TODO support OVER (PARTITION BY ...)
            self.function = 'PERCENTILE_CONT'
            self.template = '%(function)s(%(percentile)s) WITHIN GROUP (ORDER BY %(expressions)s) OVER ()'
        else:
            raise RuntimeError(f'Unsupported vendor: {vendor}')
        return super().as_sql(compiler, connection)


class Median(Percentile):
    name = 'Median'

    def __init__(self, expression, **extra):
        super().__init__(expression, percentile=.50, **extra)
