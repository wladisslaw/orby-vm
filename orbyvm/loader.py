import zipfile
import json
from pathlib import Path

from .sandbox import create_sandbox

class OrbyApp:
    def __init__(self, orby_path):
        self.path = Path(orby_path)
        self.manifest = self._load_manifest()
        self._validate()

    def _load_manifest(self):
        with zipfile.ZipFile(self.path, 'r') as zipf:
            with zipf.open('manifest.json') as f:
                return json.load(f)

    def _validate(self):
        required_fields = ["name", "version", "entry_point", "permissions"]
        for field in required_fields:
            if field not in self.manifest:
                raise ValueError(f"Манифест не содержит поле: {field}")

    def run(self):
        sandbox_env = create_sandbox(self.manifest["permissions"])
        with zipfile.ZipFile(self.path, 'r') as zipf:
            zipf.extractall("temp_orby_app")
        
        entry_path = Path("temp_orby_app") / self.manifest["entry_point"]
        with open(entry_path, "r") as f:
            code = compile(f.read(), entry_path, 'exec')
            exec(code, sandbox_env)

def load_orby_app(orby_path):
    return OrbyApp(orby_path)