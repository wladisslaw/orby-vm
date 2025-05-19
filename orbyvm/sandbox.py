import sys
from types import ModuleType

class Sandbox:
    def __init__(self, permissions):
        self.permissions = permissions
        self.allowed_modules = {"math", "json"}  # Пример белого списка

    def safe_import(self, name, *args, **kwargs):
        """Контроль импорта модулей."""
        if name not in self.allowed_modules:
            raise ImportError(f"Модуль {name} запрещён!")
        return __import__(name, *args, **kwargs)

def create_sandbox(permissions):
    """Возвращает изолированное globals() для exec()."""
    sandbox = Sandbox(permissions)
    return {
        "__builtins__": {"__import__": sandbox.safe_import},
        "print": print,  # Разрешённые функции
    }