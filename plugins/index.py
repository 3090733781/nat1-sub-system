from flask import render_template
from .auth import login_required

def register(app):
    @app.route('/')
    @login_required
    def index():
        return render_template('index.html')