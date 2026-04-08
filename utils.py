import os
import json
import base64
import secrets
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, 'config.json')

def generate_token():
    return secrets.token_urlsafe(16)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
    else:
        config = {
            "port": 9998,
            "data_dir": "sub",
            "nodes_file": "nodes.json",
            "password_file": "password.hash",
            "secret_key": "dev-key-change-in-production"
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
    # 确保有 sub_token
    if 'sub_token' not in config:
        config['sub_token'] = generate_token()
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
    return config

config = load_config()
DATA_DIR = os.path.join(BASE_DIR, config.get('data_dir', 'sub'))
NODES_FILE = os.path.join(BASE_DIR, config.get('nodes_file', 'nodes.json'))
PASSWORD_FILE = os.path.join(BASE_DIR, config.get('password_file', 'password.hash'))

os.makedirs(DATA_DIR, exist_ok=True)

# ---------- 密码操作 ----------
def is_installed():
    return os.path.exists(PASSWORD_FILE)

def verify_password(password):
    if not is_installed():
        return False
    with open(PASSWORD_FILE, 'r') as f:
        stored_hash = f.read().strip()
    return check_password_hash(stored_hash, password)

def set_password(password):
    hash_ = generate_password_hash(password)
    with open(PASSWORD_FILE, 'w') as f:
        f.write(hash_)

# ---------- 节点操作 ----------
def load_nodes():
    if os.path.exists(NODES_FILE):
        with open(NODES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        default_nodes = [
            {"id": 1, "name": "广西联通公免", "uuid": "afc170b9-39b8-433f-b4a7-1a2ded5adb96",
             "net": "ws", "host": "pull.free.video.10010.com", "path": "/", "tls": "none", "aid": "0"},
            {"id": 2, "name": "广西电信云盘", "uuid": "b15b4c3a-0746-4651-b750-ce04298afa1a",
             "net": "ws", "host": "download.cloud.189.cn", "path": "/", "tls": "none", "aid": "0"}
        ]
        save_nodes(default_nodes)
        return default_nodes

def save_nodes(nodes):
    with open(NODES_FILE, 'w', encoding='utf-8') as f:
        json.dump(nodes, f, indent=2, ensure_ascii=False)

# ---------- 动态数据 ----------
def get_current_ip():
    ip_file = os.path.join(DATA_DIR, 'current_ip.txt')
    if os.path.exists(ip_file):
        with open(ip_file, 'r') as f:
            ip = f.read().strip()
            if ip:
                if ':' in ip and '.' not in ip:
                    return f"[{ip}]"
                return ip
    return "0.0.0.0"

def get_port(node_id):
    port_file = os.path.join(DATA_DIR, f'port{node_id}.txt')
    if os.path.exists(port_file):
        with open(port_file, 'r') as f:
            port = f.read().strip()
            if port.isdigit():
                return int(port)
    return 10000

def build_vmess_link(node, ip, port):
    config = {
        "v": "2", "ps": node["name"], "add": ip, "port": port,
        "id": node["uuid"], "aid": node.get("aid", "0"),
        "net": node.get("net", "ws"), "type": node.get("type", "none"),
        "host": node.get("host", ""), "path": node.get("path", "/"),
        "tls": node.get("tls", "none")
    }
    return "vmess://" + base64.b64encode(json.dumps(config).encode()).decode()