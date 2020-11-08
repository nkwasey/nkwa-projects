__author__ = "Nana Ekow Nkwa Sey"

from flask import Flask


# Creating app object
def create_app():
    """ Initialize the core application """
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # Initialize plugins

    with app.app_context():
        # Include routes
        from . import routes

        # Import Dash application
        from .firemap.dashboard import init_dashboard
        app = init_dashboard(app)

        return app
