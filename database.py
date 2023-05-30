from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import registry, sessionmaker


class ServerDb:

    class Clients:
        def __init__(self, login):
            self.name = login
            self.last_login = datetime.now()
            self.id = None

    class ClientHistory:
        def __init__(self, name, date, ip):
            self.id = None
            self.name = name
            self.date_time = date
            self.ip = ip

    def __init__(self):
        self.engine = create_engine('sqlite:///server_db.db3', echo=False, pool_recycle=7200)

        self.metadata = MetaData()

        mapper_registry = registry()

        clients_table = Table('clients', self.metadata,
                              Column('id', Integer, primary_key=True),
                              Column('name', String(50), unique=True),
                              Column('last_login', DateTime)
                              )

        client_history = Table('login_history', self.metadata,
                               Column('id', Integer, primary_key=True),
                               Column('name', ForeignKey('clients.id')),
                               Column('date_time', DateTime),
                               Column('ip', String),
                               )

        self.metadata.create_all(self.engine)

        mapper_registry.map_imperatively(self.Clients, clients_table)
        mapper_registry.map_imperatively(self.ClientHistory, client_history)

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def login(self, login, ip):
        user = self.session.query(self.Clients).filter_by(name=login).first()
        if user:
            user.last_login = datetime.now()
        else:
            user = self.Clients(login)
            self.session.add(user)
            self.session.commit()

        history = self.ClientHistory(user.id, datetime.now(), ip)
        self.session.add(history)
        self.session.commit()

