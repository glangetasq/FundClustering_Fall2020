
class SQLHandlerMixin:
    """Mixin class that you would include in the inheritance hierarchy to migarte all possible operation to SQL
    so as to speed up calculation, you would need to integrate the sauma.core package and utilize the connection obj here"""
    
    def setup_connection(self, username, password):
        """initilize the connection obj here, and use it for any operation"""
 #       self.conn = Connection(username = username, password = password, schema = '')
        pass
    
    def setup_table_template(self):
        """define the table template as local variable in this method for all derived class, and utilize this method to setup tables"""
        raise NotImplementedError("Derived Class need to implement this method")
    
    def check_table_exist_or_not(self, schemas, table_name):
        """Please define this method to check whether a table under certain schemas exist or not"""
        pass

    def look_up_or_create_table(self, template, custom_table_name=None, custom_schemas_name=None):
        """Please define this method to create a table based on the template if a table does not exist, do nothing if table already exist,
        you may want to use self.check_table_exist_or_not here, if custom_table_name is none, you should be able to find it in template"""
        pass
    
    def drop_table(self, schemas, table_name):
        pass
    
    def chunks_update_table(self, schema, table_name, dataframe, **kwargs):
        """when you have a large dataframe, it mays takes a long time to update the sql table if you upload it at once, you could actually
        divide the table into smaller chunks and upload them piece by piece to speed up the process, as it is more memory efficient and use less cpu,
        try to implement this method here too"""
        pass
