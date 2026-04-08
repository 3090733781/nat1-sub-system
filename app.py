#!/usr/bin/env python3
import os
import importlib
from flask import Flask

# 加载配置
import utils
config = utils.load_config()

app = Flask(__name__)
app.secret_key = config.get('secret_key', 'dev-key-change-in-production')

# 加载插件
plugin_dir = os.path.join(os.path.dirname(__file__), 'plugins')
if os.path.exists(plugin_dir):
    for filename in os.listdir(plugin_dir):
        if filename.endswith('.py') and not filename.startswith('_'):
            module_name = f"plugins.{filename[:-3]}"
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, 'register'):
                    module.register(app)
                    print(f"Loaded plugin: {filename}")
            except Exception as e:
                print(f"Failed to load plugin {filename}: {e}")

if __name__ == '__main__':
    port = config.get('port', 9998)
    app.run(host='0.0.0.0', port=port, debug=False)