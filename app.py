from flask import Flask
from flask_cors import CORS

from routes.main import main_bp
from routes.programs import programs_bp
from routes.blog import blog_bp
from routes.admin import admin_bp

app = Flask(__name__)

app.config.from_object("config.Config")

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = "..."

CORS(app)

app.register_blueprint(main_bp)
app.register_blueprint(programs_bp)
app.register_blueprint(blog_bp)
app.register_blueprint(admin_bp)

if __name__ == "__main__":
    app.run(debug=True)