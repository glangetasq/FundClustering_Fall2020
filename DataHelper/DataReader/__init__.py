from .DataReaderCSV import *
from .DataReaderSQL import *

_DATA_READERS = {
    'csv': DataReaderCSV,
    'sql': DataReaderSQL,
}
