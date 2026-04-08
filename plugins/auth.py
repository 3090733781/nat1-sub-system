import functools
from flask import session, redirect, url_for, render_template, request, flash
import utils

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not session.get('logged_in'):
            if not utils.is_installed():
                return redirect(url_for('setup'))
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

def register(app):
    @app.route('/setup', methods=['GET', 'POST'])
    def setup():
        if utils.is_installed():
            return redirect(url_for('login'))
        if request.method == 'POST':
            password = request.form.get('password')
            confirm = request.form.get('confirm')
            if not password or password != confirm:
                flash('密码不能为空且两次输入必须一致', 'error')
                return render_template('setup.html')
            utils.set_password(password)
            utils.load_nodes()  # 确保默认节点生成
            session['logged_in'] = True
            return redirect(url_for('index'))
        return render_template('setup.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if not utils.is_installed():
            return redirect(url_for('setup'))
        if request.method == 'POST':
            password = request.form.get('password')
            if utils.verify_password(password):
                session['logged_in'] = True
                return redirect(url_for('index'))
            else:
                flash('密码错误', 'error')
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.pop('logged_in', None)
        return redirect(url_for('login'))