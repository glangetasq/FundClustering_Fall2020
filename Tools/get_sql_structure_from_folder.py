"""
From a path, get the structure of the SQL, the databases and their respective tables

- SQL/Structure
    - DataBase A
        - tableA1.py -> template and request
        - tableA2.py -> template and request
        - tableA3.py -> template and request
    - DataBase B
        - tableB1.py -> template and request
"""

import glob
import importlib.util
import os


def get_sql_structure_from_folder(structure_path):

    # Get all the databases from the path, i.e. the directories inside structure_path
    databases = glob.glob(os.path.join(structure_path, '*'))
    databases = [ os.path.basename(dir) for dir in databases if os.path.isdir(dir) ]

    structure = dict()

    for db in databases:

        structure[db] = dict()

        # Get all the tables from structure_path/db/
        tables = glob.glob(os.path.join(structure_path, db, '*.py'))
        tables = [ tbl for tbl in tables if os.path.isfile(tbl) and not tbl.endswith('__init__.py') ]

        for tbl in tables:

            table_name = os.path.basename(tbl)[:-3]

            # Load the file using importlib.util
            spec = importlib.util.spec_from_file_location("module.name", tbl)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            structure[db][table_name] = dict()
            structure[db][table_name]['template'] = module.TEMPLATE
            structure[db][table_name]['request'] = module.REQUEST


    return structure
