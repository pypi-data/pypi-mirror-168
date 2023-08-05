class Auth(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Auth, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Authentication(metaclass=Auth):
    token = None

    def init(self, token):
        self.token = token
