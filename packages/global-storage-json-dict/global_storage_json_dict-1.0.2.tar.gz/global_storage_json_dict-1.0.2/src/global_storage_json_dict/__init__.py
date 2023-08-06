import importlib
from typing import Protocol


class ImportList:
    def __init__(self, *args, default: str):
        self.__import = self.__generate_imports(*args, default)

    @staticmethod
    def __generate_imports(*args):
        for arg in args:
            try:
                return importlib.import_module(arg)
            except ModuleNotFoundError:
                continue
        raise ModuleNotFoundError()

    def __call__(self):
        return self.__import


class JSONModule(Protocol):
    def loads(self, s: str) -> dict:
        ...

    def dumps(self, o: dict) -> str:
        ...


json_module_default: JSONModule = ImportList("ujson", "hyperjson", "orjson", default="json")()


class FileJsonStorage(dict):
    def __init__(self, file: str = None, default: dict = None, force_load: bool = False, auto_save: bool = True):
        """
        Создание хранилища для Flask
        :param file: Наименование файла для хранения всей информации на сервере
        :param default: Значение для хранилища по умолчанию
        :param force_load: Если True - то из файла не будем читать
        :param auto_save: Если True - автоматически при изменении будет пересохраняться
        """
        super().__init__()
        self._file = file or "flask-global-storage.json"
        self.update(default or dict())
        if not force_load:
            self.update(self.__on_load())
        self._auto_save = auto_save

    def __setitem__(self, k, v):  # real signature unknown
        """ Set self[key] to value. """
        super().__setitem__(k, v)
        self._auto_save and self.save()

    def save(self):
        with open(self._file, "w", encoding="utf-8") as f:
            f.write(json_module_default.dumps(self))

    def __on_load(self) -> dict:
        try:
            with open(self._file, "r", encoding="utf-8") as f:
                return json_module_default.loads(f.read())
        except FileNotFoundError:
            return dict()


Storage = FileJsonStorage()

__all__ = (
    "Storage",
    "FileJsonStorage"
)
