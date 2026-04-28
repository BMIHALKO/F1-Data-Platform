from psycopg2.extras import execute_values

from ingestion.load.postgres_connector import get_postgres_connection


def load_dataframe_to_table(df, schema_name: str, table_name: str) -> int:
    """
    Load a pandas DataFrame into a PostgreSQL table.
    """
    if df.empty:
        return 0

    columns = list(df.columns)
    column_names = ", ".join(columns)
    values_template = "(" + ", ".join(["%s"] * len(columns)) + ")"

    df = df.astype(object).where(df.notna(), None)
    rows = [tuple(row) for row in df.itertuples(index=False, name=None)]

    insert_sql = f"""
        INSERT INTO {schema_name}.{table_name} ({column_names})
        VALUES %s
        ON CONFLICT DO NOTHING
    """

    conn = get_postgres_connection()

    try:
        with conn:
            with conn.cursor() as cur:
                execute_values(cur, insert_sql, rows, template = values_template)
                rows_inserted = cur.rowcount

        return rows_inserted

    finally:
        conn.close()