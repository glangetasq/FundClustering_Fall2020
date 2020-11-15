import os
from sauma.core import Connection

os.environ['SECRETS_DIR'] = '/Users/glangetasq'

username = 'fx_admin'
password = '#Flexstone2020'

c = Connection(username=username, password=password, schema='')

conn = c.connect()

# Create data bases
sql = "CREATE DATABASE IF NOT EXISTS fund_clustering"
c.execute(sql)
c.execute("USE fund_clustering")

sql = """CREATE TABLE IF NOT EXISTS ticker (
    fundNo int,
    fundTicker varchar(10),
    PRIMARY KEY (fundNo)
);"""

c.execute(sql)



# Add ticker

"""
Note:
    ticker is a simple table that needs to be initialized with the dict from DataReader.get_fundno_ticker()
"""

sql = """CREATE TABLE IF NOT EXISTS returns (
    fundNo int,
    date date,
    r float(53),
    PRIMARY KEY (fundNo, date)
);"""
c.execute(sql)


"""
Note:
    returns is a table that needs to be initialized using the dataframe from DataReader.get_returns().
    /!\ However, the dataframe has the date in index and fund in column and we need a dataframe with fundNo and date in index to fit in the sql format
"""

sql = """CREATE TABLE IF NOT EXISTS morning_star (
    fundNo int,
    date date,
    per_com float(53),
    per_pref float(53),
    per_conv float(53),
    per_corp float(53),
    per_muni float(53),
    per_govt float(53),
    per_oth float(53),
    per_cash float(53),
    per_bond float(53),
    per_abs float(53),
    per_mbs float(53),
    per_eq_oth float(53),
    per_fi_oth float(53),
    lipper_class_name varchar(50),
    PRIMARY KEY (fundNo, date)
);
"""
c.execute(sql)
