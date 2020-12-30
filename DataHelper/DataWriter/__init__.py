from .DataWriterCSV import *
from .DataWriterSQL import *

_DATA_WRITERS = {
    'csv': DataWriterCSV,
    'sql': DataWriterSQL,
}
