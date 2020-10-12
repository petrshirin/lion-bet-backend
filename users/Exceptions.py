

class UniqueUser(Exception):
    pass

    def __str__(self):
        return 'Пользователь уже существует'


