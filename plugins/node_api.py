from flask import request, jsonify, abort
from .auth import login_required
import utils

def register(app):
    @app.route('/api/nodes', methods=['GET'])
    @login_required
    def api_list_nodes():
        nodes = utils.load_nodes()
        return jsonify(nodes)

    @app.route('/api/node', methods=['POST'])
    @login_required
    def api_add_node():
        data = request.get_json()
        if not data:
            abort(400, 'Missing JSON')
        if 'id' not in data or 'uuid' not in data:
            abort(400, 'Missing required fields: id, uuid')
        nodes = utils.load_nodes()
        for i, n in enumerate(nodes):
            if n['id'] == data['id']:
                nodes[i] = data
                break
        else:
            nodes.append(data)
        utils.save_nodes(nodes)
        return jsonify({'status': 'ok', 'node': data})

    @app.route('/api/node/<int:node_id>', methods=['DELETE'])
    @login_required
    def api_delete_node(node_id):
        nodes = utils.load_nodes()
        new_nodes = [n for n in nodes if n['id'] != node_id]
        if len(new_nodes) == len(nodes):
            abort(404, 'Node not found')
        utils.save_nodes(new_nodes)
        return jsonify({'status': 'ok'})