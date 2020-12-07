
''' Customized table templates for SQL databases '''

TEMPLATE_TICKER = {
    "tableName": "ticker",
    "schema": "fund_clustering",
    "columns": [{"name": "fundNo", "type": "INTEGER"},
                {"name": "fundTicker", "type": "STRING", "size": 10}],
    "primaryKey": ["fundNo"],
    "description": 'fund number and ticker'
}

TEMPLATE_RETURNS = {
    "tableName": "returns",
    "schema": "fund_clustering",
    "columns": [{"name": "fundNo", "type": "INTEGER"},
                {"name": "date", "type": "DATE"},
                {"name": "r", "type": "FLOAT", "size": 53}],
    "primaryKey": ["fundNo", "date"],
    "description": 'fund returns'
}

TEMPLATE_MORNINGSTAR = {
    "tableName": "morning_star",
    "schema": "fund_clustering",
    "columns": [{"name": "fundNo", "type": "INTEGER"},
                {"name": "date", "type": "DATE"},
                {"name": "per_com", "type": "FLOAT", "size": 53},
                {"name": "per_pref", "type": "FLOAT", "size": 53},
                {"name": "per_conv", "type": "FLOAT", "size": 53},
                {"name": "per_corp", "type": "FLOAT", "size": 53},
                {"name": "per_muni", "type": "FLOAT", "size": 53},
                {"name": "per_govt", "type": "FLOAT", "size": 53},
                {"name": "per_oth", "type": "FLOAT", "size": 53},
                {"name": "per_cash", "type": "FLOAT", "size": 53},
                {"name": "per_bond", "type": "FLOAT", "size": 53},
                {"name": "per_abs", "type": "FLOAT", "size": 53},
                {"name": "per_mbs", "type": "FLOAT", "size": 53},
                {"name": "per_eq_oth", "type": "FLOAT", "size": 53},
                {"name": "per_fi_oth", "type": "FLOAT", "size": 53},
                {"name": "lipper_class_name", "type": "STRING", "size": 50}],
    "primaryKey": ["fundNo", "date"],
    "description": 'morningstar data for each fund'
}

TEMPLATE_OUTPUT = {
    "tableName": "clustering_output",
    "schema": "fund_clustering",
    "columns": [{"name": "fundNo", "type": "INTEGER"},
                {"name": "main_cluster", "type": "INTEGER"},
                {"name": "sub_cluster", "type": "INTEGER"}],
    "primaryKey": ["fundNo"],
    "description": 'fund number and cluster result'
}

TEMPLATE_FIRST_LAYER_LABELS = {
            "tableName": "firstlayer_cluster_labels",
            "schema": "fund_clustering",
            "columns": [{"name": "Fund.No", "type": "INTEGER"},
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
                        {"name": "absolute_return_val", "type": "FLOAT"}],                      
            "primaryKey": ["Fund.No"],
            "description": 'Main cluster results'
        }
