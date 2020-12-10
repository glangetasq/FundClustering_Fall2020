
import os

# Local imports
from Tools.get_sql_structure_from_folder import get_sql_structure_from_folder

STRUCTURE = get_sql_structure_from_folder(
    os.path.join('Config', 'SQL', 'Structure')
)
