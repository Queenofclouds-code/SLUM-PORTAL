from flask import Flask
from model import db
from routes import slum_routes

app = Flask(
    __name__,
    template_folder="Frontend"
)

app.config.from_pyfile("config.py")

db.init_app(app)

app.register_blueprint(slum_routes)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
