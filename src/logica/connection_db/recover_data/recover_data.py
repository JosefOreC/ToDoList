
class RecoverData:
    @staticmethod
    def constructor_query_select_simple(table: str, atributs: list):
        query = """SELECT """
        for atribut in atributs:
            query += atribut
            if atributs.index(atribut) != len(atributs) - 1:
                query += ', '

        return query + f" FROM {table}"

    @staticmethod
    def add_limit(query, limit: int):

        return query + f" LIMIT {limit}"

    @staticmethod
    def add_where(query, conditions):
        return query + " WHERE " + conditions

    @staticmethod
    def add_order_by(query, order_by: str):
        return query + f" ORDER BY {order_by}"

    @staticmethod
    def constructor_query(table: str, atributs: list, where: str=None, order_by: str = None, limit: int=None):
        query = RecoverData.constructor_query_select_simple(table, atributs)
        if where:
            query = RecoverData.add_where(query, where)
        if order_by:
            query = RecoverData.add_order_by(query, where)
        if limit:
            query = RecoverData.add_limit(query, limit)

        return query
