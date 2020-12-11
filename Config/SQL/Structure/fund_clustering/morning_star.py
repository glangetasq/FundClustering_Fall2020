"""Template and Request of the morningstar table"""

from Config import TMIN, TMAX


TEMPLATE = {
    "table_name": "morning_star",
    "schema": "fund_clustering",
    # columns
    "fundNo": {"type": "INT", "primary_key": True},
    "date": {"type": "DATE", "primary_key": True},
    "per_com": {"type": "FLOAT"},
    "per_pref": {"type": "FLOAT"},
    "per_conv": {"type": "FLOAT"},
    "per_corp": {"type": "FLOAT"},
    "per_muni": {"type": "FLOAT"},
    "per_govt": {"type": "FLOAT"},
    "per_oth": {"type": "FLOAT"},
    "per_cash": {"type": "FLOAT"},
    "per_bond": {"type": "FLOAT"},
    "per_abs": {"type": "FLOAT"},
    "per_mbs": {"type": "FLOAT"},
    "per_eq_oth": {"type": "FLOAT"},
    "per_fi_oth": {"type": "FLOAT"},
    "lipper_class_name": {"type": "STRING", "length": 50}
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
