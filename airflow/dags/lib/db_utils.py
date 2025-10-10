from airflow.providers.postgres.hooks.postgres import PostgresHook

def insert_ingestion_stats(filename, total, valid, invalid, criticality, error_counts_json):
    hook = PostgresHook(postgres_conn_id="postgres_app")
    hook.run(
        '''
        INSERT INTO ingestion_stats(filename, total_rows, valid_rows, invalid_rows, criticality, error_counts)
        VALUES (%s,%s,%s,%s,%s,%s)
        ''',
        parameters=(filename, total, valid, invalid, criticality, error_counts_json)
    )

def mark_processed(filename):
    hook = PostgresHook(postgres_conn_id="postgres_app")
    hook.run(
        "INSERT INTO processed_files(filename) VALUES (%s) ON CONFLICT DO NOTHING",
        parameters=(filename,),
    )

def unprocessed_good_files(good_files):
    hook = PostgresHook(postgres_conn_id="postgres_app")
    rows = hook.get_records("SELECT filename FROM processed_files")
    seen = {r[0] for r in rows}
    return [f for f in good_files if f not in seen]
