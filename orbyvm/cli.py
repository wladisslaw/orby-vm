import click
from pathlib import Path
from .loader import load_orby_app

@click.command()
@click.argument("orby_file", type=click.Path(exists=True))
def main(orby_file):
    """Запускает .orby-приложение."""
    app = load_orby_app(orby_file)
    print(f"🚀 Запуск: {app.manifest['name']} v{app.manifest['version']}")
    print(f"🔐 Разрешения: {app.manifest['permissions']}")
    app.run()

if __name__ == "__main__":
    main()