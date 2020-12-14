"""Template and Request of the first_layer_cluster_labels table"""

TEMPLATE = {
    "table_name": "firstlayer_cluster_labels",
    "schema": "fund_clustering",
    "columns": [
        {"name": "Fund.No", "type": "INTEGER"},
        {"name": "Ticker", "type": "STRING", "size": 10},
        {"name": "Cluster", "type": "INTEGER"},
        {"name": "Cash", "type": "FLOAT"},
        {"name": "Equity", "type": "FLOAT"},
        {"name": "Bond", "type": "FLOAT"},
        {"name": "Security", "type": "FLOAT"},
        {"name": "Mstar Category", "type": "STRING", "size": 53},
        {"name": "Cluster Category", "type": "STRING", "size": 50},
        {"name": "sharpe_ratio", "type": "STRING", "size": 50},
        {"name": "absolute_return", "type": "STRING", "size": 10},
        {"name": "absolute_return_val", "type": "FLOAT"}
    ],
    "primaryKey": ["Fund.No"],
    "description": 'Main cluster results'
}

REQUEST = 'lmao'
