# qr_server

This project is the extension of Flask project (https://pypi.org/project/Flask/), aimed on fast creation of web-apps with minimalistic syntax.
The solution provides support for basic HTTP-routing (with file sending), fast DTOs 
(data transfer objects for formalization and validation of response data),
simple jwt-token system, role manager (database-side rights system) and configurable logging.
See 'example' directory for a minimal working application built using this library

### Usage example:
```python
from qr_server.Server import MethodResult, QRContext
from qr_server.Config import QRYamlConfig
from qr_server.TokenManager import require_token, JwtTokenManager
from qr_server.FlaskServer import FlaskServer


def login(ctx: QRContext):
    login = ctx.json_data['login']
    password = ctx.json_data['password']
    user_id = ctx.repository.check_credentials(login, password)
    if user_id is None:
        return MethodResult('wrong credentials', 500)

    user = ctx.repository.get_user_data(user_id)
    if user is None:
        return MethodResult('account not found', 500)

    jwt_token = ctx.managers['token_manager'].make_token(user_id)
    return MethodResult(JwtDTO(jwt_token))


@require_token()
def user_info(ctx: QRContext, user_id):
    user = ctx.repository.get_user_data(user_id)
    if user is None:
        return MethodResult('account not found', 500)

    return MethodResult(UserInfoDTO(**user))


class AuthServer(FlaskServer, AuthRepository):
    """DI class"""


if __name__ == "__main__":
    config = QRYamlConfig()
    config.read_config('config.yaml')

    host = config['app']['host']
    port = config['app']['port']

    token_man = JwtTokenManager()
    token_man.load_config(config['jwt'])

    server = AuthServer()
    server.init_server(config['app'])
    if config['app']['logging']:
        server.configure_logger(config['app']['logging'])
    server.register_manager(token_man)

    server.register_method('/login', login, 'POST')
    server.register_method('/info', user_info, 'GET')
    server.run(host, port)
```
