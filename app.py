import config
from flask import Flask
from routes import slum_routes
from model import db

# Initialize Flask app with the template and static folder
app = Flask(__name__)

# Load the configuration
app.config.from_object(config)

# Initialize the database
db.init_app(app)

# Register the routes blueprint
app.register_blueprint(slum_routes, url_prefix="/slum-portal/api")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

