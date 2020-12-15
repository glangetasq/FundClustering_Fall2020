from .Classic import *


_DATA_CATCHERS = {
    ('classic', 'csv'): ClassicDataCatcherCSV,
    ('classic', 'sql'): ClassicDataCatcherSQL,
}
