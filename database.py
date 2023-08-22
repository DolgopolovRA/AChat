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

    class ActiveClients:
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
                               Column('ip', String(50)),
                               )
        active_clients = Table('active_clients', self.metadata,
                               Column('id', Integer, primary_key=True),
                               Column('name', ForeignKey('clients.id'), unique=True),
                               Column('date_time', DateTime),
                               Column('ip', String(50)),
                               )

        self.metadata.create_all(self.engine)

        mapper_registry.map_imperatively(self.Clients, clients_table)
        mapper_registry.map_imperatively(self.ClientHistory, client_history)
        mapper_registry.map_imperatively(self.ActiveClients, active_clients)

        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.session.query(self.ActiveClients).delete()
        print('очистка бд клиентов')
        self.session.commit()

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

        active_client = self.ActiveClients(user.id, datetime.now(), ip)
        self.session.add(active_client)
        self.session.commit()

    def del_active_users(self, login):
        user = self.session.query(self.Clients).filter_by(name=login).first()
        user_del = self.session.query(self.ActiveClients).filter_by(name=user.id).first()
        if user_del:
            self.session.delete(user_del)
            self.session.commit()


class ClientDb:
    class Contacts:
        def __init__(self, login):
            self.name = login
            self.id = None

    class MessageHistory:
        def __init__(self, name, msg, date):
            self.id = None
            self.name = name
            self.msg = msg
            self.date_time = date

    def __init__(self):
        self.engine = create_engine('sqlite:///client_db.db3', echo=False, pool_recycle=7200)

        self.metadata = MetaData()

        mapper_registry = registry()

        contacts_table = Table('contacts', self.metadata,
                               Column('id', Integer, primary_key=True),
                               Column('name', String(50), unique=True),
                               )

        message_history = Table('message_history', self.metadata,
                                Column('id', Integer, primary_key=True),
                                Column('name', ForeignKey('contacts.id')),
                                Column('msg', String()),
                                Column('date_time', DateTime)
                                )

        self.metadata.create_all(self.engine)

        mapper_registry.map_imperatively(self.Contacts, contacts_table)
        mapper_registry.map_imperatively(self.MessageHistory, message_history)

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def init_contacts_list(self, lst_contacts, lg):
        lst = lst_contacts.strip('[]').split(',')
        for login in lst:
            login = login.strip(" '")
            if login == lg:
                continue
            user = self.session.query(self.Contacts).filter_by(name=login).first()
            if not user:
                user = self.Contacts(login)
                self.session.add(user)
        self.session.commit()

    def add_to_message_history(self, message):
        login, msg = message.split(':')
        user = self.session.query(self.Contacts).filter_by(name=login).first()
        if not user:
            user = self.Contacts(login)
            self.session.add(user)
            self.session.commit()
        msg_h = self.MessageHistory(user.id, msg, datetime.now())
        self.session.add(msg_h)
        self.session.commit()
