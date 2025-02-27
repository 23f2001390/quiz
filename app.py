from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user
from models import db
from models.user import User

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'your-secret-key'  # Change this in production
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_master.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    bootstrap = Bootstrap()
    bootstrap.init_app(app)
    db.init_app(app)
    
    # Initialize Login Manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    from controllers.auth import auth
    from controllers.admin import admin
    from controllers.user import user
    from controllers.api import api
    
    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(user)
    app.register_blueprint(api)
    
    # Main route
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            if current_user.is_admin:
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('user.dashboard'))
        return redirect(url_for('auth.login'))
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True) 