"""Template and Request of the ticker table"""

TEMPLATE = {
    "tableName": "ticker",
    "schema": "fund_clustering",
    "columns": [
        {"name": "fundNo", "type": "INTEGER"},
        {"name": "fundTicker", "type": "STRING", "size": 10}
    ],
    "primaryKey": ["fundNo"],
    "description": 'fund number and ticker'
}

REQUEST = 'lmao'
