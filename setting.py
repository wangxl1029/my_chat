class MyChatRole:
    def __init__(self, role_name: str, msg_header: str = None):
        self.__role_name = role_name
        self.__msg_header = role_name if msg_header is None else msg_header

    @property
    def role_name(self):
        return self.__role_name

    @property
    def msg_header(self):
        return self.__msg_header

    def role_msg(self, msg: str, end: str = '\n'):
        return f'{self.__msg_header} : {msg}{end}'


role_sys = MyChatRole('system', 'sys')
role_user = MyChatRole('user', 'usr')
role_anonym = MyChatRole('anonym', 'nom')
