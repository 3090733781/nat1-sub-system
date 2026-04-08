from flask import jsonify, request, abort
import utils
from .auth import login_required

def register(app):
    config = utils.load_config()
    sub_token = config.get('sub_token')

    @app.route('/sub', methods=['GET'])
    def sub():
        token = request.args.get('token')
        if not token:
            abort(404)
        if token != sub_token:
            abort(403)
        nodes = utils.load_nodes()
        ip = utils.get_current_ip()
        lines = []
        for node in nodes:
            port = utils.get_port(node['id'])
            lines.append(utils.build_vmess_link(node, ip, port))
        return "\n".join(lines), 200, {'Content-Type': 'text/plain; charset=utf-8'}

    @app.route('/sub/<token>', methods=['GET'])
    def sub_with_path(token):
        if token != sub_token:
            abort(403)
        nodes = utils.load_nodes()
        ip = utils.get_current_ip()
        lines = []
        for node in nodes:
            port = utils.get_port(node['id'])
            lines.append(utils.build_vmess_link(node, ip, port))
        return "\n".join(lines), 200, {'Content-Type': 'text/plain; charset=utf-8'}

    @app.route('/api/status/ip')
    def status_ip():
        ip = utils.get_current_ip()
        return jsonify({'ip': ip})

    @app.route('/api/status/ports')
    def status_ports():
        nodes = utils.load_nodes()
        ports = {node['id']: utils.get_port(node['id']) for node in nodes}
        return jsonify(ports)

    @app.route('/api/sub_token')
    @login_required
    def sub_token_api():
        return jsonify({'token': sub_token})