import os
from flask import request
import utils

def register(app):
    @app.route('/setip', methods=['GET'])
    def set_ip():
        ip = request.args.get('ip', '')
        if not ip:
            return 'invalid ip', 400
        # 简单校验
        if not (ip.replace('.', '').replace(':', '').replace('[', '').replace(']', '').isalnum()):
            return 'invalid ip', 400
        ip_file = os.path.join(utils.DATA_DIR, 'current_ip.txt')
        with open(ip_file, 'w') as f:
            f.write(ip)
        return 'ok'

    @app.route('/set<int:node_id>', methods=['GET'])
    def set_port(node_id):
        port = request.args.get('p', '')
        if not port or not port.isdigit() or int(port) < 1 or int(port) > 65535:
            return 'invalid port', 400
        port_file = os.path.join(utils.DATA_DIR, f'port{node_id}.txt')
        with open(port_file, 'w') as f:
            f.write(port)
        return 'ok'