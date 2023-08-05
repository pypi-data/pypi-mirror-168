from dict_parsing import *
from dto_converter import *


def user_info_parser(d: dict):
    parse_dict(d, rename={'surname': 'last_name'})


@dataclass
class JwtDTO(QRDTO):
    access_token: str


@dto_kwargs_parser(user_info_parser)
@dataclass
class UserInfoDTO(QRDTO):
    name: str
    id: int
