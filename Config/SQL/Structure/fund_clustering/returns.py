"""Template and Request of the returns table"""

from Config import TMIN, TMAX


TEMPLATE = {
    "table_name": "returns",
    "schema": "fund_clustering",
    "columns": [
        {"name": "fundNo", "type": "INTEGER"},
        {"name": "date", "type": "DATE"},
        {"name": "r", "type": "FLOAT", "size": 53}
    ],
    "primaryKey": ["fundNo", "date"],
    "description": 'fund returns'
}

REQUEST = f"""
    SELECT *
    FROM returns
    WHERE date >= '{TMIN}'
    AND date <= '{TMAX}'
"""
