"""Configuration such as HOST, PORT, etc."""
from sqlalchemy import (BIGINT,
                        BINARY,
                        BLOB,
                        BigInteger,
                        Boolean,
                        CHAR,
                        CLOB,
                        DECIMAL,
                        Date,
                        DateTime,
                        Float,
                        INT,
                        Integer,
                        Interval,
                        LargeBinary,
                        NCHAR,
                        NVARCHAR,
                        Numeric,
                        REAL,
                        SMALLINT,
                        SmallInteger,
                        String,
                        TIMESTAMP,
                        Text,
                        Time,
                        Unicode,
                        VARBINARY,
                        VARCHAR)
HOST = 'localhost'
SECRETS_FILE = '.saumapass'
WINDOWS = 'Windows'
DB_META = 'mysql+pymysql'
PRIMARY_KEY = 'primary_key'

TYPE_MAPPER = {'bigint': BIGINT,
               'binary': BINARY,
               'blob': BLOB,
               'boolean': Boolean,
               'biginteger': BigInteger,
               'char': CHAR,
               'clob': CLOB,
               'date': Date,
               'datetime': DateTime,
               'decimal': DECIMAL,
               'float': Float,
               'int': INT,
               'integer': Integer,
               'interval': Interval,
               'largebinary': LargeBinary,
               'nchar': NCHAR,
               'nvarchar': NVARCHAR,
               'numeric': Numeric,
               'real': REAL,
               'smallint': SMALLINT,
               'smallinteger': SmallInteger,
               'string': String,
               'text': Text,
               'time': Time,
               'timestamp': TIMESTAMP,
               'unicode': Unicode,
               'varbinary': VARBINARY,
               'varchar': VARCHAR}

SAUMA_KEYWORDS = [
    "schema",
    "table_name"
]
