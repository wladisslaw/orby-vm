from typing import Tuple
from pathlib import Path
import os
import sys
import subprocess


class Runner:
    """
    Класс предоставляет интерфейс запуска приложений.
    """

    @staticmethod
    def run_app(app_path: str, use_global_python: bool = False) -> Tuple[bool, Exception | None]:
        """
        Запускает приложение .orby.

        Args:
            app_path (str): Путь к приложению.
            use_global_python (bool, optional): Использовать ли предустановленную версию Python.
        
        Returns:
            Кортеж, содержащий:
                bool: Статус выполнения.
                Exception | None: Исключение, если возникла ошибка при запуске или работе приложения, 
                            None если ошибок не было.
        """

        try:
            if not use_global_python:
                python_exe = Path.home() / ".orby/python/bin/python"
            else:
                python_exe = Path(sys.executable)

            if not python_exe.exists():
                raise RuntimeError("Python interpreter not found.")
            
            env = os.environ.copy()
            env["PYTHONPATH"] = app_path
            env["ORBY_APP_PATH"] = app_path
            env["ORBY_IS_SANDBOXED"] = "1"

            env["PYTHONPATH"] += ":" + str(Path(__file__).parent)

            main_file = app_path / "main.py"
            if not main_file.exists():
                raise FileNotFoundError("main.py not found in app.")
            
            subprocess.run([str(python_exe), str(main_file)], env=env)
            
        except Exception as e:
            return False, e