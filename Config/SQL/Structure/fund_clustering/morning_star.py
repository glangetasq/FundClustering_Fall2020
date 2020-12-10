"""Template and Request of the morningstar table"""

from Config import TMIN, TMAX


TEMPLATE = {
    "tableName": "morning_star",
    "schema": "fund_clustering",
    "columns": [
        {"name": "fundNo", "type": "INTEGER"},
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
        {"name": "lipper_class_name", "type": "STRING", "size": 50}
    ],
    "primaryKey": ["fundNo", "date"],
    "description": 'morningstar data for each fund'
}


REQUEST = f"""
    SELECT
        fundNo,
        date,
        per_cash as cash,
        per_com + per_pref + per_eq_oth as equity,
        per_conv + per_corp + per_muni + per_govt as bond,
        per_abs + per_mbs + per_fi_oth + per_oth as sec,
        lipper_class_name
    FROM morning_star
    WHERE
        date >= '{TMIN}'
    AND date <= '{TMAX}'
"""
