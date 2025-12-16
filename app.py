from flask import Flask, request, session, redirect, url_for, render_template_string
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key'

users = {
    'alice': {'password': 'alicepassword', 'is_admin': False},
    'bob': {'password': 'bobpassword', 'is_admin': False},
    'admin': {'password': 'adminpassword', 'is_admin': True}
}

login_page = """
<h2>Login</h2>
<form method="POST">
    Username: <input name="username"><br>
    Password: <input type="password" name="password"><br>
    <button type="submit">Login</button>
</form>
"""

dashboard_template = """
<h2>Dashboard</h2>
<p>Welcome, {{ user }}</p>
{% if is_admin %}
<p>You are an admin. Visit <a href='/admin'>/admin</a></p>
{% endif %}
"""
admin_template = """
<h2>Admin Area</h2>
<p>This is the admin dashboard.</p>
<p>But there's nothing sensitive here...</p>
"""

@app.route('/admin/flag')
def admin_flag():
    return "<h2>Internal Admin Tool</h2><code>FLAG{misconfig_admin_subroute_exposed}</code>"

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        user = users.get(uname)
        if user and user['password'] == pwd:
            session['user'] = uname
            return redirect('/dashboard')
        else:
            return "Invalid credentials", 403
    return render_template_string(login_page)

@app.route('/dashboard')
def dashboard():
    user = session.get('user')
    if not user:
        return redirect('/login')
    is_admin = users[user]['is_admin']
    return render_template_string(dashboard_template, user=user, is_admin=is_admin)

@app.route('/admin')
def admin_area():
    user = session.get('user')
    if not user or not users[user]['is_admin']:
        return "403 Forbidden", 403
    return render_template_string(admin_template)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
