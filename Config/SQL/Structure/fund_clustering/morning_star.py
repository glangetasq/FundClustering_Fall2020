"""Template and Request of the morningstar table"""

import pandas as pd


# Local imports
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


### FORMATTING ###

_IDENTITY = lambda col : col
_DATE_FROM_NUMERIC = lambda col : pd.to_datetime(col, format='%Y%m%d')
def _BOOL_FROM_STR(t, f):
    formatting = {
        t : True,
        f : False,
    }

    return lambda col : col.apply(lambda s : formatting.get(s, None))

FORMATTING = {
    'crsp_fundno' : _IDENTITY,
    'caldt' : _DATE_FROM_NUMERIC,
    #'nav_latest' : _IDENTITY,
    #'nav_latest_dt' : _DATE_FROM_NUMERIC,
    #'tna_latest' : _IDENTITY,
    #'tna_latest_dt' : _DATE_FROM_NUMERIC,
    #'yield' : _IDENTITY,
    #'div_ytd' : _IDENTITY,
    #'cap_gains_ytd' : _IDENTITY,
    #'nav_52w_h' : _IDENTITY,
    #'nav_52w_h_dt' : _DATE_FROM_NUMERIC,
    # 'nav_52w_l' : _IDENTITY,
    # 'nav_52w_l_dt' : _DATE_FROM_NUMERIC,
    # 'unrealized_app_dep' : _IDENTITY,
    # 'unrealized_app_dt' : _DATE_FROM_NUMERIC,
    # 'asset_dt' : _DATE_FROM_NUMERIC,
    'per_com' : _IDENTITY,
    'per_pref' : _IDENTITY,
    'per_conv' : _IDENTITY,
    'per_corp' : _IDENTITY,
    'per_muni' : _IDENTITY,
    'per_govt' : _IDENTITY,
    'per_oth' : _IDENTITY,
    'per_cash' : _IDENTITY,
    'per_bond' : _IDENTITY,
    'per_abs' : _IDENTITY,
    'per_mbs' : _IDENTITY,
    'per_eq_oth' : _IDENTITY,
    'per_fi_oth' : _IDENTITY,
    # 'maturity' : _IDENTITY,
    # 'maturity_dt' : _DATE_FROM_NUMERIC,
    # 'cusip8' : _IDENTITY,
    # 'crsp_portno' : _IDENTITY,
    # 'crsp_cl_grp' : _IDENTITY,
    # 'fund_name' : _IDENTITY,
    # 'ticker' : _IDENTITY,
    # 'ncusip' : _IDENTITY,
    # 'mgmt_name' : _IDENTITY,
    # 'mgr_name' : _IDENTITY,
    # 'mgr_dt' : _DATE_FROM_NUMERIC,
    # 'adv_name' : _IDENTITY,
    # 'open_to_inv' : _BOOL_FROM_STR('Y', 'N'),
    # 'retail_fund' : _BOOL_FROM_STR('Y', 'N'),
    # 'inst_fund' : _BOOL_FROM_STR('Y', 'N'),
    # 'm_fund' : _BOOL_FROM_STR('Y', 'N'),
    # 'index_fund_flag' : _IDENTITY,
    # 'vau_fund' : _BOOL_FROM_STR('Y', 'N'),
    # 'et_flag' : _BOOL_FROM_STR('T', 'F'),
    # 'delist_cd' : _IDENTITY,
    # 'first_offer_dt' : _DATE_FROM_NUMERIC,
    # 'end_dt' : _DATE_FROM_NUMERIC,
    # 'dead_flag' : _BOOL_FROM_STR('Y', 'N'),
    # 'merge_fundno' : _IDENTITY,
    # 'actual_12b1' : _IDENTITY,
    # 'max_12b1' : _IDENTITY,
    # 'mgmt_fee' : _IDENTITY,
    # 'exp_ratio' : _IDENTITY,
    # 'turn_ratio' : _IDENTITY,
    # 'fiscal_yearend' : _DATE_FROM_NUMERIC,
    # 'crsp_obj_cd' : _IDENTITY,
    # 'si_obj_cd' : _IDENTITY,
    # 'accrual_fund' : _BOOL_FROM_STR('Y', 'N'),
    # 'sales_restrict' : _BOOL_FROM_STR('Y', 'N'),
    # 'wbrger_obj_cd' : _IDENTITY,
    # 'policy' : _IDENTITY,
    # 'lipper_class' : _IDENTITY,
    'lipper_class_name' : _IDENTITY,
    # 'lipper_obj_cd' : _IDENTITY,
    # 'lipper_obj_name' : _IDENTITY,
    # 'lipper_asset_cd' : _IDENTITY,
    # 'lipper_tax_cd' : _IDENTITY,
}
