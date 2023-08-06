def create_table(query, table_name, schema_name):
    query = f"""
    CREATE TABLE {schema_name}.{table_name} AS 
    (
        {query}
    ) WITH DATA
    --PRIMARY INDEX (CURVE_ID_1, CURVE_ID_2)
    NO PRIMARY INDEX
    """
    return query


def insert_into(query, table_name, schema_name):
    query = f"""
    INSERT INTO {schema_name}.{table_name}  
    {query}
    """

    return query