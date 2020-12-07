""" test core"""

import os
import unittest
import json
import pandas as pd
import unittest.mock as mock
from sauma.config import HOST, SECRETS_FILE
from sauma.core import Connection
from sqlalchemy import create_engine

class TestConnection(unittest.TestCase):
    """
    Test the core.Connection() method
    """
    def setUp(self):
        """
        Setup the fixtures for testing
        """
        local = os.getenv('LOCAL', 'false').lower() == 'true'
        if local:
            self.fakeobj = Connection()
        else:
            fakeuser = "fakeuser"
            fakepassword = "fakepassword"
            fakedatabase = "fakedatabase"
            self.fakeobj = Connection(fakeuser, fakepassword, fakedatabase)

    @mock.patch('sauma.core.Connection.connect')
    def test_connect_without_secrets_file(self, mock_connection):
        """
        Test that the user can connect with username prompted or loaded from
        a secrets file
        """
        fakeuser = "fakeuser"
        fakepassword = "fakepassword"
        fakedatabase = "fakedatabase"
        fakeobj = Connection(fakeuser, fakepassword, fakedatabase)
        fakeobj.connect()
        mock_connection.assert_called_once()

    @mock.patch('sauma.core.Connection.connect')
    def test_connect_with_secrets_file(self, mock_connection):
        """
        Test that the user is able to login using a secrets file
        """
        local = os.getenv('LOCAL', 'false').lower() == 'true'
        if local:
            fakeobj = Connection()
        else:
            fakeuser = "fakeuser"
            fakepassword = "fakepassword"
            fakedatabase = "fakedatabase"
            fakeobj = Connection(fakeuser, fakepassword, fakedatabase)

        fakeobj.connect()
        mock_connection.assert_called_once()

    @mock.patch('sauma.core.Connection.show_schemas')
    def test_show_schemas(self, mock_connection):
        """Test the show schemas method"""
        self.fakeobj.show_schemas()
        mock_connection.assert_called_once()

    @mock.patch('sauma.core.Connection.show_tables')
    def test_show_tables(self, mock_method):
        """Test the show tables method"""
        fakeschema = 'fakeschema'
        self.fakeobj.show_tables(fakeschema)
        mock_method.assert_called_once()

    @mock.patch('sauma.core.Connection.get_table')
    def test_get_table_default_schema(self, mock_method):
        """Test the get_table method"""
        faketable = "faketable"
        self.fakeobj.get_table(faketable)
        mock_method.assert_called_once()

    @mock.patch('sauma.core.Connection.get_table')
    def test_get_table_with_schema(self, mock_method):
        """Test the get_table method with schema"""
        fakedatabase = "fakedatabase"
        faketable = "faketable"
        self.fakeobj.get_table(faketable, fakedatabase)
        mock_method.assert_called_once()

    @mock.patch('sauma.core.Connection.execute')
    def test_execute(self, mock_method):
        """Test the execution of raw SQL select statements"""
        fakequery = "SELECT * FROM faketable"
        self.fakeobj.execute(fakequery)
        mock_method.assert_called_once()

    @mock.patch('sauma.core.Connection.create_table')
    def test_create_table(self, mock_method):
        """Test the create table method"""
        json_object = {"id": {
                            "type":"INT",
                            "primary_key":True
                            },
                       "var":{
                           "type":"INT"
                            },
                       "val":{
                            "type":"INT"
                            },
                       "table_name": "test", "schema":"morning_star"}
        fakejson = json.dumps(json_object)
        self.fakeobj.create_table(fakejson)
        mock_method.assert_called_once()

    @mock.patch('sauma.core.Connection.update_table')
    def test_update_table_default_schema(self, mock_method):
        """Test the update table method with default schema"""
        fakedict = {
            'id': [1, 2, 3],
            'var': ['first', 'second', 'third'],
            'val': [5.0, 5.0, 5.0]
        }
        fakedf = pd.DataFrame(fakedict)
        faketable = "faketable"
        self.fakeobj.update_table(faketable, fakedf)
        mock_method.assert_called_once()

    @mock.patch('sauma.core.Connection.update_table')
    def test_update_table_with_schema(self, mock_method):
        """Test the update table with a schema provided"""
        fakedict = {
            'id': [1, 2, 3],
            'var': ['first', 'second', 'third'],
            'val': [5.0, 5.0, 5.0]
        }
        fakedf = pd.DataFrame(fakedict)
        faketable = "faketable"
        fakedatabase = "fakedatabase"
        self.fakeobj.update_table(faketable, fakedf, fakedatabase)
        mock_method.assert_called_once()

    @mock.patch('sauma.core.Connection.update_table')
    def test_update_table_ifexist_fail(self, mock_method):
        """Test that the update table method should fail if it already exists in the schema """
        fakedict = {
            'id': [1, 2, 3],
            'var': ['first', 'second', 'third'],
            'val': [5.0, 5.0, 5.0]
        }
        fakedf = pd.DataFrame(fakedict)
        faketable = "faketable"
        action = "fail"
        self.fakeobj.update_table(faketable, fakedf, ifexists=action)
        mock_method.assert_called_once()

    @mock.patch('sauma.core.Connection.update_table')
    def test_update_table_ifexist_replace(self, mock_method):
        """Test that the update table method replaces the existing table"""
        fakedict = {
            'id': [1, 2, 3],
            'var': ['first', 'second', 'third'],
            'val': [5.0, 5.0, 5.0]
        }
        fakedf = pd.DataFrame(fakedict)
        faketable = "faketable"
        action = "replace"
        self.fakeobj.update_table(faketable, fakedf, ifexists=action)
        mock_method.assert_called_once()

    @mock.patch('sauma.core.Connection.update_table')
    def test_update_table_ifexist_append(self, mock_method):
        """Test that the update table method appends to the existing table"""
        fakedict = {
            'id': [1, 2, 3],
            'var': ['first', 'second', 'third'],
            'val': [5.0, 5.0, 5.0]
        }
        fakedf = pd.DataFrame(fakedict)
        faketable = "faketable"
        action = "append"
        self.fakeobj.update_table(faketable, fakedf, ifexists=action)
        mock_method.assert_called_once()

    @mock.patch('sauma.core.Connection.close')
    def test_close(self, mock_method):
        """Test the close method"""
        self.fakeobj.close()
        mock_method.assert_called_once()

    @mock.patch('sauma.core.Connection.get_dataframe')
    def test_get_dataframe(self, mock_method):
        """Test the get_dataframe method"""
        faketable = "faketable"
        fakeschema = "fakeschema"
        self.fakeobj.get_dataframe(faketable, fakeschema)
        mock_method.assert_called_once()

    @mock.patch('sauma.core.Connection.get_dataframe_from_sql_query')
    def test_get_dataframe_from_sql_query(self, mock_method):
        """Test the get_dataframe_from_sql_query method"""
        fakesql = "SELECT * FROM fakeschema.faketable LIMIT 5"
        self.fakeobj.get_dataframe_from_sql_query(fakesql)
        mock_method.assert_called_once()
