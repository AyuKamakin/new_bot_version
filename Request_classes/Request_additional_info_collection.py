import json
import jsonpickle
from Request_classes.Request_additional_info import Request_additional_info


class Request_additional_info_collection:
    def __init__(self):
        self._additional_info = {}

    def __getitem__(self, key):
        return self._additional_info[key]

    def __setitem__(self, key, value):
        self._additional_info[key] = value

    def __delitem__(self, key):
        del self._additional_info[key]

    def __iter__(self):
        return iter(self._additional_info)

    def __str__(self):
        return str(self._additional_info)

    def __len__(self):
        return len(self._additional_info)

    def keys(self):
        return self._additional_info.keys()

    def values(self):
        return self._additional_info.values()

    def clear(self):
        self._additional_info.clear()

    def get(self, key, default=None):
        return self._additional_info.get(key, default)

    def print(self):
        for key, value in self._additional_info.items():
            print(f'{key}: {value}')

    def to_json(self):
        return json.dumps(self._additional_info, ensure_ascii=False, default=lambda o: o.__dict__, indent=2)

    # раcкодировка из красивого json и копирование внутрь коллекции
    def copy_from_json(self, json_str):
        data = json.loads(json_str)
        for key, value in data.items():
            self.create_and_add_info(value['id'], value['equipment'], value['status'])

    def add_existing_info(self, new_info: Request_additional_info):
        if isinstance(new_info, Request_additional_info) and new_info.id not in self._additional_info.keys():
            self._additional_info[new_info.id] = new_info
            return True
        else:
            return False

    # Создание объекта класса Request_additional_info
    def create_and_add_info(self, new_id: int, new_comment: str, new_rating: int):
        req_info = Request_additional_info(id=new_id, comment=new_comment, rating=new_rating)
        self.add_existing_info(req_info)

    def get_info_by_id(self, new_id: int):
        if new_id in self._additional_info.keys():
            return self._additional_info.get(new_id)
        else:
            return False

    def update_info_by_id(self, changable_id: int, new_comment: str = None, new_rating: int = None):
        if self._additional_info.get(changable_id):
            if new_comment is not None:
                self._additional_info[changable_id].comment = new_comment
            if new_rating is not None:
                self._additional_info[changable_id].rating = new_rating
            return True
        else:
            return False

    def delete_info_by_id(self, id_to_del: int):
        if id_to_del in self._additional_info.keys():
            self._additional_info.pop(id_to_del)
            if self._additional_info.get(id_to_del) is None:
                return True
            else:
                return False
        else:
            return False

    def delete_info_by_id_list(self, id_to_del_list):
        for i in id_to_del_list:
            if isinstance(i, int):
                self.delete_info_by_id(i)
