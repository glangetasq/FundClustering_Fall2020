import os
from sauma.core import Connection

# Local imports
from .formatting import ticker_formatting, returns_formatting
from .formatting import morning_star_formatting

os.environ['SECRETS_DIR'] = '/Users/glangetasq'

username = 'fx_admin'
password = '#Flexstone2020'

c = Connection(username=username, password=password, schema='')

conn = c.connect()

# Insert ticker
def insert_ticker(c):

    ticker = ticker_formatting()

    c.update_table(table_name='ticker',
        schema='fund_clustering',
        dataframe=ticker,
        index=False,
        if_exists='append'
    )

# Insert returns
def insert_returns(c, chunk_size=100000):

    returns = returns_formatting()
    N = returns.shape[0]

    for i in range(N // chunk_size + 1):

        print(f"Inserting chunk {i+1}/{N//chunk_size + 1}")
        returns_to_insert = returns.iloc[i*N:(i+1)*N]

        c.update_table(table_name='returns',
                schema='fund_clustering',
                dataframe=returns_to_insert,
                index=True,
                if_exists='append'
        )

# Insert morningstar data
def insert_morning_star(c, chunk_size=10000):

    mrnstar = morning_star_formatting()
    N = mrnstar.shape[0]

    for i in range(N // chunk_size + 1):

        print(f"Inserting chunk {i+1}/{N//chunk_size + 1}")
        mrnstar_to_insert = mrnstar.iloc[i*N:(i+1)*N]

        c.update_table(table_name='morning_star',
                schema='fund_clustering',
                dataframe=mrnstar_to_insert,
                index=False, 
                if_exists='append'
        )
