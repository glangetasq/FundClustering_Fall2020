"""Template and Request of the clustering_output table"""

TEMPLATE = {
    "table_name": "clustering_output",
    "schema": "fund_clustering",
    "fundNo": {"type": "INT", "primary_key": True},
    "main_cluster": {"type": "INT"},
    "sub_cluster": {"type": "INT"},
}

REQUEST = 'lmao'
