import click

try:
    from config import Config
except Exception as e:
    from src.api.config import Config

@click.group(help="help")
def command():
    return True

@command.command()
def init():
    config = Config()
    config.create()
    return

@command.command()
def update():
    return

if __name__ == "__main__":
    command()
