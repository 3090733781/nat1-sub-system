NAT1 节点订阅系统

一个用于家庭网络（动态公网 IP + NATMap 随机端口）的自动化 vmess 订阅管理系统。支持多节点、动态 IP/端口上报、管理员认证、订阅 token 保护。

## 功能特点

- 支持多个 vmess 节点，每个节点独立随机公网端口
- 路由器端通过 NATMap 自动上报公网 IP 和端口
- 管理员 Web 界面：节点管理、端口状态、一键生成路由器脚本
- 订阅地址受 token 保护，防止未授权访问
- 提供标准 vmess 订阅 (`/sub`)
- 数据持久化（本地文件存储）
- 一键安装脚本（自动配置 systemd 服务）

## 环境要求

- Linux 服务器（Ubuntu/Debian/CentOS）
- Python 3.6+
- 防火墙开放端口（默认 9998）

## 安装步骤

### 1. 下载源码

```bash
git clone https://github.com/3090733781/nat1-sub-system.git
cd nat1-sub-system
```
2. 创建虚拟环境并安装依赖
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```
3. 初始化配置
首次运行会自动生成 config.json（包含随机 token）和默认节点配置。

```bash
python app.py
```
访问 http://你的服务器IP:9998/setup 设置管理员密码。

4. 配置 systemd 服务（实现开机自启）
创建服务文件 /etc/systemd/system/vmess-sub.service：
```bash

ini
[Unit]
Description=Vmess Subscription Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/nat1-sub-system
ExecStart=/root/nat1-sub-system/venv/bin/python /root/nat1-sub-system/app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
启动并启用服务：

```bash
systemctl daemon-reload
systemctl enable vmess-sub
systemctl start vmess-sub
```
5. 开放防火墙端口
云服务商安全组：放行 TCP 9998 端口

系统防火墙（如有）：

```bash
# Ubuntu/Debian
ufw allow 9998/tcp
# CentOS
firewall-cmd --permanent --add-port=9998/tcp && firewall-cmd --reload
```
路由器端配置（NATMap）
登录管理后台，进入“生成路由器脚本”页面，复制对应节点的脚本到 OpenWrt 路由器，例如：

```bash
cat > /usr/bin/notify1.sh <<'EOF'
#!/bin/sh
curl -s "http://你的服务器IP:9998/setip?ip=$1"
curl -s "http://你的服务器IP:9998/set1?p=$2"
EOF
chmod +x /usr/bin/notify1.sh
```
然后在 NATMap 实例中指定该脚本。每个节点需要单独的通知脚本。

订阅地址
vmess 订阅：http://你的服务器IP:9998/sub?token=你的token

登录管理后台后，首页会显示带 token 的完整订阅地址。

管理 API
所有管理 API 需要登录（Cookie 认证）。

端点	方法	说明
/api/nodes	GET	获取节点列表
/api/node	POST	添加/更新节点
/api/node/<id>	DELETE	删除节点
/api/status/ip	GET	当前公网 IP
/api/status/ports	GET	各节点端口
配置文件说明
config.json（自动生成，可手动修改）：
```bash
json
{
  "port": 9998,
  "data_dir": "sub",
  "nodes_file": "nodes.json",
  "password_file": "password.hash",
  "secret_key": "随机字符串",
  "sub_token": "随机订阅token"
}
```
port：服务监听端口

data_dir：动态数据目录（存放 current_ip.txt 和 port*.txt）

sub_token：订阅地址 token，可自行修改

常见问题
1. 忘记管理员密码？
删除 password.hash 文件，重新访问 /setup 设置。

2. 订阅 token 泄露？
修改 config.json 中的 sub_token，重启服务。

3. 如何添加新节点？
登录管理后台，点击“+ 添加节点”，填写名称、UUID 等信息。保存后，在路由器上为新节点创建对应的通知脚本（NATMap 实例）。

4. 更新代码
```bash
cd /root/nat1-sub-system
git pull
systemctl restart vmess-sub
```
开发与扩展
插件位于 plugins/ 目录，实现 register(app) 即可自动加载。

可自行添加对 trojan、ss 等协议的支持。




将此文件保存为 `README.md` 并推送到仓库：

```bash
cd /www/wwwroot/sub
git add README.md
git commit -m "Add README (Python only, vmess only)"
git push
```
