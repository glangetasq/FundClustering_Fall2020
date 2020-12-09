"""Template and Request of the returns table"""

TEMPLATE = {
    "tableName": "returns",
    "schema": "fund_clustering",
    "columns": [
        {"name": "fundNo", "type": "INTEGER"},
        {"name": "date", "type": "DATE"},
        {"name": "r", "type": "FLOAT", "size": 53}
    ],
    "primaryKey": ["fundNo", "date"],
    "description": 'fund returns'
}

REQUEST = 'lmao'
