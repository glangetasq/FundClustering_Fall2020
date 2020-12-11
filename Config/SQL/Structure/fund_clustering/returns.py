"""Template and Request of the returns table"""

from Config import TMIN, TMAX


TEMPLATE = {
    "table_name": "returns",
    "schema": "fund_clustering",
    "fundNo": {"type": "INTEGER", 'primary_key': True},
    "date": {"type": "DATE", 'primary_key': True},
    "r": {"type": "FLOAT"},
}

REQUEST = f"""
    SELECT *
    FROM returns
    WHERE date >= '{TMIN}'
    AND date <= '{TMAX}'
"""
