from flask import render_template, request
from .auth import login_required
import utils

def register(app):
    @app.route('/router_script')
    @login_required
    def router_script():
        nodes = utils.load_nodes()
        server = request.host
        if ':' not in server:
            server = f"{server}:9998"
        return render_template('router_script.html', nodes=nodes, server=server)