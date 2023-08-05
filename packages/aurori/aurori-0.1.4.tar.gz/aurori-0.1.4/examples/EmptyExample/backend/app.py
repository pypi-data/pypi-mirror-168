""" The ordenario app. """

from aurori.config import Config
from aurori import create_app, db
from environment import create_environment

config = Config(config_path="config.ini")
app = create_app(config)

print()
print(app.url_map)

with app.app_context():
    create_environment(app, db)

if __name__ == '__main__':
    app.run()