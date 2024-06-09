from flask import Flask
from routes.routes import main
from config import Config

app = Flask(__name__, static_folder = Config.STATIC_FOLDER, template_folder = Config.TEMPLATE_FOLDER)
app.config.from_object(Config)

app.register_blueprint(main)

app.run(host = "0.0.0.0", debug = True, port = "5000")