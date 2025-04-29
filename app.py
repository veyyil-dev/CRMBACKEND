from flask import Flask
from dotenv import load_dotenv
from database import db
from models import Contact, Task, Lead
from routes import contact_bp
from routes.leads import leads_bp
from routes.activities import activities_bp
from routes.tasks import tasks_bp
from flask_cors import CORS
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Enable CORS for all routes
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

    # Database configuration
    database_url = "postgresql://neondb_owner:npg_Mm5HetcKZ9FD@ep-polished-truth-a4p42npb-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require"
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(contact_bp, url_prefix='/api')
    app.register_blueprint(leads_bp, url_prefix='/api')
    app.register_blueprint(activities_bp, url_prefix='/api')
    app.register_blueprint(tasks_bp, url_prefix='/api')

    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 