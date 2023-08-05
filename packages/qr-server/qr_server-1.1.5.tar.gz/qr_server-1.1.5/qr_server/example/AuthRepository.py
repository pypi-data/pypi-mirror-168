import Repository as rep

users = [('user1', 'pass1'), ('user2', 'pass2')]


class AuthRepository(rep.IQRRepository):
    def __init__(self):
        super().__init__()

    def connect_repository(self, configuration):
        pass

    def set_role(self, role: str):
        pass

    def check_credentials(self, login, password):
        for i, u in enumerate(users):
            if u == (login, password):
                return i
        return None

    def get_user_data(self, user_id):
        if user_id < len(users):
            data = users[user_id]
            return {'name': data[0], 'id': user_id}
        return None