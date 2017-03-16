import sys
sys.dont_write_bytecode = True
from sqlalchemy.orm import sessionmaker, scoped_session
import sqlalchemy
import pyodbc

class Connection:

    def __init__(self):

        #### Authentication Params
        self.serverUser = 'nickflorin'
        self.serverPW = 'N1cholas!'
        self.serverDB = 'portfolioAppDB'
        self.serverHost ='10.13.0.29'
        self.serverPort = 5432

        self.tranUser = 'Transparency'
        self.tranPW = 'RCGTransparency'
        self.tranDB = 'Research'
        self.tranHost ='10.13.0.25'
        self.tranPort = 1433

        self.transparency_conn = None
        return

    ####################################
    def enterTransparencySession(self):
        self.engine = pyodbc.connect('DRIVER={SQL SERVER};SERVER=10.13.0.25;UID=Transparency;PWD=RCGTransparency;TDS_Version=8.0;PORT=1433;')
        return

    ###################################
    #### Leaves Open Session
    def leaveTransparencySession(self):
        self.engine.close()
        return


##############################################################################
def local_connect(user, password, db, host='localhost', port=5432):

    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)
    print "Conncted to : ",url
    con = sqlalchemy.create_engine(url, client_encoding='utf8')

    #Bind The Connection To to MetaData()
    meta = sqlalchemy.MetaData(bind=con, reflect=True)
    return con, meta

##############################################################################
def server_connect(user, password, db, host='10.13.0.29', port=5432):

    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)
    print "Conncted to : ",url
    con = sqlalchemy.create_engine(url)
    
    #Bind The Connection To to MetaData()
    meta = sqlalchemy.MetaData(bind=con, reflect=True)
    
    return con, meta

##############################################################################
def transparency_connect():
    conn = pyodbc.connect('DRIVER={SQL SERVER};SERVER=10.13.0.25;UID=Transparency;PWD=RCGTransparency;TDS_Version=8.0;PORT=1433;')
    return conn