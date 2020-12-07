
OUTPUT = {
    "tableName": "clustering_output",
    "schema": "fund_clustering",
    "columns": [{"name": "fundNo", "type": "INTEGER"},
                {"name": "main_cluster", "type": "INTEGER"},
                {"name": "sub_cluster", "type": "INTEGER"}],
    "primaryKey": ["fundNo"],
    "description": 'fund number and cluster result'
}
