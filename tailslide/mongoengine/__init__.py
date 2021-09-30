from mongoengine.queryset import QuerySet

__all__ = ['TailslideQuerySet']


class TailslideQuerySet(QuerySet):
    def median(self, field):
        return self.percentile(field, .5)

    # https://www.compose.com/articles/mongo-metrics-finding-a-happy-median/
    def percentile(self, field, percentile):
        percentile = float(percentile)

        if percentile < 0 or percentile > 1:
            raise ValueError('percentile is not between 0 and 1')

        db_field = self._fields_to_dbfields([field]).pop()
        pipeline = [
            {'$match': self._query},
            {'$match': {db_field: {'$ne': None}}},
            {'$sort': {db_field: 1}},
            {'$group': {'_id': None, 'values': {'$push': '$' + db_field}, 'count': {'$sum': 1}}},
            {'$project': {'values': 1, 'count': {'$subtract': ['$count', 1]}}},
            {'$project': {'values': 1, 'count': 1, 'x': {'$multiply': ['$count', percentile]}}},
            {'$project': {'values': 1, 'count': 1, 'r': {'$mod': ['$x', 1]}, 'i': {'$floor': '$x'}}},
            {'$project': {'values': 1, 'count': 1, 'r': 1, 'i': 1, 'i2': {'$add': ['$i', 1]}}},
            {'$project': {'values': 1, 'count': 1, 'r': 1, 'i': 1, 'i2': {'$min': ['$i2', '$count']}}},
            {'$project': {'r': 1, 'beginValue': {'$arrayElemAt': ['$values', '$i']}, 'endValue': {'$arrayElemAt': ['$values', '$i2']}}},
            {'$project': {'r': 1, 'beginValue': 1, 'result': {'$subtract': ['$endValue', '$beginValue']}}},
            {'$project': {'beginValue': 1, 'result': {'$multiply': ['$result', '$r']}}},
            {'$project': {'result': {'$add': ['$beginValue', '$result']}}}
        ]

        result = tuple(self._document._get_collection().aggregate(pipeline))
        return result[0]['result'] if result else None
