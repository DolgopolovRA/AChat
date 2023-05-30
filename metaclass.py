import dis


class ClientVerifier(type):

    def __init__(self, clsname, bases, clsdict):
        methods = []
        for el in clsdict:
            try:
                qwe = dis.get_instructions(clsdict[el])
            except:
                pass
            else:
                for i in qwe:
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            methods.append(i.argval)
        if 'accept' in methods or 'listen' in methods or 'socket' in methods:
            raise TypeError('Использование недопустимых методов')


class ServerVerifier(type):

    def __init__(self, clsname, bases, clsdict):
        methods = []
        for el in clsdict:
            try:
                qwe = dis.get_instructions(clsdict[el])
            except:
                pass
            else:
                for i in qwe:
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            methods.append(i.argval)
        if 'connect' in methods:
            raise TypeError('Использование метода connect недопустимо в классе сервера')
        if not ('SOCK_STREAM' in methods and 'AF_INET' in methods):
            raise TypeError('Некорректная инициализация сокета.')
