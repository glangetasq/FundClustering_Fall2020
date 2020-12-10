"""Template and Request of the ticker table"""

TEMPLATE = {
    "table_name": "ticker",
    "schema": "fund_clustering",
    "fundNo": {"type": "INT", "primary_key": True},
    "ticker": {"type": "STRING", "length": 10},
}

REQUEST = """
    SELECT *
    FROM ticker
"""
