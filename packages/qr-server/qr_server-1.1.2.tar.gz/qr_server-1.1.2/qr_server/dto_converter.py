from abc import abstractmethod
from typing import List

from dataclasses import dataclass

class QRDTO:
    @abstractmethod
    def to_dict(self):
        return self.__dict__.copy()


def OneOfQRDTO(*variants):
    class OneOfDTO:
        __variants = variants
        def __init__(self, *args, **kwargs):
            self.obj = None

            for variant in self.__variants:
                try:
                    self.obj = variant(*args, **kwargs)
                    break
                except Exception as e:
                    continue
            if self.obj is None:
                raise Exception('OneOfDTO: no variants fit the data!')

        def to_dict(self):
            return self.obj.to_dict()
    return OneOfDTO


def ArrayQRDTO(objects_type):
    class ArrayDTO(QRDTO):
        def __init__(self, data: list):
            self.data = data
            for i in range(len(data)):
                if isinstance(data[i], dict):
                    self.data[i] = objects_type(**data[i])
                else:
                    self.data[i] = objects_type(data[i])

        def to_dict(self):
            res = self.data.copy()
            for i in range(len(res)):
                res[i] = res[i].to_dict()
            return res
    return ArrayDTO

@dataclass
class DefaultResponseDTO(QRDTO):
    response: str = 'ok'

    def to_dict(self):
        return self.response


def convert_fields(data: dict):
    def wrapper(dto_class: QRDTO):
        init = dto_class.__init__

        def __init__(self, *args, **kwargs):
            init(self, *args, **kwargs)
            for k, v in data.items():
                as_list = False
                if k.startswith('[]'):
                    k = k[2:]
                    as_list = True
                if self.__dict__.get(k) is not None:
                    stor = self.__dict__
                    if not as_list:
                        stor[k] = v(**stor[k])
                    else:
                        stor[k] = [v(**x) for x in stor[k]]

        dto_class.__init__ = __init__
        return dto_class
    return wrapper


def dto_kwargs_parser(func):
    def wrapper(dto_class: QRDTO):
        init = dto_class.__init__

        def __init__(self, *args, **kwargs):
            func(kwargs)
            init(self, *args, **kwargs)

        dto_class.__init__ = __init__
        return dto_class
    return wrapper