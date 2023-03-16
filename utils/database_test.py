import re
from collections import Counter

from django.db import reset_queries, connection


def database_debug(func):
    def inner_func(request, *args, **kwargs):
        reset_queries()
        results = func(request, *args, **kwargs)
        query_info = connection.queries
        sql_list = [query["sql"] for query in query_info]
        dup_sql_list = [re.sub("[ 0-9]", "_", x) for x in sql_list]
        print('function_name: {}'.format(func.__name__))
        print('query_count: {}'.format(len(query_info)))
        print("\n".join(sql_list))
        print("\ndup queries")
        print("\n".join([x for x, y in Counter(dup_sql_list).items() if y > 1]))
        return results

    return inner_func
