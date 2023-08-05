from abc import abstractmethod, abstractproperty
from .Config import *
from qrookDB.DB import DB

class IQRRepository:
    """abstract class representing the Repository object - one providing data-managing functions"""
    @abstractmethod
    def connect_repository(self, configuration: IQRConfig):
        """initialize repository with configuration given"""

    @abstractmethod
    def set_role(self, role: str):
        """set database role for the request"""

class QRRepository(IQRRepository):
    def __init__(self):
        self.db = None

    def connect_repository(self, config: IQRConfig):
        conn = [config['connector'],
                config['dbname'],
                config['username'],
                config['password'],
                config['host'],
                config['port']
                ]
        self.db = DB(*conn, format_type='dict')
        self.db.create_data()
        if config['logging']:
            lg = config['logging']
            fl = config['level'] if lg['file_level'] is None else lg['file_level']
            fl = fl.upper()
            self.db.create_logger(lg['logger_name'], lg['app_name'], lg['level'].upper(), lg['file'], fl)

    def set_role(self, role: str = 'guest'):
        if not role.isidentifier():
            raise Exception('set_role method got not an identifier!')
        request = self.db.exec('set role "%s"' % role)
        request.exec()
        if request.get_error() != None:
            raise Exception('failed to set role: ', request.get_error())